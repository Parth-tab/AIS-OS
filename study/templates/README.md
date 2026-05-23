# study/templates/

Standardized Markdown and code skeletons for the `/study` skill.

The agent reads the relevant template first, then fills in the placeholders
(`{{TOKEN}}`) with topic-specific content. This avoids regenerating structure
on every run, saving tokens and keeping output consistent.

---

## Files

| File | Purpose | Used By |
|---|---|---|
| `study-sheet.md` | 8-point study guide skeleton | `generating-study-guides` step 4 |
| `checklist.md` | Assignment + concept-check skeleton | `generating-study-guides` step 7 |
| `reference-code.c` | Annotated C/C++ code skeleton | `generating-study-guides` step 5 |

---

## Placeholder convention

All placeholders follow the pattern `{{UPPER_SNAKE_CASE}}`.
Replace every `{{TOKEN}}` before saving the output file to `study/<course>/`.

### Universal tokens (all templates)

| Token | Replace with |
|---|---|
| `{{TOPIC}}` | Topic name (e.g., `Memory Pointers`) |
| `{{COURSE}}` | Course slug (e.g., `CS50`) |
| `{{DATE}}` | ISO date string (e.g., `2026-05-23`) |
| `{{SOURCE_LABEL}}` | Short description of primary source used |

### study-sheet.md tokens

| Token | Replace with |
|---|---|
| `{{EXPLANATION}}` | 3-6 sentence plain-English explanation |
| `{{SIGNIFICANCE}}` | Bullet list of why the topic matters |
| `{{TYPES_VARIANTS}}` | Bulleted list of subtypes/forms |
| `{{LANG}}` | Code fence language tag (`c`, `cpp`, `py`, etc.) |
| `{{IMPLEMENTATION_CODE}}` | Minimal working code block |
| `{{DIAGRAM_SECTION_TITLE}}` | `Mermaid Class Diagram` OR `Memory Layout` |
| `{{DIAGRAM_OR_LAYOUT}}` | Mermaid block, ASCII table, or `_N/A — skipped_` |
| `{{REAL_WORLD_ILLUSTRATION}}` | One clear metaphor, 4-6 sentences |
| `{{ASSIGNMENTS}}` | Numbered list of 2-3 practice exercises |
| `{{CORE_NATURE}}` | Low-level mechanics (memory/stack/heap) |

### checklist.md tokens

| Token | Replace with |
|---|---|
| `{{TASK_N}}` | Concrete practice task (verb phrase) |
| `{{CONCEPT_CHECK_N}}` | True/False or short-answer prompt |
| `{{RESOURCE_N}}` | URL or title of reference material |

### reference-code.c tokens

| Token | Replace with |
|---|---|
| `{{PURPOSE_SUMMARY}}` | One-sentence description of what the file demonstrates |
| `{{COMPILE_CMD}}` | Compiler command (e.g., `gcc topic.c -o topic`) |
| `{{RUN_CMD}}` | Run command (e.g., `./topic`) |
| `{{INCLUDES}}` | Required `#include` directives |
| `{{TYPEDEFS_AND_CONSTANTS}}` | Type defs, enums, `#define` constants |
| `{{HELPER_FUNCTIONS}}` | Supporting function implementations |
| `{{STEP_N_LABEL}}` | Short label for each main() demonstration step |
| `{{STEP_N_CODE}}` | Code for that step |

---

## Rules

- **Never edit template files directly** for topic-specific content.
  Copy → fill → save to `study/<course>/`.
- If a section is genuinely not applicable, replace its token with `_N/A_`.
- Keep templates in sync with the 8-point spec in
  `.antigravity/skills/generating-study-guides/SKILL.md` section 3.
