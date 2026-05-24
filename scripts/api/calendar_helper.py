#!/usr/bin/env python3
"""
calendar_helper.py — Google Calendar integration for AIOS.

Capabilities:
  - list        : list upcoming calendar events for the next N days
"""
import os
import sys
import argparse
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Dependency guard
# ---------------------------------------------------------------------------
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Missing required Google API libraries.", file=sys.stderr)
    print("Install with:", file=sys.stderr)
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Scopes — calendar.readonly: Access to view events
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials():
    """Load or refresh credentials, triggering browser OAuth if needed."""
    creds = None
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(workspace_root, ".secrets", "token_calendar.json")
    creds_path = os.path.join(workspace_root, ".secrets", "credentials.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"Error: '{creds_path}' not found.", file=sys.stderr)
                print("Download your OAuth Client ID credentials from Google Cloud Console", file=sys.stderr)
                print("and place it at the workspace root.", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds


def build_service():
    """Return an authenticated Calendar v3 service object."""
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)


def list_events(days=7, max_results=20):
    """List calendar events starting from now up to N days in the future."""
    # Ensure console can handle any output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    try:
        service = build_service()
        
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        end_date = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

        print(f"Retrieving events for the next {days} days...")
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=end_date,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        print(f"\n{'Start Time':<25} | {'Event Summary':<45} | {'Location/Link':<35}")
        print("-" * 110)
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "(No Title)")
            location = event.get("location", event.get("hangoutLink", "—"))
            
            # Format start time slightly for cleaner display
            if "T" in start:
                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                start_formatted = dt.strftime("%Y-%m-%d %H:%M")
            else:
                start_formatted = f"{start} (All Day)"

            print(f"{start_formatted:<25} | {summary[:45]:<45} | {location[:35]:<35}")

    except HttpError as error:
        print(f"An API error occurred: {error}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Google Calendar Helper — list upcoming calendar events."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # --- list ---
    list_parser = subparsers.add_parser("list", help="List upcoming calendar events")
    list_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days in the future to list events for (default: 7)"
    )
    list_parser.add_argument(
        "--max",
        type=int,
        default=20,
        help="Maximum number of events to return (default: 20)"
    )

    args = parser.parse_args()

    if args.action == "list":
        list_events(days=args.days, max_results=args.max)


if __name__ == "__main__":
    main()
