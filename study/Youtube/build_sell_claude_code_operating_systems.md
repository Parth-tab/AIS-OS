# Study Guide: Build & Sell Claude Code Operating Systems

This study guide consolidates the concepts from Nate Herk's video on building and scaling personal/agency AI Operating Systems (AIOS).

---

## 1. Explanation
An **AI Operating System (AIOS)** is an intelligent layer built on top of your development environment (e.g., Antigravity, Claude Code, or VS Code) that serves as a single cockpit for your entire workflow. Unlike a standard LLM chat interface, an AIOS has access to all your local files, active API connections, custom skills, and scheduled routines. It transitions the AI from a simple "vending machine" (one prompt, one response) into an active, context-aware "mentor" and teammate.

---

## 2. Significance
Building an AIOS represents a massive leverage shift for freelance service delivery and personal productivity:
*   **The 30% Rule**: You don't need to automate 100% of a job. Automating 30% to 50% of a manual, repetitive task generates huge compounding productivity gains.
*   **Tool Agnosticism**: Standardizing the underlying frameworks (3Ms and 4Cs) ensures that even if specific LLMs or tools change, your automation architecture remains durable.
*   **Freelance Readiness**: Automating your own workflows teaches you how to design, package, and sell high-ticket automation scripts to small businesses.

---

## 3. Types/Variants (The 4Cs Framework)
An AIOS is built sequentially across four distinct structural layers:
1.  **Context**: The brain of the system. Knows who you are, what you sell, your voice registry, and your priorities (e.g., `GEMINI.md`, `context/`).
2.  **Connections**: The sensors. Reaches your data domains via APIs, MCP servers, or browser automation (e.g., Notion, Telegram, Google Drive).
3.  **Capabilities**: The muscles. Custom skills and sub-agents that execute SOPs (e.g., `.antigravity/skills/`).
4.  **Cadence**: The heartbeat. Autonomous background routines that run without being prompted (e.g., cron jobs, scheduled reminders).

---

## 4. Implementation Guide
To build a custom connection or capability in your AIOS:
1.  **Identify the Target**: Define the specific task and system to connect.
2.  **Create API Key / Credentials**: Save them to a local `.env` file (never check this into git).
3.  **Write the Gatherer Script**: Create a Python script in `scripts/` to handle raw API requests.
4.  **Create the Skill File**: Write a `SKILL.md` under `.antigravity/skills/` to define the SOP for the agent.
5.  **Register the Command**: Add the shortcut command to your master operating manual (`GEMINI.md`).

---

## 5. Real-World Illustration (The 3Ms Framework)
The **3Ms Framework** guides how you approach automation opportunities:
*   **Mindset**: The lens to find leverage.
    *   *Default Shift*: Before doing a task, ask: *"To what extent can AI do this?"*
    *   *Function Breakdown*: Decompose a massive goal (like "making a YouTube video") into tiny modular tasks (e.g., drafting titles, scraping transcripts).
*   **Method**: The scoring system. Filter candidate automations by checking:
    *   *Eliminate / Automate / Delegate*: Can we just stop doing this task entirely? If not, automate it.
    *   *Autonomy Levels (L0-L4)*: Start at L1 (human decides every step) before trying to build L4 (full autonomy).
*   **Machine**: The implementation.
    *   *Lego Principle*: Build small, reusable scripts first.
    *   *Validation Chain*: Verify step 1 works before chaining it to step 2.

---

## 6. Short Assignment
1.  **Analyze Your Role**: List 3 tasks you did more than 3 times this week. Apply the *Function Breakdown* to one of them.
2.  **Sketch a Connection**: Choose a tool you use daily (e.g., Spotify, Trello, or Gmail). Write down:
    - What is the trigger?
    - What are the data sources and destinations?
    - Which API mechanism (MCP, Python script, or Export) would you use?
3.  **Audit Your Setup**: What is your current AIOS score out of 100? Identify the single highest-leverage gap.

---

## 7. Core Nature (The 7 Universal Data Domains)
When building connections for a client or yourself, map them to these 7 Tier-1 data domains:
```
[Domain]                 | [Example Tools]            | [AIOS Integration Mechanism]
-------------------------|----------------------------|-------------------------------
1. Revenue/Financials    | Stripe, QuickBooks, Skool  | API Script (Read-only for safety)
2. Customer Interactions | HubSpot, Salesforce, CRM   | API / Browser Automation
3. Calendar              | Google Calendar, Outlook   | MCP Server (gcal)
4. Communication         | Gmail, Slack, Telegram     | Python script (Read/Write)
5. Project/Tasks         | Notion, ClickUp, Linear    | Notion API / notion_helper.py
6. Meeting Intelligence  | Fireflies, Otter.ai        | Webhook transcript collector
7. Knowledge/Files       | Google Drive, local files  | Google Drive API / token.json
```

---

## 8. Checklist
- [ ] Internalized the *Default Shift* (asking "To what extent can AI do this?")
- [ ] Mapped the 7 Universal Data Domains in `connections.md`
- [ ] Saved a client secrets file (`credentials.json`) for Google Drive
- [ ] Created your first custom agent skill in `.antigravity/skills/`
- [ ] Logged a configuration decision in `decisions/log.md`
- [ ] Ran `/audit` to establish your baseline score
