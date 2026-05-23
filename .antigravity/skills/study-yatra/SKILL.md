---
name: study-yatra
description: >
  Manages Microsoft AI Skills Yatra study plans, schedules, timelines, checklists, and visual HTML planners.
  Triggers on: study-yatra, yatra, microsoft yatra, ais-skills-yatra, yatra planner, yatra schedule.
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# Microsoft AI Skills Yatra Study System

Use this skill when the user wants to check progress, sync courses to Notion, trigger Telegram reminders, or print the dynamic schedule for the Microsoft AI Skills Yatra initiative.

---

## 1. Core Commands

- **Sync all courses to Notion database:**
  ```powershell
  python scripts/yatra_planner_helper.py --sync-notion
  ```

- **Send Telegram status notification:**
  ```powershell
  python scripts/yatra_planner_helper.py --notify-telegram
  ```

- **Print study schedule:**
  ```powershell
  python scripts/yatra_planner_helper.py --schedule --start-date "2026-05-25"
  ```

- **Generate checklists and dashboard HTML:**
  ```powershell
  python scripts/generate_yatra_checklists.py
  python scripts/generate_yatra_dashboard.py
  ```

---

## 2. Browser Automation Commands (Chrome DevTools / Puppeteer)

If you are currently studying and want the AIOS to assist you by fetching page text or taking screenshots of dynamic slides/diagrams:

- **Launch Chrome headed to Log In (Run once to save your session):**
  ```powershell
  python scripts/yatra_planner_helper.py --browser-login
  ```

- **Scrape dynamically loaded course text:**
  ```powershell
  python scripts/yatra_planner_helper.py --scrape-page "https://learn.microsoft.com/en-us/..." --output "study/AI_Skills_Yatra/scraped_content.txt"
  ```

- **Capture a screenshot of a slide or diagram:**
  ```powershell
  python scripts/yatra_planner_helper.py --screenshot-page "https://learn.microsoft.com/en-us/..." --output "study/AI_Skills_Yatra/slide_screenshot.png"
  ```

---

## 3. Directories & Artifacts

- **Checklists Directory:** `study/AI_Skills_Yatra/`
  - Contains folders for **Copilot**, **AI**, and **Security** containing individual checklist files.
- **Visual Planner Dashboard:** `study/AI_Skills_Yatra/study_planner.html`
  - Open this file in your browser to view your progress, complete units, and click on checklists.
- **Timeline:** `study/AI_Skills_Yatra/timeline.md`
  - Structured 6-day intensive summer sprint schedule.
