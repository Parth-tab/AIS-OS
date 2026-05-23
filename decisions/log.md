# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-05-23 — Connected Google Drive Integration

**Decision:** Fully wired and authorized the Google Drive integration. Installed missing python API dependencies and fixed UnicodeEncodeErrors in the helper script on Windows.

**Why:** Google Drive acts as Parth's primary knowledge base and file storage. Connecting it completes the core data domains and makes files searchable.

**Alternatives considered:** Using manual CSV export pipelines, but it is too slow for frequent file queries.

**Owner:** Antigravity (AIOS Assistant) & Parth (Operator)

---

## 2026-05-23 — Created `/study` consolidated generator skill

**Decision:** Designed and implemented the consolidated Study Sheet & Reference Code Generator (`generating-study-guides` skill) utilizing a Python gatherer script to aggregate YouTube transcripts, local outlines, and interactive console clips, while querying NotebookLM and push-syncing practice tasks to Notion.

**Why:** Automates the most time-consuming part of learning CS (note-taking and summarizing) and instantly scaffolds runnable examples, allowing Parth to dedicate 100% of study time to coding and practice.

**Alternatives considered:** Keeping each tool separate, but a unified workflow is far lower friction and avoids API/login bottlenecks by utilizing robust fallback loops.

**Owner:** Antigravity (AIOS Assistant) & Parth (Operator)

---

## 2026-05-23 — Created `/recon` and `/dork` OSINT investigator skill

**Decision:** Implemented the `investigating-osint` skill to run advanced open-source intelligence gathering and research workflows locally in the workspace, registering the command vectors `/recon` and `/dork` in [GEMINI.md](file:///E:/AIOS/AIS-OS/GEMINI.md).

**Why:** Equips the AIOS with a highly structured playbook for general-purpose research, digital footprint analysis, and structured reporting, while establishing strong OPSEC checklists and ethical boundaries.

**Alternatives considered:** Relying on default chat instructions, which leads to inconsistent reporting formats and loose OPSEC considerations.

**Owner:** Antigravity (AIOS Assistant) & Parth (Operator)

