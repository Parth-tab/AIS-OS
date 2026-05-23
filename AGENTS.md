# AGENTS.md — AIS-OS (Parth's AI Operating System)

> This file is read by all coding agents on every invocation. It encodes the engineering
> philosophy, architecture constraints, and operational rules for this project.
> Treat it as a senior engineer's tribal knowledge dump.

---

## Project Overview

**What this is:** A personal AI Operating System (AIOS) that acts as Parth's thought partner for learning computer science fundamentals, C/C++ OOP, and building projects with AI agents.

**Tech stack:**
- Language: Python 3.x (scripts), C/C++ (study code), Markdown (skills/docs)
- Agent runtime: Google Antigravity CLI
- Package manager: `pip` (standard library preferred; `yaml`, `youtube-transcript-api` as exceptions)
- External APIs: Google Drive API, Notion API, Telegram Bot API, Wayback Machine API
- Search: DuckDuckGo HTML fallback (no API key required)
- Caching: Local JSON files in `study/cache/`
- Config: `context/study_config.yaml` (single source of truth for search/domain settings)

**Repo layout:**
```
AIS-OS/
├── .antigravity/skills/     # Agent skill definitions (SKILL.md per skill)
│   ├── audit/
│   ├── generating-study-guides/
│   ├── investigating-osint/
│   ├── level-up/
│   └── onboard/
├── context/                 # Parth's personal context (filled by /onboard)
│   ├── courses/             # Per-course local context outlines (cs50.md, etc.)
│   ├── about-me.md
│   ├── about-business.md
│   ├── priorities.md
│   └── study_config.yaml   # Dork templates, engine URLs, domain reputations
├── scripts/                 # Python helper scripts
│   ├── study_helper.py      # Main orchestrator: transcripts, dorking, codebase mapping
│   ├── code_mapper.py       # C++ class/inheritance → Mermaid diagram
│   ├── source_validator.py  # URL reputation + Wayback Machine check
│   ├── notion_helper.py     # Notion task creation
│   ├── gdrive_helper.py     # Google Drive file search
│   └── telegram_helper.py   # Telegram notifications
├── references/              # Frameworks and voice samples (3ms-framework.md, voice.md)
├── decisions/log.md         # Append-only decision record
├── archives/                # Old content — move here, never delete
├── study/                   # Generated study outputs (gitignored: temp_context.json, cache/)
├── connections.md           # Registry of every connected system
├── aios-intake.md           # Onboarding intake form
├── GEMINI.md                # Gemini CLI entry point and slash command registry
└── AGENTS.md                # This file
```

---

## Folder Conventions

> Violating these conventions is a bug, not a style preference.

- `.antigravity/skills/<name>/` — One folder per skill. Each must contain a `SKILL.md`. No logic lives here, only instructions.
- `scripts/` — All Python helper scripts. Each script must be independently runnable via `python scripts/<name>.py --help`.
- `context/` — Personal context about Parth. **Never auto-generate into this folder.** Only `/onboard` writes here.
- `context/courses/` — One `.md` file per course (e.g., `cs50.md`). File name must match the `--course` argument to `study_helper.py` (lowercase, underscores for spaces).
- `study/` — Generated outputs only. `temp_context.json` and `cache/` are gitignored.
- `references/` — Read-only reference files. Never overwrite; append or archive.
- `decisions/log.md` — Append-only. Never edit past entries. Add new ones at the bottom.
- `archives/` — Graveyard for retired files. Move here, never delete.

**Cross-boundary rules:**
- `scripts/` must never import from `.antigravity/` or `context/` except via file path reads.
- `source_validator.py` must not import `yaml` — it uses its own minimal YAML parser to stay dependency-light.
- `study_helper.py` is the only entry point that imports other scripts (`code_mapper`, `source_validator`). Other scripts must not import each other.

---

## Mandatory Commands

Before marking any task complete, run ALL applicable checks:

```powershell
# Syntax check all Python scripts
python -m py_compile scripts/study_helper.py
python -m py_compile scripts/code_mapper.py
python -m py_compile scripts/source_validator.py
python -m py_compile scripts/notion_helper.py
python -m py_compile scripts/gdrive_helper.py
python -m py_compile scripts/telegram_helper.py

# End-to-end smoke test (code mapper)
python scripts/code_mapper.py <any_cpp_directory>

# End-to-end smoke test (source validator)
python scripts/source_validator.py "https://cs50.harvard.edu/x/2024/notes/5/"

# Full pipeline smoke test
python scripts/study_helper.py --topic "Test" --course "CS50"
```

