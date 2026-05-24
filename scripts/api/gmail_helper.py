#!/usr/bin/env python3
"""
gmail_helper.py — Gmail integration for AIOS.

Capabilities:
  - list        : list recent emails
  - search      : search emails matching a query string
  - get         : fetch and print details of a specific email by ID
"""
import os
import sys
import argparse
import base64

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
# Scopes — gmail.readonly: Access to view messages and metadata
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials():
    """Load or refresh credentials, triggering browser OAuth if needed."""
    creds = None
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(workspace_root, ".secrets", "token_gmail.json")
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
    """Return an authenticated Gmail v1 service object."""
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def _get_header(headers, name):
    """Find a specific header value by name."""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return "—"


def list_messages(max_results=10, query=""):
    """List or search recent messages."""
    # Ensure console can handle any output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    try:
        service = build_service()
        
        # Call the Gmail API
        result = service.users().messages().list(
            userId="me",
            maxResults=max_results,
            q=query
        ).execute()
        
        messages = result.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print(f"\n{'ID':<18} | {'From':<35} | {'Subject':<50}")
        print("-" * 110)
        
        for msg in messages:
            msg_details = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "Subject"]
            ).execute()
            
            headers = msg_details.get("payload", {}).get("headers", [])
            sender = _get_header(headers, "From")
            subject = _get_header(headers, "Subject")

            # Clean up display strings
            sender_clean = sender.split("<")[0].strip() if "<" in sender else sender
            
            print(f"{msg['id']:<18} | {sender_clean[:35]:<35} | {subject[:50]:<50}")

    except HttpError as error:
        print(f"An API error occurred: {error}", file=sys.stderr)


def get_message_detail(message_id):
    """Fetch and display the details and body of a single message."""
    # Ensure console can handle any output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    try:
        service = build_service()
        msg = service.users().messages().get(userId="me", id=message_id).execute()
        
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        
        subject = _get_header(headers, "Subject")
        sender = _get_header(headers, "From")
        date = _get_header(headers, "Date")

        print("=" * 80)
        print(f"Subject : {subject}")
        print(f"From    : {sender}")
        print(f"Date    : {date}")
        print(f"ID      : {message_id}")
        print("=" * 80)

        # Extract message body
        body = ""
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                        break
        else:
            data = payload.get("body", {}).get("data")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        if not body:
            # Fallback if text/plain is nested inside multipart/alternative
            parts = payload.get("parts", [])
            for p in parts:
                if p.get("mimeType") == "multipart/alternative":
                    subparts = p.get("parts", [])
                    for sp in subparts:
                        if sp["mimeType"] == "text/plain":
                            data = sp["body"].get("data")
                            if data:
                                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                                break

        if body:
            # Output first 1500 chars to avoid cluttering console
            print(body[:1500])
            if len(body) > 1500:
                print("\n... [Truncated. Use web interface to view full email] ...")
        else:
            print("[No plain text body found for this email]")
            
        print("=" * 80)

    except HttpError as error:
        print(f"An API error occurred: {error}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Gmail Helper — list, search, and view emails."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # --- list ---
    list_parser = subparsers.add_parser("list", help="List recent emails")
    list_parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="Maximum number of emails to retrieve (default: 10)"
    )

    # --- search ---
    search_parser = subparsers.add_parser("search", help="Search emails matching a query")
    search_parser.add_argument("query", help="Gmail search query (e.g. 'subject:CS50' or 'from:google')")
    search_parser.add_argument(
        "--max",
        type=int,
        default=5,
        help="Maximum number of search results to retrieve (default: 5)"
    )

    # --- get ---
    get_parser = subparsers.add_parser("get", help="Get full details of a specific email")
    get_parser.add_argument("id", help="The Gmail message ID")

    args = parser.parse_args()

    if args.action == "list":
        list_messages(max_results=args.max)
    elif args.action == "search":
        list_messages(max_results=args.max, query=args.query)
    elif args.action == "get":
        get_message_detail(args.id)


if __name__ == "__main__":
    main()
