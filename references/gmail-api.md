# Gmail Integration Guide

This guide describes how to connect and use the Gmail integration to query and search your inbox.

---

## 1. Setup Instructions

The Gmail integration uses the same Google Cloud Console Desktop OAuth App credentials as the Google Drive and Calendar integrations.

### Step 1: Enable the Gmail API
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project **`Parth-AIOS`**.
3. In the sidebar, go to **APIs & Services** -> **Enabled APIs & Services**.
4. Click **+ Enable APIs and Services** at the top.
5. Search for `Gmail API` and click it.
6. Click **Enable**.

### Step 2: Ensure Auth Files are Ignored
Make sure your Gmail token file is ignored in `.gitignore`:
- Open `.gitignore` and ensure it has:
  ```
  credentials.json
  token.json
  token_calendar.json
  token_gmail.json
  ```

---

## 2. CLI Usage & Authentication

Before running the script, make sure Google API libraries are installed:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### First-Time Run (Authorization)
Run the script to start the OAuth consent flow:
```bash
python scripts/gmail_helper.py list
```
1. A browser window will open automatically asking you to log into your Google account.
2. If you see a "Google hasn't verified this app" screen, click **Advanced** -> **Go to Parth AIOS (unsafe)**.
3. Grant permissions for Gmail reading and return to the terminal.
4. A file named `token_gmail.json` will be generated in your root directory. Future runs will use this file for automatic logins.

### Usage Commands

#### List recent emails (defaults to 10):
```bash
python scripts/gmail_helper.py list
```

#### Search emails (supports standard Gmail search operators):
```bash
python scripts/gmail_helper.py search "subject:CS50"
python scripts/gmail_helper.py search "from:hbtu.ac.in"
python scripts/gmail_helper.py search "is:unread"
```

#### View email detail and body:
```bash
python scripts/gmail_helper.py get <message_id>
```

---

## 3. API Reference Details

- **Protocol**: HTTPS REST
- **Base URL**: `https://www.googleapis.com/gmail/v1`
- **Scope**: `https://www.googleapis.com/auth/gmail.readonly`
- **Core Endpoints**:
  - List Messages: `GET /users/me/messages`
    - Parameters: `q` (query), `maxResults`
  - Get Message: `GET /users/me/messages/<id>`
    - Format: `full` or `metadata`
