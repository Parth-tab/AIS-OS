---
name: generating-study-guides
description: >
  Generates structured study sheets, runnable reference code files, and class dependency maps
  from consolidated sources (YouTube, Local Context, NotebookLM MCP, and Academic Dorks).
  Triggers on: study, study sheet, lecture notes, study guide, C/C++ OOP learning,
  CS50 homework, study-dork, study-map, study-verify, study-timeline.
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# Generating Study Guides & Reference Code

Use this skill when the user wants to generate structured notes, explanations, assignments, class inheritance diagrams, or verified academic sources for a computer science or programming topic.

---

## 1. Core Workflow

- [ ] **1. Run Python Gatherer**: Execute `python scripts/study_helper.py` with your targeted parameters:
  ```bash
  python scripts/study_helper.py --topic "[Topic Name]" --course "[Course]" --dork --map-dir "[Local Code Path]"
  ```
- [ ] **2. Read gathered context**: Load `study/temp_context.json`.
- [ ] **3. Query NotebookLM (Optional)**: If NotebookLM is running, query the notebook associated with the course for extra lecture details.
- [ ] **4. Synthesize 8-Point Study Sheet**: Write a Markdown guide to `study/<course>/<topic_dashed>.md` containing the concepts and Mermaid mapping data.
- [ ] **5. Generate Runnable Code**: Write a fully-commented example code file to `study/<course>/<topic_dashed>.<ext>`.
- [ ] **6. Add Notion Task**: Invoke `python scripts/notion_helper.py` to add a practice task card to the user's Notion task list:
  ```bash
  python scripts/notion_helper.py add "Practice: [Topic]" "Not started"
  ```
- [ ] **7. Generate Checklist & Sync to Google Drive**: Create the assignment checklist and upload all three artifacts:
  ```bash
  # Generate checklist and sync it
  python scripts/checklist_generator.py \
      --topic "[Topic Name]" \
      --course "[Course]" \
      --items "[Task 1],[Task 2],[Task 3]" \
      --drive-sync

  # Sync study sheet + code file to Drive
  python scripts/gdrive_helper.py sync \
      --course "[Course]" \
      --topic "[Topic Name]" \
      --files "study/[Course]/[topic-dashed].md,study/[Course]/[topic-dashed].[ext]"
  ```
  Files are uploaded to `My Drive/AIOS/Study/[Course]/`. Re-runs update existing files — no duplicates.

---

## 2. Integrated OSINT & Verification Features

### A. Academic Dorking (`--dork`)
When `--dork` is enabled, the gatherer queries Bing/DuckDuckGo using configurations in `context/study_config.yaml`:
*   **Harvard CS50**: Targets lecture slides, official notes pages, and Code50 repositories.
*   **General Topics**: Targets university PDF guides (`filetype:pdf site:edu`), wiki pages, and C++ git repositories.
*   **Interactive Fallback**: If network lookups are blocked by search engine anti-bot pages (WAF), the script outputs clickable dork search URLs. Open these in a standard browser and copy-paste key links.

### B. Source Validation (`scripts/source_validator.py`)
Checks URLs to verify:
1.  **Accessibility**: Confirm HTTP status `200 OK`.
2.  **Reputation**: Assesses domain confidence level (`HIGH` for universities/Wikis, `MEDIUM` for tech portals like GeeksforGeeks, `LOW` for standard personal blogs).
3.  **Archive Check**: Locates Wayback Machine backups to ensure page persistence.

### C. OOP Codebase Mapper (`--map-dir`)
Scans folders for C/C++ classes:
*   Parses `#include` structures and inheritance lines (e.g. `class Dog : public Animal`).
*   Outputs standard Mermaid code class diagrams to embed in the generated study sheets.

---

## 3. Study Guide Output Specification

### 1. 8-Point Study Sheet Structure
Save to `study/<course>/<topic_dashed>.md`. Include:
1.  **Explanation**: Plain-English explanation of the topic.
2.  **Significance**: Why this concept is critical in computer science.
3.  **Types/Variants**: Classifications or forms of this topic.
4.  **Implementation Guide**: Syntactic blueprint and standard usage.
5.  **Mermaid Class Diagram**: If `--map-dir` was run, insert the generated class inheritance map.
6.  **Real-world Illustration**: Clear metaphor or example mapping the concept to a real scenario.
7.  **Short Assignment**: 2-3 practice exercises to write by hand.
8.  **Core Nature**: Mechanical low-level breakdown (e.g. how it behaves in memory/stack/heap).

### 2. Code Example Generation
Save a clean, standalone, runnable source file to `study/<course>/<topic_dashed>.<ext>` containing:
- Complete implementation of the topic.
- In-line comments explaining line-by-line mechanical execution.
- A main function demonstrating correct execution.

---

## 4. Configuration Rules

All search settings and reputations are externalized in `context/study_config.yaml`:
```yaml
domain_reputations:
  harvard.edu: "HIGH"
  wikipedia.org: "HIGH"
  geeksforgeeks.org: "MEDIUM"
```
Do not hardcode query string arrays or domain weights in python files.

---

## 5. Google Drive Sync

Study artifacts are automatically synced to `My Drive/AIOS/Study/<course>/` after each session.

### Drive Folder Structure
```
My Drive/
└── AIOS/
    └── Study/
        ├── CS50/
        │   ├── <topic-dashed>.md          ← Study sheet
        │   ├── <topic-dashed>.<ext>       ← Reference code
        │   └── <topic-dashed>-checklist.md ← Assignment checklist
        └── ...other courses
```

### Commands

| Command | Purpose |
|---|---|
| `gdrive_helper.py sync --course X --topic Y --files a,b` | Upload/update specific files |
| `checklist_generator.py --topic X --course Y --items "..." --drive-sync` | Generate checklist + sync |
| `study_helper.py ... --drive-sync` | Sync already-generated topic files |

### Re-auth Note
If Drive sync throws a scope error, delete `token.json` and re-run — a browser login will appear once to approve the `drive.file` permission.

---

## Attribution
Adapted from The Three Ms of AI™ © 2026 Nate Herk.
