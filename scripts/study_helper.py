#!/usr/bin/env python3
import os
import sys
import json
import re
import argparse

def extract_youtube_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_youtube_transcript(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join([t.text for t in transcript])
    except ImportError:
        return "[Error: 'youtube-transcript-api' package is not installed.]"
    except Exception as e:
        return f"[Error fetching transcript: {str(e)}]"

def load_local_context(course, topic):
    # Look in context/courses/<course>.md or context/courses/<course>_<topic>.md
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_paths = [
        os.path.join(workspace_root, 'context', 'courses', f"{course.lower()}.md"),
        os.path.join(workspace_root, 'context', 'courses', f"{course.lower()}_{topic.lower().replace(' ', '_')}.md")
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    return ""

def prompt_for_clipboard():
    print("\n--- Clipboard / Console Prompt Fallback ---")
    print("Paste any additional lecture notes, slide text, or code examples below.")
    print("When finished, press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to save:\n")
    try:
        lines = sys.stdin.read()
        return lines.strip()
    except Exception as e:
        return f"[Error reading console: {str(e)}]"

def main():
    parser = argparse.ArgumentParser(description="Gather context for AIOS study generator.")
    parser.add_argument("--topic", required=True, help="Topic name")
    parser.add_argument("--course", required=True, help="Course name")
    parser.add_argument("--youtube", help="Optional YouTube URL")
    parser.add_argument("--interactive", action="store_true", help="Prompt for manual paste")
    args = parser.parse_args()

    context_data = {
        "topic": args.topic,
        "course": args.course,
        "youtube_url": args.youtube or "",
        "youtube_transcript": "",
        "local_context": "",
        "interactive_context": ""
    }

    # 1. Fetch YouTube Transcript
    if args.youtube:
        video_id = extract_youtube_id(args.youtube)
        if video_id:
            print(f"Fetching transcript for YouTube video ID: {video_id}...")
            context_data["youtube_transcript"] = fetch_youtube_transcript(video_id)
        else:
            print("Warning: Invalid YouTube URL format.")

    # 2. Fetch Local Context
    local_txt = load_local_context(args.course, args.topic)
    if local_txt:
        print(f"Found local context file for course '{args.course}'.")
        context_data["local_context"] = local_txt

    # 3. Interactive console fallback
    if args.interactive:
        context_data["interactive_context"] = prompt_for_clipboard()

    # 4. Save consolidated output
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(workspace_root, 'study')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'temp_context.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(context_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConsolidated context successfully written to: {output_path}")

if __name__ == "__main__":
    main()
