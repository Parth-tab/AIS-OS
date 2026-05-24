#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
import sys

# Load environment variables from .env file if it exists in the workspace root
def load_env():
    # Looks for .env in the parent directory of this script (assuming scripts/notion_helper.py)
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip("'\"` ")
                    os.environ[key] = val

load_env()

def get_clean_database_id(db_id_or_url):
    if not db_id_or_url:
        return None
    db_id_or_url = db_id_or_url.strip()
    if 'notion.so/' in db_id_or_url:
        # Extract path component (before query parameters or hashes)
        path = db_id_or_url.split('?')[0].split('#')[0]
        # The last segment of the path contains the ID
        last_segment = path.split('/')[-1]
        # It might be in the format Name-ID
        parts = last_segment.split('-')
        possible_id = parts[-1]
        if len(possible_id) == 32:
            return possible_id
        if len(last_segment) == 32:
            return last_segment
    return db_id_or_url

NOTION_TOKEN = os.environ.get('NOTION_INTEGRATION_TOKEN')
DATABASE_ID = get_clean_database_id(os.environ.get('NOTION_DATABASE_ID'))

def make_request(url, method='GET', data=None):
    if not NOTION_TOKEN:
        print("Error: NOTION_INTEGRATION_TOKEN environment variable not set.", file=sys.stderr)
        print("Please configure it in a .env file at the workspace root or set it in your system environment.", file=sys.stderr)
        sys.exit(1)
        
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode('utf-8')
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            err_body = json.loads(e.read().decode('utf-8'))
            print(f"Notion API Message: {err_body.get('message', '')}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error making request: {e}", file=sys.stderr)
        sys.exit(1)

def list_tasks():
    if not DATABASE_ID:
        print("Error: NOTION_DATABASE_ID environment variable not set.", file=sys.stderr)
        sys.exit(1)
        
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = make_request(url, method='POST')
    
    results = res.get('results', [])
    if not results:
        print("No tasks found in the database.")
        return
        
    print(f"{'ID':<36} | {'Title':<40} | {'Status':<15}")
    print("-" * 97)
    for page in results:
        page_id = page['id']
        properties = page.get('properties', {})
        
        # Determine title property dynamically
        title = "Untitled"
        for key, prop in properties.items():
            if prop.get('type') == 'title':
                title_list = prop.get('title', [])
                if title_list:
                    title = title_list[0]['text']['content']
                break
                
        # Determine status property dynamically
        status = "None"
        for key, prop in properties.items():
            prop_type = prop.get('type')
            if prop_type == 'status':
                status = prop.get('status', {}).get('name', 'None')
                break
            elif prop_type == 'select' and key.lower() in ['status', 'state', 'stage']:
                status = prop.get('select', {}).get('name', 'None')
                break
            
        print(f"{page_id:<36} | {title[:40]:<40} | {status:<15}")

def add_task(title, status_name="Not Started"):
    if not DATABASE_ID:
        print("Error: NOTION_DATABASE_ID environment variable not set.", file=sys.stderr)
        sys.exit(1)
        
    # Query database schema to find correct property names dynamically
    db_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    db_info = make_request(db_url, method='GET')
    db_properties = db_info.get('properties', {})
    
    title_prop_name = None
    status_prop_name = None
    status_type = None
    
    # Identify title property
    for key, prop in db_properties.items():
        if prop.get('type') == 'title':
            title_prop_name = key
            break
            
    # Identify status or select property for Status
    for key in ['Status', 'status', 'State', 'state']:
        if key in db_properties:
            prop_type = db_properties[key].get('type')
            if prop_type in ['status', 'select']:
                status_prop_name = key
                status_type = prop_type
                break
                
    # Fallback search for status if named differently
    if not status_prop_name:
        for key, prop in db_properties.items():
            if prop.get('type') == 'status':
                status_prop_name = key
                status_type = 'status'
                break
            elif prop.get('type') == 'select' and key.lower() in ['status', 'state', 'priority', 'stage']:
                status_prop_name = key
                status_type = 'select'
                break
                
    if not title_prop_name:
        print("Error: Could not find a 'title' type property in the Notion database schema.", file=sys.stderr)
        sys.exit(1)
        
    url = "https://api.notion.com/v1/pages"
    
    properties = {
        title_prop_name: {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }
    
    if status_prop_name:
        # Match option name capitalization if possible
        resolved_status_name = status_name
        options = []
        if status_type == 'status':
            options = db_properties[status_prop_name].get('status', {}).get('options', [])
        elif status_type == 'select':
            options = db_properties[status_prop_name].get('select', {}).get('options', [])
            
        for opt in options:
            if opt.get('name', '').lower() == status_name.lower():
                resolved_status_name = opt.get('name')
                break
                
        if status_type == 'status':
            properties[status_prop_name] = {
                "status": {
                    "name": resolved_status_name
                }
            }
        elif status_type == 'select':
            properties[status_prop_name] = {
                "select": {
                    "name": resolved_status_name
                }
            }
            
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": properties
    }
    
    res = make_request(url, method='POST', data=data)
    print(f"Successfully created task '{title}' with ID: {res.get('id')}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python notion_helper.py [list|add] [arguments...]")
        print("  list: Lists tasks in the Notion database")
        print("  add [title] [status]: Adds a new task to the database")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == 'list':
        list_tasks()
    elif action == 'add':
        if len(sys.argv) < 3:
            print("Error: 'add' action requires a task title.")
            sys.exit(1)
            
        title = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "Not Started"
        add_task(title, status)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()