For **new skill additions**, additionally:
- Verify the `SKILL.md` has valid YAML frontmatter (`name`, `description` keys)
- Register the slash command in `GEMINI.md` under `## Your skills`

For **config changes** (`context/study_config.yaml`):
- Verify `study_helper.py` loads and parses cleanly with `python -c "import yaml; yaml.safe_load(open('context/study_config.yaml'))"`

A task is NOT done until all applicable commands pass with zero errors.

---

## Architecture Rules

### Scripts Layer

- Each script must have a `main()` function and an `if __name__ == "__main__":` guard.
- CLI arguments are parsed with `argparse`. Every flag must have a `help` string.
- `study_helper.py` is the **only orchestrator**. It calls other modules; other modules never call each other.
- New flags in `study_helper.py` must be gated (e.g., `if args.dork:`). OSINT features must NOT run by default.
- All file paths must be built from `os.path.dirname(os.path.abspath(__file__))` — never hardcode absolute paths.

### Caching Layer

- Cache files live in `study/cache/` (gitignored). Format: JSON. Key pattern: `"<course>:<topic>"`.
- Cache entries must store a `timestamp` (Unix float) alongside results.
- TTL is read from `context/study_config.yaml` `cache_settings.search_ttl_days` — never hardcode TTL values.
- If cache is stale or missing, fetch fresh data. If fetch fails, fall back to printing manual search URLs.

### Config Layer

- `context/study_config.yaml` is the **single source of truth** for dork templates, search engines, and domain reputations.
- Adding a new course's dork templates = add a new key under `dork_templates:` in the YAML. No code change required.
- Adding a new domain reputation = add a new entry under `domain_reputations:` in the YAML. No code change required.

### Skills Layer

- Skills are Markdown instruction files, not code. They tell the agent what to do; scripts do the execution.
- Skill `description:` in YAML frontmatter must be a single sentence covering trigger keywords. Agents use this to decide when to load the skill.
- Never put executable logic in `SKILL.md`. Reference `scripts/` for actual work.

### OSINT / Dorking

- OSINT features are gated behind `--dork` and `--verify` flags in `study_helper.py`. Default run is always clean.
- Between DuckDuckGo queries, apply a 1-second jitter delay to avoid WAF throttling.
- If a search engine returns zero results or throws an exception, fall back to printing manually-clickable URLs. Never crash.
- `source_validator.py` classifies domains as `HIGH` / `MEDIUM` / `LOW`. Only `HIGH` and `MEDIUM` sources pass into study context.

---

## Preferred Libraries

> When adding functionality, reach for these before introducing anything new.

| Need | Use |
|---|---|
| HTTP requests | `urllib.request` (built-in) — no `requests` |
| YAML parsing (scripts with full deps) | `yaml` (`PyYAML`) |
| YAML parsing (lightweight scripts) | Custom line-by-line parser as in `source_validator.py` |
| CLI argument parsing | `argparse` (built-in) |
| JSON read/write | `json` (built-in) |
| File path ops | `os.path` (built-in) |
| Regex | `re` (built-in) |
| Notion API | `scripts/notion_helper.py` — always go through this wrapper |
| Google Drive API | `scripts/gdrive_helper.py` — always go through this wrapper |
| Telegram | `scripts/telegram_helper.py` — always go through this wrapper |

**Never introduce a new `pip` dependency without asking first.** Standard library is always preferred.

---

## Anti-Patterns — Do Not Do These

- [ ] **No hardcoded absolute paths.** Always derive from `os.path.abspath(__file__)`. Windows paths like `C:\Users\...` break on other machines.
- [ ] **No API keys or tokens in code.** Always use `.env` and `os.environ.get()`. The `.env` file is gitignored.
- [ ] **No silent `except` blocks.** Always print a warning or return a structured error. Never swallow exceptions quietly.
- [ ] **No cross-script imports in the wrong direction.** Only `study_helper.py` imports siblings. Other scripts stand alone.
- [ ] **No writing to `context/`.** That folder belongs to `/onboard`. Agent logic writes to `study/` only.
- [ ] **No running OSINT dorks by default.** They are opt-in only (`--dork` flag). Never auto-trigger.
- [ ] **No editing `decisions/log.md` past entries.** It is append-only. Past decisions are immutable.
- [ ] **No deleting files.** Move to `archives/` instead.
- [ ] **No YAML without PyYAML available in `source_validator.py`.** It uses a custom minimal parser intentionally to stay zero-dependency.
- [ ] **No generic `print()` for errors.** Use `print(..., file=sys.stderr)` so errors go to stderr, not stdout.

