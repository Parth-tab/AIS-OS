#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta

COURSES = [
    {"num": 1, "level": "Explorer", "name": "Get started with Microsoft 365 Copilot Chat", "category": "Copilot", "duration": 24, "day": 1},
    {"num": 2, "level": "Fluency", "name": "Work smarter with AI using Microsoft Copilot", "category": "Copilot", "duration": 65, "day": 1},
    {"num": 3, "level": "Mastery", "name": "Transform your everyday work with agents", "category": "Copilot", "duration": 232, "day": 2},
    {"num": 4, "level": "Explorer", "name": "Explore AI basics and Generative AI", "category": "AI", "duration": 95, "day": 3},
    {"num": 5, "level": "Fluency", "name": "Learn more on the AI concepts", "category": "AI", "duration": 40, "day": 3},
    {"num": 6, "level": "Mastery", "name": "Develop computer vision solutions in Azure", "category": "AI", "duration": 167, "day": 4},
    {"num": 7, "level": "Explorer", "name": "Describe the concepts of cybersecurity", "category": "Security", "duration": 137, "day": 5},
    {"num": 8, "level": "Fluency", "name": "Introduction to security, compliance, and identity concepts", "category": "Security", "duration": 97, "day": 5},
    {"num": 9, "level": "Mastery", "name": "Introduction to Microsoft security solutions", "category": "Security", "duration": 216, "day": 6}
]

def sync_notion(start_date_str="2026-05-25"):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    print("Syncing courses to Notion database with updated due dates...")
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    notion_helper = os.path.join(scripts_dir, 'notion_helper.py')
    
    for c in COURSES:
        day_offset = c['day'] - 1
        due_date = start_date + timedelta(days=day_offset)
        task_title = f"AI Skills Yatra: Day {c['day']} - {c['level']} - {c['name']} (Due: {due_date.strftime('%b %d')})"
        print(f"Adding task: {task_title}")
        
        cmd = [sys.executable, notion_helper, 'add', task_title, 'Not started']
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  Success: {res.stdout.strip()}")
        else:
            print(f"  Error: {res.stderr.strip()}", file=sys.stderr)

def send_telegram():
    print("Sending Telegram notification...")
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    telegram_helper = os.path.join(scripts_dir, 'telegram_helper.py')
    
    msg = (
        "*🔥 Microsoft AI Skills Yatra Intensive Sprint (6-Day Plan)!*\n\n"
        "Parth, since you are on summer break, I have accelerated your study plan to 3-4 hours a day:\n"
        "• *Day 1:* Copilot Explorer & Fluency (89 mins)\n"
        "• *Day 2:* Copilot Mastery - Agents (232 mins)\n"
        "• *Day 3:* AI Explorer & Fluency (135 mins)\n"
        "• *Day 4:* AI Mastery - Computer Vision (167 mins)\n"
        "• *Day 5:* Security Explorer & Fluency (234 mins)\n"
        "• *Day 6:* Security Mastery (216 mins)\n\n"
        "Check Notion for updated daily tasks and track details on [study_planner.html](file:///E:/AIOS/AIS-OS/study/AI_Skills_Yatra/study_planner.html)!"
    )
    
    cmd = [sys.executable, telegram_helper, 'send', msg]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("Telegram notification sent successfully!")
    else:
        print(f"Error sending Telegram notification: {res.stderr.strip()}", file=sys.stderr)

def print_schedule(start_date_str="2026-05-25"):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    print(f"\n======================================================================")
    print(f"AI SKILLS YATRA: INTENSIVE 6-DAY SUMMER SPRINT (Starting Monday, {start_date.strftime('%B %d, %Y')})")
    print(f"======================================================================")
    
    for c in COURSES:
        day_offset = c['day'] - 1
        study_date = start_date + timedelta(days=day_offset)
        date_str = study_date.strftime('%a, %b %d, %Y')
        print(f"Day {c['day']} | {c['category']:<8} | {c['level']:<8} | {date_str:<22} | {c['name'][:40]:<40} ({c['duration']} mins)")

def run_browser_tool(action, url, output=None, headed=False):
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    js_helper = os.path.join(scripts_dir, 'browser_helper.js')
    
    cmd = ['node', js_helper, '--action', action, '--url', url]
    if output:
        cmd.extend(['--output', output])
    if headed:
        cmd.append('--headed')
        
    print(f"Executing browser action: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Manage Microsoft AI Skills Yatra Summer Sprint.")
    parser.add_argument('--sync-notion', action='store_true', help="Sync all 9 courses with daily targets to Notion")
    parser.add_argument('--notify-telegram', action='store_true', help="Send Telegram sprint alert")
    parser.add_argument('--schedule', action='store_true', help="Print the 6-day study schedule")
    parser.add_argument('--start-date', default="2026-05-25", help="Start date in YYYY-MM-DD format")
    
    # Browser features
    parser.add_argument('--browser-login', action='store_true', help="Launch headed browser to log in to Microsoft Learn")
    parser.add_argument('--scrape-page', help="URL of course page to scrape text from")
    parser.add_argument('--screenshot-page', help="URL of course page to capture as full screenshot")
    parser.add_argument('--output', help="Filepath to save scraped text or screenshot image")
    parser.add_argument('--headed', action='store_true', help="Run browser in headed mode (visible window)")
    
    args = parser.parse_args()
    
    # Check if browser actions are targeted
    if args.browser_login:
        run_browser_tool('scrape', 'https://learn.microsoft.com/en-us/plans/', headed=True)
        return
        
    if args.scrape_page:
        if not args.output:
            print("Error: --output [filepath] is required when using --scrape-page.", file=sys.stderr)
            sys.exit(1)
        run_browser_tool('scrape', args.scrape_page, args.output, args.headed)
        return
        
    if args.screenshot_page:
        if not args.output:
            print("Error: --output [filepath] is required when using --screenshot-page.", file=sys.stderr)
            sys.exit(1)
        run_browser_tool('screenshot', args.screenshot_page, args.output, args.headed)
        return
        
    if not any([args.sync_notion, args.notify_telegram, args.schedule]):
        parser.print_help()
        sys.exit(1)
        
    if args.schedule:
        print_schedule(args.start_date)
        
    if args.sync_notion:
        sync_notion(args.start_date)
        
    if args.notify_telegram:
        send_telegram()

if __name__ == '__main__':
    main()
