#!/usr/bin/env python3
import os
import sys
import json
import re
import argparse
import time
import urllib.request
import urllib.parse
import yaml
from utils.source_validator import validate_url, load_config

def extract_youtube_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_youtube_transcript(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join([t.text for t in transcript])
    except ImportError:
        return "[Error: 'youtube-transcript-api' package is not installed.]"
    except Exception as e:
        return f"[Error fetching transcript: {str(e)}]"

def load_local_context(course, topic):
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_paths = [
        os.path.join(workspace_root, 'context', 'courses', f"{course.lower()}.md"),
        os.path.join(workspace_root, 'context', 'courses', f"{course.lower()}_{topic.lower().replace(' ', '_')}.md")
    ]
    for path in search_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    return ""

def prompt_for_clipboard():
    print("\n--- Clipboard / Console Prompt Fallback ---")
    print("Paste any additional lecture notes, slide text, or code examples below.")
    print("When finished, press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to save:\n")
    try:
        lines = sys.stdin.read()
        return lines.strip()
    except Exception as e:
        return f"[Error reading console: {str(e)}]"

def get_dork_templates(course, config_yaml):
    templates = config_yaml.get("dork_templates", {})
    course_key = course.lower()
    if course_key in templates:
        return templates[course_key]
    return templates.get("default", [])

def scrape_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            uddg_links = re.findall(r'uddg=([^"&]+)', html)
            links = []
            for link in uddg_links:
                decoded = urllib.parse.unquote(link)
                if decoded.startswith("http") and "duckduckgo.com" not in decoded:
                    links.append(decoded)
            return list(dict.fromkeys(links))[:5]
    except Exception as e:
        print(f"Warning: DuckDuckGo search failed: {e}", file=sys.stderr)
        return []

def load_cache(cache_path):
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(cache_path, cache_data):
    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def run_dork_pipeline(course, topic, config_yaml):
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load Cache
    cache_settings = config_yaml.get("cache_settings", {})
    cache_path = os.path.join(workspace_root, cache_settings.get("search_cache_path", "study/cache/dork_results.json"))
    search_ttl = cache_settings.get("search_ttl_days", 30) * 86400
    cache = load_cache(cache_path)
    
    cache_key = f"{course.lower()}:{topic.lower()}"
    now = time.time()
    
    if cache_key in cache:
        cached_entry = cache[cache_key]
        if now - cached_entry.get("timestamp", 0) < search_ttl:
            print("Found fresh cached dork results.")
            return cached_entry.get("results", [])
            
    print(f"Generating search dorks for topic '{topic}'...")
    templates = get_dork_templates(course, config_yaml)
    
    all_links = []
    failed_queries = []
    
    for temp in templates:
        query = temp.format(topic=topic)
        print(f"Executing search: {query}")
        links = scrape_duckduckgo(query)
        if links:
            all_links.extend(links)
            # Randomized jitter delay between queries to prevent throttling
            time.sleep(1)
        else:
            failed_queries.append(query)
            
    # Clean and validate links
    unique_links = list(dict.fromkeys(all_links))
    validated_sources = []
    
    val_config = load_config()
    for link in unique_links:
        print(f"Validating source trust: {link}")
        res = validate_url(link, val_config)
        # Keep only accessible and high/medium reputation files
        if res["accessible"] and res["reputation"] in ["HIGH", "MEDIUM"]:
            validated_sources.append({
                "url": link,
                "reputation": res["reputation"],
                "archive_url": res["archive_url"]
            })
            
    # Interactive Fallback: If searches failed or returned empty results
    if failed_queries or not validated_sources:
        print("\n--- [Interactive Fallback] Query Execution Blocked or Empty ---")
        print("Alternative queries to run manually in your browser:")
        for q in failed_queries:
            encoded_q = urllib.parse.quote(q)
            print(f"  - DuckDuckGo: https://html.duckduckgo.com/html/?q={encoded_q}")
            print(f"  - Google: https://google.com/search?q={encoded_q}")
            
    # Save cache
    cache[cache_key] = {
        "timestamp": now,
        "results": validated_sources
    }
    save_cache(cache_path, cache)
    
    return validated_sources

def main():
    parser = argparse.ArgumentParser(description="Gather context for AIOS study generator.")
    parser.add_argument("--topic", required=True, help="Topic name")
    parser.add_argument("--course", required=True, help="Course name")
    parser.add_argument("--youtube", help="Optional YouTube URL")
    parser.add_argument("--interactive", action="store_true", help="Prompt for manual paste")
    parser.add_argument("--dork", action="store_true", help="Perform academic dork searches")
    parser.add_argument("--map-dir", help="Directory path to scan and map C++ classes")
    parser.add_argument(
        "--drive-sync",
        action="store_true",
        help="After context is saved, sync study artifacts to Google Drive AIOS/Study/<course>/",
    )
    args = parser.parse_args()

    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_yaml_path = os.path.join(workspace_root, 'config', 'study_config.yaml')
    
    with open(config_yaml_path, 'r', encoding='utf-8') as f:
        config_yaml = yaml.safe_load(f)

    context_data = {
        "topic": args.topic,
        "course": args.course,
        "youtube_url": args.youtube or "",
        "youtube_transcript": "",
        "local_context": "",
        "interactive_context": "",
        "dork_results": [],
        "codebase_map": ""
    }

    # 1. Fetch YouTube Transcript
    if args.youtube:
        video_id = extract_youtube_id(args.youtube)
        if video_id:
            print(f"Fetching transcript for YouTube video ID: {video_id}...")
            context_data["youtube_transcript"] = fetch_youtube_transcript(video_id)
        else:
            print("Warning: Invalid YouTube URL format.")

    # 2. Fetch Local Context
    local_txt = load_local_context(args.course, args.topic)
    if local_txt:
        print(f"Found local context file for course '{args.course}'.")
        context_data["local_context"] = local_txt

    # 3. Interactive console fallback
    if args.interactive:
        context_data["interactive_context"] = prompt_for_clipboard()

    # 4. Optional OSINT Dorking Sweep
    if args.dork:
        context_data["dork_results"] = run_dork_pipeline(args.course, args.topic, config_yaml)

    # 5. Optional Codebase Dependency Map
    if args.map_dir:
        from utils.code_mapper import CodebaseMapper
        print(f"Scanning codebase for dependency mapping: {args.map_dir}")
        mapper = CodebaseMapper(args.map_dir)
        mapper.scan_files()
        context_data["codebase_map"] = mapper.generate_mermaid()

    # 6. Save consolidated output
    output_dir = os.path.join(workspace_root, 'study')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'cache', 'temp_context.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(context_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConsolidated context successfully written to: {output_path}")

    # 7. Optional: Sync existing study artifacts to Google Drive
    # The SKILL generates .md and code files AFTER this script runs.
    # Pass --drive-sync to have the SKILL call gdrive_helper directly,
    # OR re-run this script with --drive-sync after the SKILL finishes.
    if args.drive_sync:
        import re as _re
        topic_slug = _re.sub(r'[\s_]+', '-', args.topic.lower().strip())
        topic_slug = _re.sub(r'[^\w-]', '', topic_slug)
        course_dir = os.path.join(workspace_root, 'study', args.course)

        # Collect any already-generated artifact files for this topic
        candidate_extensions = [".md", ".c", ".cpp", ".py", ".h"]
        files_to_sync = []
        for ext in candidate_extensions:
            candidate = os.path.join(course_dir, f"{topic_slug}{ext}")
            if os.path.isfile(candidate):
                files_to_sync.append(candidate)
        # Also include checklist if it exists
        checklist_path = os.path.join(course_dir, f"{topic_slug}-checklist.md")
        if os.path.isfile(checklist_path):
            files_to_sync.append(checklist_path)

        if files_to_sync:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from api.gdrive_helper import sync_study_artifacts
            sync_study_artifacts(args.course, args.topic, files_to_sync)
        else:
            print(
                "[Drive Sync] No study files found for this topic yet.\n"
                "  Generate the study sheet first (via /study skill), then re-run with --drive-sync."
            )

if __name__ == "__main__":
    main()
