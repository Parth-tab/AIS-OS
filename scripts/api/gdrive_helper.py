#!/usr/bin/env python3
"""
gdrive_helper.py — Google Drive integration for AIOS Study Agent.

Capabilities:
  - list        : list top-N files in Drive
  - sync        : upload/update study artifacts to AIOS/Study/<course>/ folder
  - upload      : upload a single file to a specific Drive folder ID

Re-auth note:
  Scope upgraded from drive.readonly → drive.file.
  Delete token.json once so the new scope is requested on next run.
"""
import os
import sys
import argparse

# ---------------------------------------------------------------------------
# Dependency guard
# ---------------------------------------------------------------------------
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("Error: Missing required Google API libraries.", file=sys.stderr)
    print("Install with:", file=sys.stderr)
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Scopes — drive.file: create & update files this app owns
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Root folder name that will be created at the top of My Drive
DRIVE_ROOT_FOLDER = "AIOS"
DRIVE_STUDY_FOLDER = "Study"

# Map common file extensions to MIME types
MIME_MAP = {
    ".md":   "text/markdown",
    ".txt":  "text/plain",
    ".c":    "text/x-csrc",
    ".cpp":  "text/x-c++src",
    ".h":    "text/x-chdr",
    ".py":   "text/x-python",
    ".json": "application/json",
    ".yaml": "application/x-yaml",
    ".yml":  "application/x-yaml",
}


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def get_credentials():
    """Load or refresh credentials, triggering browser OAuth if needed."""
    creds = None
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(workspace_root, ".secrets", "token.json")
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
    """Return an authenticated Drive v3 service object."""
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)


# ---------------------------------------------------------------------------
# Folder utilities
# ---------------------------------------------------------------------------
def get_or_create_folder(service, name, parent_id=None):
    """
    Find a Drive folder by name (under parent_id if given).
    Create it if it doesn't exist. Returns the folder ID.
    """
    query_parts = [
        f"name = '{name}'",
        "mimeType = 'application/vnd.google-apps.folder'",
        "trashed = false",
    ]
    if parent_id:
        query_parts.append(f"'{parent_id}' in parents")

    query = " and ".join(query_parts)

    try:
        results = service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)",
            pageSize=5,
        ).execute()
        folders = results.get("files", [])

        if folders:
            return folders[0]["id"]

        # Folder not found — create it
        meta = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            meta["parents"] = [parent_id]

        folder = service.files().create(body=meta, fields="id").execute()
        print(f"  [Drive] Created folder: {name}")
        return folder["id"]

    except HttpError as err:
        print(f"Drive API error while resolving folder '{name}': {err}", file=sys.stderr)
        raise


def ensure_drive_path(service, *folder_names):
    """
    Ensure a chain of nested folders exists in Drive and return the
    deepest folder's ID.

    Example: ensure_drive_path(service, "AIOS", "Study", "CS50")
    """
    parent_id = None
    for name in folder_names:
        parent_id = get_or_create_folder(service, name, parent_id)
    return parent_id


# ---------------------------------------------------------------------------
# File upload / update
# ---------------------------------------------------------------------------
def _guess_mime(local_path):
    """Guess MIME type from extension."""
    _, ext = os.path.splitext(local_path)
    return MIME_MAP.get(ext.lower(), "text/plain")


