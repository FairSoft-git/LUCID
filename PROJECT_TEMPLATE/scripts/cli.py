#!/usr/bin/env python3
"""cli.py - Master CLI for [Project Name].

This script provides command-line access to all project features.

Usage:
    python scripts/cli.py -C              # Spellcheck: Check spelling
    python scripts/cli.py -D              # Docs: Serve documentation locally
    python scripts/cli.py -G              # Git: Git operations
    python scripts/cli.py --help          # Show all options

Feature Flags:
    -C, --check      Spellcheck (--fix for interactive mode)
    -D, --docs       Serve documentation locally
    -G, --git        Git operations (--commit MSG, --push)

Examples:
    python scripts/cli.py -C --fix         # Interactive spellcheck
    python scripts/cli.py -D               # Serve docs at http://localhost:8000
    python scripts/cli.py -G --commit "feat: new feature" --body "Details"
    python scripts/cli.py -G --push        # Push to remote
"""
import argparse
import sys
import subprocess
import re
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "features"))

# Configuration
PROJECT_CODE = "PROJ"  # TODO: Change this to your project code


def cmd_spellcheck(args):
    """Handle spellcheck commands."""
    cmd = [sys.executable, str(ROOT / "scripts" / "spellcheck.py")]

    if args.fix:
        cmd.append("--fix")

    try:
        subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode


def get_next_commit_number():
    """Scan git log for PROJECT.NNNN pattern and return next number."""
    try:
        # Get last 100 commit subjects
        output = subprocess.check_output(
            ["git", "log", "-n", "100", "--pretty=format:%s"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return 1  # No commits yet

    max_num = 0
    pattern = re.compile(rf"{PROJECT_CODE}\.(\d+):")

    for line in output.splitlines():
        match = pattern.match(line)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    return max_num + 1


def cmd_git(args):
    """Handle git operations."""
    if args.commit:
        print(f"=== Mock Push (Commit) ===")

        # 1. Calculate next number
        next_num = get_next_commit_number()
        prefix = f"{PROJECT_CODE}.{next_num:04d}"

        # 2. Construct Header
        header = f"{prefix}: {args.commit}"

        # 3. Validate Header Width
        if len(header) > 80:
            print(f"❌ Error: Commit subject too long ({len(header)} > 80 chars).")
            print(f"Header: {header}")
            return 1

        # 4. Validate Body
        full_msg = header
        if args.body:
            if len(args.body) > 200:
                print(f"❌ Error: Commit body too long ({len(args.body)} > 200 chars).")
                return 1
            full_msg = f"{header}\n\n{args.body}"

        print(f"Commit Message:\n{'-'*40}\n{full_msg}\n{'-'*40}")

        try:
            # Stage all changes
            print("Staging files...")
            subprocess.run(["git", "add", "."], check=True)

            # Commit (triggers pre-commit hooks)
            print("Committing (running pre-commit hooks)...")
            subprocess.run(["git", "commit", "-m", full_msg], check=True)
            print("✓ Commit successful. Ready to push.")
            return 0
        except subprocess.CalledProcessError as e:
            print("❌ Commit failed. Fix errors and try again.")
            return e.returncode

    if args.push:
        print(f"=== Push ===")
        try:
            # Check if there are unpushed commits
            status = subprocess.run(
                ["git", "status", "-sb"], capture_output=True, text=True, check=True
            ).stdout

            if "ahead" not in status:
                print("Nothing to push.")
                return 0

            print("Pushing to origin...")
            subprocess.run(["git", "push"], check=True)
            print("✓ Push successful.")
            return 0
        except subprocess.CalledProcessError as e:
            print("❌ Push failed.")
            return e.returncode

    print("Please specify --commit 'msg' or --push")
    return 1


def cmd_docs(args):
    """Serve documentation locally using grip (GitHub style) or http.server."""
    import webbrowser

    PORT = 8000
    DIRECTORY = str(ROOT)

    try:
        from grip import serve

        print(f"Starting Grip (GitHub-style) server at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")

        # Grip serves the directory and renders README.md by default
        # It handles relative links by rendering them as well
        serve(path=DIRECTORY, port=PORT, browser=True)
        return 0

    except ImportError:
        print("⚠️  'grip' not installed. Falling back to simple file server.")
        print("   To get GitHub-style rendering, run: pip install grip")

        import http.server
        import socketserver

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)

        print(f"Serving raw files at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")

        # Open browser to docs/README.md
        url = f"http://localhost:{PORT}/docs/README.md"
        webbrowser.open(url)

        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            return 0
        except OSError as e:
            print(f"Error starting server: {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(description="Project Master CLI")

    # Feature groups
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-C", "--check", action="store_true", help="Spellcheck")
    group.add_argument("-D", "--docs", action="store_true", help="Serve documentation locally")
    group.add_argument("-G", "--git", action="store_true", help="Git operations")

    # Spellcheck args
    parser.add_argument("--fix", action="store_true", help="Interactive fix mode")

    # Git args
    parser.add_argument("--commit", type=str, help="Commit title (Mock Push)")
    parser.add_argument("--body", type=str, help="Commit body (max 200 chars)")
    parser.add_argument("--push", action="store_true", help="Push to remote")

    args = parser.parse_args()

    if args.check:
        sys.exit(cmd_spellcheck(args))
    elif args.docs:
        sys.exit(cmd_docs(args))
    elif args.git:
        sys.exit(cmd_git(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
