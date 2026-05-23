---
name: generating-study-guides
description: >
  Generates structured study sheets and runnable reference code files from consolidated sources.
  Use when the user mentions: study, study sheet, lecture notes, study guide, C/C++ OOP learning,
  or CS50 homework generation. Integrates YouTube, Local Context, NotebookLM MCP, and Notion.
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# Generating Study Guides & Reference Code

Use this skill when the user wants to generate structured notes, explanations, and assignments for a CS/programming topic.

## Workflow

- [ ] **1. Run Python Gatherer**: Execute `python scripts/study_helper.py` with target parameters.
- [ ] **2. Read gathered context**: Load `study/temp_context.json`.
- [ ] **3. Query NotebookLM (Optional)**: If NotebookLM is running, query the notebook associated with the course for extra lecture details.
- [ ] **4. Synthesize 8-Point Study Sheet**: Write a Markdown guide to `study/<course>/<topic_dashed>.md`.
- [ ] **5. Generate Runnable Code**: Write a fully-commented example code file to `study/<course>/<topic_dashed>.<ext>`.
- [ ] **6. Add Notion Task**: Invoke `python scripts/notion_helper.py` to add a practice task card to the user's Notion task list.

## Instructions

### 1. 8-Point Study Sheet Structure
Save to `study/<course>/<topic_dashed>.md`. Include:
1. **Explanation**: Plain-English explanation of the topic.
2. **Significance**: Why this concept is critical in CS.
3. **Types/Variants**: Different forms or classifications of this topic.
4. **Implementation Guide**: Syntactic blueprint and standard usage.
5. **Real-world Illustration**: Clear example mapping the concept to a real scenario.
6. **Short Assignment**: 2-3 practice exercises to write by hand.
7. **Core Nature**: Mechanical low-level breakdown (e.g. how it behaves in memory).
8. **Checklist**: Checkboxes of sub-topics mastered vs. sub-topics needing study.

### 2. Code Example Generation
Save a clean, standalone, runnable source file to `study/<course>/<topic_dashed>.<ext>` containing:
- Complete implementation of the topic.
- In-line comments explaining line-by-line mechanical execution.
- A main function demonstrating correct execution.

### 3. Notion Task Scaffolding
Run this command to create a Notion tracker card for practice:
```bash
python scripts/notion_helper.py add "Practice: [Topic Name]" "Not started"
```

## Attribution
Adapted from The Three Ms of AI™ © 2026 Nate Herk.
