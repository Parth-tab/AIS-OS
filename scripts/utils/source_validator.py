#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import time

def load_config():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(workspace_root, 'context', 'study_config.yaml')
    
    # Minimal YAML parsing to avoid dependencies
    config = {
        "domain_reputations": {},
        "cache_settings": {
            "reputation_cache_path": "study/cache/domain_reputations.json",
            "reputation_ttl_days": 30
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                current_section = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if line.endswith(':'):
                        current_section = line[:-1].strip()
                        continue
                    if current_section == "domain_reputations":
                        parts = line.split(':')
                        if len(parts) >= 2:
                            domain = parts[0].strip().strip('"').strip("'")
                            rep = parts[1].strip().strip('"').strip("'")
                            config["domain_reputations"][domain] = rep
        except Exception as e:
            print(f"Warning: Failed parsing YAML config: {e}", file=sys.stderr)
            
    return config

def get_domain(url):
    try:
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""

def check_reputation(domain, config):
    # Check manual configs
    reputations = config["domain_reputations"]
    if domain in reputations:
        return reputations[domain]
    
    # Fallback to suffix checks
    if domain.endswith(".edu") or domain.endswith(".gov") or domain.endswith(".org"):
        return "HIGH"
    if domain.endswith(".com") or domain.endswith(".net") or domain.endswith(".io"):
        return "MEDIUM"
        
    return "LOW"

def check_wayback_archive(url):
    archive_url = f"http://archive.org/wayback/available?url={urllib.parse.quote(url)}"
    try:
        req = urllib.request.Request(
            archive_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read().decode('utf-8'))
            snapshots = data.get("archived_snapshots", {})
            if snapshots and "closest" in snapshots:
                return snapshots["closest"].get("url", "")
    except Exception:
        pass
    return ""

def validate_url(url, config):
    result = {
        "url": url,
        "accessible": False,
        "status_code": 0,
        "reputation": "LOW",
        "archive_url": "",
        "timestamp": time.time()
    }
    
    domain = get_domain(url)
    if not domain:
        return result
        
    result["reputation"] = check_reputation(domain, config)
    
    # Check accessibility
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result["accessible"] = True
            result["status_code"] = response.getcode()
    except HTTPError as e:
        result["status_code"] = e.code
    except URLError:
        result["status_code"] = -1
    except Exception:
        result["status_code"] = -99
        
    # Check archive
    result["archive_url"] = check_wayback_archive(url)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python source_validator.py [url]")
        sys.exit(1)
        
    url = sys.argv[1]
    config = load_config()
    print(f"Validating source: {url}")
    result = validate_url(url, config)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