---

## Git Rules

**Branch strategy:** Feature-branch off `main`. PR to `main`. Direct commits to `main` for small fixes only.

**Branch naming:** `feat/<short-description>` or `fix/<short-description>`

**Commit message format:**
```
type(scope): concise summary (max 72 chars)

[optional body — explain WHY, not WHAT]
```

Types: `feat` | `fix` | `refactor` | `chore` | `docs` | `skill`

**Never:**
- Force-push to `main`
- Commit `.env`, `credentials.json`, `token.json`, or `study/cache/` contents
- Commit `study/temp_context.json`
- Change files unrelated to the current task in a single commit

**Before every push:**
- Run `git status` to verify nothing unintended is staged
- Confirm `.gitignore` covers all secrets and generated outputs

---

## Debugging Workflow

When something is broken, follow this sequence:

1. **Reproduce** — run the exact failing command and capture the full error output
2. **Isolate** — run the sub-script in isolation (`python scripts/source_validator.py <url>`) to narrow the failure
3. **Inspect** — check Python traceback, stderr output, and the contents of `study/temp_context.json` if the pipeline ran
4. **Hypothesize** — form one specific theory (e.g., "cache key mismatch") before changing code
5. **Fix** — make the minimal change that addresses the root cause
6. **Verify** — re-run the smoke test that originally failed; confirm no regressions in other scripts

Do not shotgun-patch. Do not add `try/except` around entire functions to hide errors.

---

## Security Rules

- Never store API keys in code — use `.env` with `os.environ.get("KEY_NAME")`
- Never log personal data from `context/about-me.md` or `context/about-business.md` to stdout
- When running OSINT dorks, never auto-submit queries to services without user-initiated `--dork` flag
- `credentials.json` and `token.json` (Google OAuth) are gitignored — never stage them
- URL inputs to `source_validator.py` must be validated with `urllib.parse.urlparse` before making any HTTP requests

---

## Definition of Done

A task is complete ONLY when ALL of the following are true:

- [ ] Functionality works as specified
- [ ] All affected Python scripts pass `python -m py_compile`
- [ ] Smoke tests pass (see Mandatory Commands above)
- [ ] No hardcoded absolute paths introduced
- [ ] No new `pip` dependencies introduced without approval
- [ ] No `.env`, `credentials.json`, `token.json`, or cache files staged
- [ ] If a new slash command was added: registered in `GEMINI.md`
- [ ] If a new config key was added: `study_config.yaml` updated
- [ ] If a decision was made: appended to `decisions/log.md`
- [ ] No unrelated files changed in the same commit
- [ ] `git status` is clean (or only contains expected gitignored files)

---

## Self-Correction Memory

When corrected, the agent must:

1. Record what was wrong
2. Check if the same mistake exists elsewhere in the current change
3. Apply the correction consistently across the entire codebase

Known corrections for this project:
- **PowerShell uses `;` not `&&` as statement separator.** Always chain commands with `;` in PowerShell.
- **`YouTubeTranscriptApi().fetch()` (not `.get_transcript()`).** The newer API version requires instantiation then `.fetch()`.
- **DuckDuckGo HTML scraping often triggers anomaly pages.** Always wrap in try/except and fall back to clickable URL printing.
- **`source_validator.py` must NOT import `yaml`.** It uses a custom minimal parser deliberately — do not refactor this.

---

## Communication Style

- Be direct and concise. One sentence of context, then the action.
- Lead with what needs action, not status updates.
- When asked a question, answer it first. Do not restate the question.
- Flag uncertainty early. State the assumption and proceed, do not wait.
- When a decision is made, surface it for `decisions/log.md`.
- When a manual task is spotted repeating 3+ times, flag it at the next `/level-up`.
- Default shift: ask "to what extent could AI be leveraged here?" before assuming Parth will do it the old way.

---

*Think like an owner of this codebase, not a temporary contributor.*
