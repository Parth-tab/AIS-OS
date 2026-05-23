# Google Drive Integration Guide

This guide describes how to connect and use the Google Drive integration to access, list, and search files inside your personal or college Google Drive account.

---

## 1. Setup Instructions

To connect Google Drive to your AIOS, you need to configure an OAuth 2.0 Client ID in the Google Cloud Console.

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown in the top-left corner and select **New Project**.
3. Name your project `Parth-AIOS` and click **Create**.

### Step 2: Enable the Google Drive API
1. In the sidebar, go to **APIs & Services** -> **Enabled APIs & Services**.
2. Click **+ Enable APIs and Services** at the top.
3. Search for `Google Drive API` and click it.
4. Click **Enable**.

### Step 3: Configure the OAuth Consent Screen
1. Go to **APIs & Services** -> **OAuth consent screen** in the sidebar.
2. Select **External** (or Internal if using a school/workspace domain) and click **Create**.
3. Fill in the required fields:
   - **App name**: `Parth AIOS`
   - **User support email**: Your Gmail address
   - **Developer contact information**: Your Gmail address
4. Click **Save and Continue**.
5. **Scopes Screen**: Click **Save and Continue** (no scopes needed to be added explicitly here).
6. **Test Users Screen**: Click **+ Add Users** and type your Gmail address. (Crucial, since the app is in "Testing" mode!). Click **Save and Continue**.
7. Click **Back to Dashboard**.

### Step 4: Download Credentials
1. Go to **APIs & Services** -> **Credentials** in the sidebar.
2. Click **+ Create Credentials** at the top and select **OAuth client ID**.
3. Set **Application type** to **Desktop app**.
4. Set **Name** to `Parth AIOS Desktop`.
5. Click **Create**.
6. In the modal that appears, click **Download JSON**.
7. Rename the downloaded file to exactly **`credentials.json`** and save it at the root of your workspace (`E:\AIOS\AIS-OS\credentials.json`).

### Step 5: Ignore Auth Files in `.gitignore`
Make sure `token.json` and `credentials.json` are ignored so they don't get checked into Git:
- Open `.gitignore` and add:
  ```
  credentials.json
  token.json
  ```

---

## 2. CLI Usage & Authentication

Before running the script, install the required Google libraries:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### First-Time Run (Authorization)
Run the script for the first time:
```bash
python scripts/gdrive_helper.py list
```
1. A browser window will open automatically asking you to log into your Google account.
2. If you see a "Google hasn't verified this app" screen, click **Advanced** -> **Go to Parth AIOS (unsafe)**. (This is normal for personal developer test apps).
3. Approve permissions and return to the terminal.
4. A file named `token.json` will be generated in your root directory. Future script runs will use this file for automatic login.

### Usage Commands

#### List files
Lists the top 15 files in your Google Drive:
```bash
python scripts/gdrive_helper.py list
```

---

## 3. API Reference Details

- **Protocol**: HTTPS REST
- **Base URL**: `https://www.googleapis.com/drive/v3`
- **Scope**: `https://www.googleapis.com/auth/drive.readonly` (Access to read metadata and contents of all files in Google Drive).
- **Core Endpoints**:
  - List Files: `GET /files`
    - Fields: `files(id, name, mimeType)`
