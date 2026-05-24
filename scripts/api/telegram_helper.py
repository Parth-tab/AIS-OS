#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
import sys

# Load environment variables from .env file if it exists in the workspace root
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip("'\"` ")
                    os.environ[key] = val

load_env()

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def make_request(method_name, data=None):
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.", file=sys.stderr)
        print("Please configure it in a .env file at the workspace root or set it in your system environment.", file=sys.stderr)
        sys.exit(1)
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method_name}"
    
    req_data = None
    headers = {}
    if data:
        req_data = json.dumps(data).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method='POST' if data else 'GET')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Telegram API Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            err_body = json.loads(e.read().decode('utf-8'))
            print(f"Message: {err_body.get('description', '')}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error making request to Telegram: {e}", file=sys.stderr)
        sys.exit(1)

def send_message(text):
    if not CHAT_ID:
        print("Error: TELEGRAM_CHAT_ID environment variable not set.", file=sys.stderr)
        print("Run 'python scripts/telegram_helper.py get_chat_id' to find it after messaging your bot.", file=sys.stderr)
        sys.exit(1)
        
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    res = make_request("sendMessage", data=payload)
    if res.get("ok"):
        print("Successfully sent message to Telegram!")
    else:
        print(f"Failed to send message: {res}", file=sys.stderr)

def get_chat_id():
    print("Fetching updates from Telegram to locate your Chat ID...")
    res = make_request("getUpdates")
    
    results = res.get("result", [])
    if not results:
        print("\nNo recent messages found. Please do the following first:")
        print("1. Search for your bot in Telegram and click 'Start' or send it a message.")
        print("2. Run this command again.")
        return
        
    print("\nRecent messages received by your bot:")
    print(f"{'Sender':<20} | {'Chat ID':<15} | {'Message Text':<30}")
    print("-" * 71)
    
    found_ids = set()
    for update in results:
        message = update.get("message", {})
        chat = message.get("chat", {})
        from_user = message.get("from", {})
        
        chat_id = chat.get("id")
        text = message.get("text", "")
        username = from_user.get("username", "")
        first_name = from_user.get("first_name", "")
        sender_name = f"@{username}" if username else first_name
        
        if chat_id:
            found_ids.add(chat_id)
            print(f"{sender_name:<20} | {chat_id:<15} | {text:<30}")
            
    if found_ids:
        print(f"\nRecommended CHAT_ID to use: {list(found_ids)[0]}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python telegram_helper.py [send|get_chat_id] [arguments...]")
        print("  send [text]: Sends a message to the configured CHAT_ID")
        print("  get_chat_id: Lists recent incoming messages and their Chat IDs")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == 'send':
        if len(sys.argv) < 3:
            print("Error: 'send' action requires a message text.")
            sys.exit(1)
        send_message(sys.argv[2])
    elif action == 'get_chat_id':
        get_chat_id()
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()
