#!/usr/bin/env python3
"""
create_post.py

Usage:
  python create_post.py             # creates today's post (YYYY-MM-DD)
  python create_post.py --date 2025-11-16
  python create_post.py --commit    # also runs: git add . && git commit -m "chore: add YYYY-MM-DD" && git push

Notes:
- Make sure git remote and credentials are set up if you use --commit.
- Works on Windows, macOS, Linux (Python 3.7+).
"""
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import sys

TEMPLATE = """# Daily log — {date}

**Date:** {date}  
**Topic / Concept:** {topic}  
**What I learned (1–3 lines):** {learned}  
**Problem I solved / experiment I ran:** {experiment}  
**Command / Code snippet (if any):** `{cmd}`  
**One mistake I made:** {mistake}  
**Links / References:** {links}  
**Tomorrow's plan:** {tomorrow}
"""

def run_cmd(cmd_list):
    try:
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd_list)}\n{e}", file=sys.stderr)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", "-d", help="Date for the post (YYYY-MM-DD). Default: today")
    p.add_argument("--commit", "-c", action="store_true", help="Also git add/commit/push the new file")
    p.add_argument("--open", "-o", action="store_true", help="Open the created file in default editor (where supported)")
    args = p.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: date must be in YYYY-MM-DD format", file=sys.stderr)
        sys.exit(1)

    repo_root = Path(__file__).parent.resolve()
    posts_dir = repo_root / "posts"
    posts_dir.mkdir(exist_ok=True)

    filename = posts_dir / f"{date_str}.md"
    if filename.exists():
        print(f"File already exists: {filename}")
    else:
        # Basic placeholder values you can edit later
        content = TEMPLATE.format(
            date=date_str,
            topic="(add topic here)",
            learned="(write 1-3 lines)",
            experiment="(describe the short experiment or problem solved)",
            cmd="(any shell/solidity snippet)",
            mistake="(one mistake learned from)",
            links="(links if any)",
            tomorrow="(tomorrow's plan)"
        )
        filename.write_text(content, encoding="utf-8")
        print(f"Created: {filename}")

    if args.commit:
        # Stage the file and commit
        commit_msg = f"chore: add {date_str} daily post"
        run_cmd(["git", "add", str(filename)])
        run_cmd(["git", "commit", "-m", commit_msg])
        # Try push (may prompt for credentials depending on your setup)
        run_cmd(["git", "push"])
        print("Committed and pushed (if git remote is configured).")

    if args.open:
        # Try to open the file in default editor/viewer
        try:
            if sys.platform.startswith("darwin"):
                run_cmd(["open", str(filename)])
            elif sys.platform.startswith("win"):
                run_cmd(["start", str(filename)],)  # may require shell
            else:
                run_cmd(["xdg-open", str(filename)])
        except Exception as e:
            print("Could not open file automatically:", e)

if __name__ == "__main__":
    main()
