#!/usr/bin/env python3
import os
import json
import urllib.request
import sys

# Load environment
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip("'\"` ")

load_env()

NOTION_TOKEN = os.environ.get('NOTION_INTEGRATION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

if 'notion.so/' in DATABASE_ID:
    path = DATABASE_ID.split('?')[0].split('#')[0]
    DATABASE_ID = path.split('/')[-1].split('-')[-1]

if not NOTION_TOKEN or not DATABASE_ID:
    print("Error: Missing NOTION_INTEGRATION_TOKEN or NOTION_DATABASE_ID")
    sys.exit(1)

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as res:
        db_info = json.loads(res.read().decode('utf-8'))
        print("Database Title:", db_info.get('title', [{}])[0].get('text', {}).get('content', 'Untitled'))
        print("\nProperties in your Notion Database:")
        print("-" * 50)
        for prop_name, prop_val in db_info.get('properties', {}).items():
            print(f"Name: {prop_name:<25} | Type: {prop_val.get('type')}")
except Exception as e:
    print("Error:", e)