def upload_or_update_file(service, local_path, folder_id):
    """
    Upload a file to Drive (under folder_id).
    If a file with the same name already exists in that folder,
    UPDATE its content instead of creating a duplicate.

    Returns the Drive file ID.
    """
    if not os.path.isfile(local_path):
        print(f"  [Drive] Skipped (not found locally): {local_path}", file=sys.stderr)
        return None

    filename = os.path.basename(local_path)
    mime_type = _guess_mime(local_path)
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=False)

    # Search for existing file in the target folder
    query = (
        f"name = '{filename}' "
        f"and '{folder_id}' in parents "
        f"and trashed = false"
    )
    try:
        results = service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)",
            pageSize=5,
        ).execute()
        existing = results.get("files", [])

        if existing:
            # Update existing file content — keeps the same Drive link
            file_id = existing[0]["id"]
            service.files().update(
                fileId=file_id,
                media_body=media,
            ).execute()
            print(f"  [Drive] Updated: {filename}")
            return file_id
        else:
            # Create new file in folder
            meta = {"name": filename, "parents": [folder_id]}
            file = service.files().create(
                body=meta,
                media_body=media,
                fields="id",
            ).execute()
            print(f"  [Drive] Uploaded: {filename}")
            return file["id"]

    except HttpError as err:
        print(f"Drive API error for '{filename}': {err}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Top-level sync entry point (used by study_helper and SKILL)
# ---------------------------------------------------------------------------
def sync_study_artifacts(course, topic, file_paths):
    """
    Sync a list of local file paths to Drive at:
        My Drive / AIOS / Study / <course> /

    Args:
        course     : e.g. "CS50"
        topic      : e.g. "memory-pointers" (used only for logging)
        file_paths : list of absolute or workspace-relative file paths
    """
    # Ensure console can handle any output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print(f"\n[Drive Sync] Course={course}  Topic={topic}")
    print(f"[Drive Sync] Ensuring folder path: AIOS -> Study -> {course}")

    service = build_service()
    folder_id = ensure_drive_path(service, DRIVE_ROOT_FOLDER, DRIVE_STUDY_FOLDER, course)

    synced, skipped = 0, 0
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for path in file_paths:
        # Resolve relative paths from workspace root
        if not os.path.isabs(path):
            path = os.path.join(workspace_root, path)

        if os.path.isfile(path):
            upload_or_update_file(service, path, folder_id)
            synced += 1
        else:
            print(f"  [Drive] File not found, skipping: {path}", file=sys.stderr)
            skipped += 1

    print(f"\n[Drive Sync] Done — {synced} file(s) synced, {skipped} skipped.")
    return synced


# ---------------------------------------------------------------------------
# CLI list function (backward-compatible)
# ---------------------------------------------------------------------------
def list_files(page_size=15):
    """List top N files in Drive."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    try:
        service = build_service()
        results = service.files().list(
            pageSize=page_size,
            fields="nextPageToken, files(id, name, mimeType)",
        ).execute()
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        print(f"{'ID':<33} | {'Name':<40} | {'Mime Type':<30}")
        print("-" * 110)
        for item in items:
            print(f"{item['id']:<33} | {item['name'][:40]:<40} | {item['mimeType']:<30}")

    except HttpError as error:
        print(f"An API error occurred: {error}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="AIOS Google Drive Helper — upload study artifacts or list files."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # --- list ---
    subparsers.add_parser("list", help="List top 15 files in your Google Drive")

    # --- sync ---
    sync_parser = subparsers.add_parser(
        "sync", help="Sync local study files to Drive AIOS/Study/<course>/"
    )
    sync_parser.add_argument("--course", required=True, help="Course name (e.g. CS50)")
    sync_parser.add_argument("--topic", required=True, help="Topic name (for logging)")
    sync_parser.add_argument(
        "--files",
        required=True,
        help="Comma-separated list of local file paths to sync",
    )

    # --- upload (single file to a specific folder ID) ---
    up_parser = subparsers.add_parser("upload", help="Upload a single file to a Drive folder ID")
    up_parser.add_argument("--file", required=True, help="Local path to the file")
    up_parser.add_argument("--folder-id", required=True, help="Drive folder ID to upload into")

    args = parser.parse_args()

    if args.action == "list":
        list_files()

    elif args.action == "sync":
        paths = [p.strip() for p in args.files.split(",") if p.strip()]
        sync_study_artifacts(args.course, args.topic, paths)

    elif args.action == "upload":
        service = build_service()
        upload_or_update_file(service, args.file, args.folder_id)


if __name__ == "__main__":
    main()
