#!/usr/bin/env python3
"""
checklist_generator.py — Generate and sync study assignment checklists.

Usage:
  python scripts/checklist_generator.py \\
      --topic "Memory Pointers" \\
      --course "CS50" \\
      --items "Write a swap function using pointers,Implement a dynamic array with malloc,Draw a pointer diagram for a linked node" \\
      [--drive-sync]

Output:
  study/<course>/<topic-dashed>-checklist.md
  (optionally synced to Google Drive AIOS/Study/<course>/)
"""
import os
import sys
import argparse
import re
from datetime import date


def slugify(text):
    """Convert a topic name to a lowercase-dashed filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


def generate_checklist(topic, course, items):
    """
    Build a Markdown checklist document.

    Args:
        topic  : human-readable topic name
        course : course name (e.g. "CS50")
        items  : list of assignment task strings

    Returns:
        str — full Markdown content
    """
    today = date.today().strftime("%Y-%m-%d")
    lines = [
        f"# {topic} — Assignment Checklist",
        f"> Course: **{course}** | Generated: {today}",
        "",
        "---",
        "",
        "## ✅ Practice Tasks",
        "",
    ]

    for item in items:
        item = item.strip()
        if item:
            lines.append(f"- [ ] {item}")

    lines += [
        "",
        "---",
        "",
        "## 📝 Notes",
        "",
        "> Add your observations here after completing each task.",
        "",
    ]

    return "\n".join(lines) + "\n"


def save_checklist(content, course, topic_slug, workspace_root):
    """Write checklist to study/<course>/<topic-slug>-checklist.md and return the path."""
    out_dir = os.path.join(workspace_root, "study", course)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{topic_slug}-checklist.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Markdown assignment checklist and optionally sync to Google Drive."
    )
    parser.add_argument("--topic", required=True, help="Topic name (e.g. 'Memory Pointers')")
    parser.add_argument("--course", required=True, help="Course name (e.g. 'CS50')")
    parser.add_argument(
        "--items",
        required=True,
        help="Comma-separated list of practice task descriptions",
    )
    parser.add_argument(
        "--drive-sync",
        action="store_true",
        help="Upload the generated checklist to Google Drive after saving",
    )
    args = parser.parse_args()

    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topic_slug = slugify(args.topic)
    items = [i.strip() for i in args.items.split(",") if i.strip()]

    # Ensure console can handle output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if not items:
        print("Error: --items cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Generate and save
    content = generate_checklist(args.topic, args.course, items)
    out_path = save_checklist(content, args.course, topic_slug, workspace_root)
    print(f"Checklist saved -> {out_path}")

    # Optional Drive sync
    if args.drive_sync:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gdrive_helper import sync_study_artifacts
        sync_study_artifacts(args.course, args.topic, [out_path])

    return out_path


if __name__ == "__main__":
    main()
