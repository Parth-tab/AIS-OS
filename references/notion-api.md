# Notion Task Integration Guide

This guide describes how to connect and use the Notion Task integration script to track tasks, homework, and projects for your AIOS.

---

## 1. Setup Instructions

To connect your Notion workspace:

1. **Create a Notion Integration**:
   - Go to [Notion Developers](https://www.notion.so/my-integrations).
   - Click **+ New Integration**.
   - Set Name to `Parth-AIOS`, select the correct Workspace, and submit.
   - Under **Secrets**, copy the **Internal Integration Token** (e.g., `secret_...`).

2. **Set Up Task Database**:
   - Create a new Database in Notion (e.g., choose the "To-do list" template or create a table database).
   - Ensure it has the default properties:
     - `Name` (Type: Title)
     - `Status` (Type: Status)
   - Copy the Database ID from the URL of your Notion database page:
     - `https://www.notion.so/workspace-name/DATABASE_ID?v=...`
     - The Database ID is the 32-character alphanumeric string between the workspace name slash and the question mark.

3. **Share Database with Integration**:
   - In Notion, navigate to your database page.
   - Click the triple dots `...` in the top right corner.
   - Go to **Connections** -> **Connect to** and search for `Parth-AIOS`.
   - Select it and confirm to share access.

4. **Add Credentials to Environment**:
   - Create a `.env` file at the root of your workspace (`E:\AIOS\AIS-OS\.env`) and add:
     ```env
     NOTION_INTEGRATION_TOKEN=your_secret_integration_token_here
     NOTION_DATABASE_ID=your_database_id_here
     ```

---

## 2. API Reference & Usage

The script `scripts/notion_helper.py` provides simple task management utilities using Notion's public API.

### List Tasks
Queries the database to return the ID, Title, and Status of all pages.
```bash
python scripts/notion_helper.py list
```

### Add Task
Adds a new task to your Notion database.
```bash
python scripts/notion_helper.py add "Finish CS50 Lecture 1" "Not Started"
```
*Note: Available statuses typically include "Not Started", "In Progress", or "Done" depending on your database settings.*

---

## 3. Notion API Details

- **Protocol**: HTTP/1.1 REST
- **Base URL**: `https://api.notion.com/v1`
- **Headers**:
  - `Authorization: Bearer <NOTION_INTEGRATION_TOKEN>`
  - `Notion-Version: 2022-06-28`
  - `Content-Type: application/json`
- **Common Endpoints**:
  - Query Database: `POST /v1/databases/<DATABASE_ID>/query`
  - Create Page (Task): `POST /v1/pages`
  - Update Page (Task): `PATCH /v1/pages/<PAGE_ID>`
