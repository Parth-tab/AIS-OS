# Telegram Integration Guide

This guide describes how to connect and use the Telegram bot integration to send updates, alerts, and reminders to your personal Telegram account.

---

## 1. Setup Instructions

To connect your Telegram account to your AIOS:

1. **Create a Bot via BotFather**:
   - Open Telegram and search for the official account `@BotFather`.
   - Send the message `/newbot` to start the creation process.
   - Choose a display name for your bot (e.g., `Parth AIOS Bot`).
   - Choose a unique username for your bot ending in `bot` (e.g., `parth_aios_bot`).
   - Copy the **HTTP API Bot Token** provided by BotFather (looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

2. **Start the Chat**:
   - Click the link to your new bot (e.g., `t.me/your_bot_username`).
   - Click the **Start** button or send any test message (e.g., "Hello").

3. **Get Your Chat ID**:
   - Add your bot token temporarily to your `.env` file (see step 4).
   - Run the helper script to scan recent messages and find your Chat ID:
     ```bash
     python scripts/telegram_helper.py get_chat_id
     ```
   - Copy the printed Chat ID (usually a 9 or 10-digit number, e.g., `987654321`).

4. **Configure Environment Variables**:
   - Open or create your `.env` file at the root of your workspace (`E:\AIOS\AIS-OS\.env`).
   - Add the following keys:
     ```env
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     TELEGRAM_CHAT_ID=your_chat_id_here
     ```

---

## 2. CLI Usage

The script `scripts/telegram_helper.py` provides command-line functions to interact with the Telegram bot API.

### Get Chat ID
Scans incoming messages sent to the bot in the last 24 hours and prints the sender's Chat ID.
```bash
python scripts/telegram_helper.py get_chat_id
```

### Send Message
Sends a message to the configured `TELEGRAM_CHAT_ID` using Markdown formatting.
```bash
python scripts/telegram_helper.py send "Hello Parth! *CS50 study session* starts now. 🚀"
```

---

## 3. Telegram Bot API Details

- **Protocol**: HTTPS REST
- **Base URL**: `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>`
- **Headers**:
  - `Content-Type: application/json`
- **Common Endpoints**:
  - Get Updates: `GET /getUpdates`
  - Send Message: `POST /sendMessage`
    - Payload fields: `chat_id` (string/int), `text` (string), `parse_mode` ("Markdown" or "HTML")
