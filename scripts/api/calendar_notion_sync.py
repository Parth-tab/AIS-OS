#!/usr/bin/env python3
"""
calendar_notion_sync.py — Syncs study events from Google Calendar to Notion.

Looks for calendar events in the next N days containing keywords like
"Study", "CS50", "C++", "C ", "Calculus", "OOP" and inserts them into
the Notion Goals Tracker database if they don't already exist.
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# Import Google Calendar auth from calendar_helper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from calendar_helper import build_service as build_calendar_service
except ImportError:
    print("Error: calendar_helper.py must be in the same folder as this script.", file=sys.stderr)
    sys.exit(1)

# Keywords to identify "study" events
STUDY_KEYWORDS = ["study", "cs50", "c++", "c language", "oop", "calculus", "dsa", "review"]

# ---------------------------------------------------------------------------
# Notion API Utilities
# ---------------------------------------------------------------------------
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip("'\"` ")

load_env()

NOTION_TOKEN = os.environ.get('NOTION_INTEGRATION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

def get_clean_database_id(db_id_or_url):
    if not db_id_or_url:
        return None
    db_id_or_url = db_id_or_url.strip()
    if 'notion.so/' in db_id_or_url:
        path = db_id_or_url.split('?')[0].split('#')[0]
        last_segment = path.split('/')[-1]
        parts = last_segment.split('-')
        possible_id = parts[-1]
        if len(possible_id) == 32:
            return possible_id
        if len(last_segment) == 32:
            return last_segment
    return db_id_or_url

DATABASE_ID = get_clean_database_id(DATABASE_ID)


def make_notion_request(url, method='GET', data=None):
    if not NOTION_TOKEN:
        print("Error: NOTION_INTEGRATION_TOKEN not set in environment or .env.", file=sys.stderr)
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
        print(f"Notion API HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            print(f"Message: {json.loads(e.read().decode('utf-8')).get('message', '')}", file=sys.stderr)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"Error making request to Notion: {e}", file=sys.stderr)
        return None


def find_notion_task(title):
    """Query Notion to check if a task with the exact title already exists."""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    query_data = {
        "filter": {
            "property": "Goal name",
            "title": {
                "equals": title
            }
        }
    }
    res = make_notion_request(url, method='POST', data=query_data)
    if res and res.get("results"):
        return res["results"][0]  # Return existing page if found
    return None


def add_notion_task(title, due_date_iso):
    """Add a new task to Notion with a due date."""
    url = "https://api.notion.com/v1/pages"
    
    # Format date dictionary
    # If the date string has a time component (e.g. 2026-05-24T12:30:00Z)
    # Notion accepts it directly as start date.
    date_prop = {"start": due_date_iso}

    properties = {
        "Goal name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Due date": {
            "date": date_prop
        },
        "Status": {
            "status": {
                "name": "Not started"
            }
        },
        "Priority": {
            "select": {
                "name": "Medium"
            }
        }
    }
    
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": properties
    }
    
    res = make_notion_request(url, method='POST', data=data)
    if res:
        print(f"  [Notion] Created task: '{title}' (Due: {due_date_iso[:16].replace('T', ' ')})")
        return res.get("id")
    return None

# ---------------------------------------------------------------------------
# Sync Logic
# ---------------------------------------------------------------------------
def sync_calendar_to_notion(days=7):
    # Reconfigure stdout for Windows compatibility
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print(f"Syncing Google Calendar events to Notion (Looking ahead {days} days)...")
    
    try:
        calendar_service = build_calendar_service()
    except Exception as e:
        print(f"Error connecting to Google Calendar: {e}", file=sys.stderr)
        sys.exit(1)

    now = datetime.utcnow().isoformat() + "Z"
    end_date = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

    try:
        events_result = calendar_service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
    except Exception as e:
        print(f"Error fetching Google Calendar events: {e}", file=sys.stderr)
        sys.exit(1)

    if not events:
        print("No events found in Google Calendar for the specified timeframe.")
        return

    synced_count = 0
    skipped_count = 0

    print(f"Found {len(events)} total events. Filtering for study keywords...")
    
    for event in events:
        summary = event.get("summary", "")
        if not summary:
            continue

        # Check if the summary matches any of our keywords
        is_study_event = any(kw in summary.lower() for kw in STUDY_KEYWORDS)
        
        if is_study_event:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            
            # If all-day event (format: YYYY-MM-DD), format it for Notion
            if len(start_time) == 10:
                start_time_iso = start_time
            else:
                # Keep standard ISO format (e.g. 2026-05-24T12:30:00+05:30)
                start_time_iso = start_time
            
            print(f"\nProcessing event: '{summary}' ({start_time_iso[:16].replace('T', ' ')})")
            
            # Check if it already exists in Notion
            existing = find_notion_task(summary)
            if existing:
                print(f"  [Notion] Task already exists. Skipping.")
                skipped_count += 1
            else:
                # Add to Notion
                task_id = add_notion_task(summary, start_time_iso)
                if task_id:
                    synced_count += 1

    print(f"\nSync complete. Synced: {synced_count} new task(s), Skipped: {skipped_count} existing task(s).")


def main():
    parser = argparse.ArgumentParser(
        description="Sync study schedule events from Google Calendar to Notion Goals Tracker."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days in the future to search for events (default: 7)"
    )
    args = parser.parse_args()

    if not DATABASE_ID:
        print("Error: NOTION_DATABASE_ID is missing from environment.", file=sys.stderr)
        sys.exit(1)

    sync_calendar_to_notion(days=args.days)


if __name__ == "__main__":
    main()
