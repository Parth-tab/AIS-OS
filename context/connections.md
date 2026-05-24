# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from your Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | None (Student) | not yet connected | — | — |
| 2 | Customer interactions | Gmail | script | key+ref | 2026-05-23 |
| 3 | Calendar | Google Calendar | script | key+ref | 2026-05-23 |
| 4 | Communication | Telegram | script | key+ref | 2026-05-23 |
| 5 | Project / task tracking | Notion | script | key+ref | 2026-05-23 |
| 6 | Meeting intelligence | None | not yet connected | — | — |
| 7 | Knowledge / files | Google Drive | script | key+ref | 2026-05-23 |
| 8 | Knowledge / RAG | NotebookLM | mcp | key+ref | 2026-05-23 |


**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
