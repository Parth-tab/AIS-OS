# Google Calendar Integration Guide

This guide describes how to connect and use the Google Calendar integration to list and monitor upcoming events.

---

## 1. Setup Instructions

The Google Calendar integration uses the same Google Cloud Console Desktop OAuth App credentials as the Google Drive integration.

### Step 1: Enable the Google Calendar API
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project **`Parth-AIOS`** (the one created during the Google Drive setup).
3. In the sidebar, go to **APIs & Services** -> **Enabled APIs & Services**.
4. Click **+ Enable APIs and Services** at the top.
5. Search for `Google Calendar API` and click it.
6. Click **Enable**.

### Step 2: Ensure Auth Files are Ignored
Make sure your calendar token file is ignored in `.gitignore`:
- Open `.gitignore` and ensure it has:
  ```
  credentials.json
  token.json
  token_calendar.json
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
python scripts/calendar_helper.py list
```
1. A browser window will open automatically asking you to log into your Google account.
2. If you see a "Google hasn't verified this app" screen, click **Advanced** -> **Go to Parth AIOS (unsafe)**.
3. Grant permissions for Calendar viewing and return to the terminal.
4. A file named `token_calendar.json` will be generated in your root directory. Future runs will use this file for automatic logins.

### Usage Commands

#### List upcoming events (defaults to next 7 days):
```bash
python scripts/calendar_helper.py list
```

#### List upcoming events for next 14 days:
```bash
python scripts/calendar_helper.py list --days 14
```

#### Limit results:
```bash
python scripts/calendar_helper.py list --days 30 --max 10
```

---

## 3. API Reference Details

- **Protocol**: HTTPS REST
- **Base URL**: `https://www.googleapis.com/calendar/v3`
- **Scope**: `https://www.googleapis.com/auth/calendar.readonly`
- **Core Endpoints**:
  - List Events: `GET /calendars/primary/events`
    - Parameters: `timeMin`, `timeMax`, `singleEvents=True`, `orderBy="startTime"`
