#!/usr/bin/env python3
import os
import sys

# Try to import google API libraries. If not present, explain how to install them.
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Missing required Google API libraries.", file=sys.stderr)
    print("Please install them by running:", file=sys.stderr)
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
    sys.exit(1)

# Google Drive Read-Only Scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_credentials():
    creds = None
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(workspace_root, 'token.json')
    creds_path = os.path.join(workspace_root, 'credentials.json')

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"Error: '{creds_path}' not found.", file=sys.stderr)
                print("Please download your credentials.json (OAuth Client ID) from Google Cloud Console", file=sys.stderr)
                print("and place it at the root of your workspace.", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def list_files(page_size=15):
    # Reconfigure stdout to use UTF-8 to prevent UnicodeEncodeErrors on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    try:
        creds = get_credentials()
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API to list files
        results = service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
            
        print(f"{'ID':<33} | {'Name':<40} | {'Mime Type':<30}")
        print("-" * 110)
        for item in items:
            print(f"{item['id']:<33} | {item['name'][:40]:<40} | {item['mimeType']:<30}")
            
    except HttpError as error:
        print(f"An API error occurred: {error}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python gdrive_helper.py [list] [arguments...]")
        print("  list: Lists the top 15 files in your Google Drive")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == 'list':
        list_files()
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()
