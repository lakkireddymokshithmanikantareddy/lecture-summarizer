"""
deploy_to_github.py — Helper script to push this project to a new GitHub repo.

Usage:
    python deploy_to_github.py

Environment variables (optional — will prompt if missing):
    GITHUB_USERNAME   Your GitHub username
    GITHUB_PAT        A GitHub Personal Access Token with 'repo' scope
"""

import os
import subprocess
import sys

REPO_NAME = "lecture-summarizer"
COMMIT_MSG = "Initial commit: Lecture Summarizer v1.0"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str], check: bool = True, **kwargs) -> subprocess.CompletedProcess:
    """Run a shell command and print it first."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False, text=True, capture_output=True, **kwargs)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def prompt_env(var_name: str, prompt_text: str, secret: bool = False) -> str:
    """Return env var or prompt user for it."""
    value = os.environ.get(var_name, "").strip()
    if value:
        return value
    try:
        if secret:
            import getpass
            value = getpass.getpass(f"{prompt_text}: ").strip()
        else:
            value = input(f"{prompt_text}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)
    if not value:
        print(f"Error: {var_name} cannot be empty.")
        sys.exit(1)
    return value


# ---------------------------------------------------------------------------
# GitHub API
# ---------------------------------------------------------------------------

def create_github_repo(username: str, pat: str) -> str:
    """
    Create a new public GitHub repository via the REST API.
    Returns the clone URL.
    Handles 'already exists' gracefully.
    """
    try:
        import urllib.request
        import json as _json
    except ImportError:
        print("Standard library modules unavailable — this should never happen.")
        sys.exit(1)

    payload = _json.dumps({
        "name": REPO_NAME,
        "description": "AI-powered lecture notes summarizer using Google Gemini",
        "private": False,
        "auto_init": False,
    }).encode()

    req = urllib.request.Request(
        "https://api.github.com/user/repos",
        data=payload,
        headers={
            "Authorization": f"token {pat}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = _json.loads(resp.read())
            clone_url = data["clone_url"]
            print(f"✅ Repository created: {clone_url}")
            return clone_url
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        data = {}
        try:
            data = _json.loads(body)
        except Exception:
            pass

        if exc.code == 422 and "already exists" in body:
            clone_url = f"https://github.com/{username}/{REPO_NAME}.git"
            print(f"⚠️  Repository already exists — using existing: {clone_url}")
            return clone_url
        elif exc.code in (401, 403):
            print(f"❌ Authentication failure (HTTP {exc.code}). Check your GITHUB_PAT has 'repo' scope.")
            sys.exit(1)
        else:
            print(f"❌ GitHub API error {exc.code}: {data.get('message', body)}")
            sys.exit(1)


# ---------------------------------------------------------------------------
# Git operations
# ---------------------------------------------------------------------------

def git_setup(username: str, pat: str, clone_url: str) -> None:
    """Init git repo, commit, and push to GitHub."""
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Inject credentials into URL (HTTPS)
    auth_url = clone_url.replace(
        "https://",
        f"https://{username}:{pat}@",
    )

    print("\n📦 Initialising git repository…")
    run(["git", "init"], cwd=project_dir)
    run(["git", "checkout", "-b", "main"], cwd=project_dir, check=False)
    run(["git", "add", "."], cwd=project_dir)
    run(["git", "commit", "-m", COMMIT_MSG], cwd=project_dir)

    print("\n🚀 Pushing to GitHub…")
    # Remove existing remote if present
    run(["git", "remote", "remove", "origin"], cwd=project_dir, check=False)
    run(["git", "remote", "add", "origin", auth_url], cwd=project_dir)
    run(["git", "push", "-u", "origin", "main"], cwd=project_dir)

    print(f"\n🎉 Done! Your repo is live at:\n   https://github.com/{username}/{REPO_NAME}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Lecture Summarizer — GitHub Deploy Helper")
    print("=" * 60)
    print()

    username = prompt_env("GITHUB_USERNAME", "GitHub username")
    pat = prompt_env("GITHUB_PAT", "GitHub Personal Access Token", secret=True)

    print(f"\n📡 Creating repo '{REPO_NAME}' under @{username}…")
    clone_url = create_github_repo(username, pat)

    git_setup(username, pat, clone_url)


if __name__ == "__main__":
    main()
