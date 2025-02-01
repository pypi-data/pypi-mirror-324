"""Changelog generation module."""

import subprocess
from datetime import datetime
from typing import List, Dict
import openai
import os


def get_git_commits(since_tag: str = None) -> List[str]:
    """Get git commits since the last tag."""
    cmd = ["git", "log", "--pretty=format:%s"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.splitlines()


def generate_changelog() -> str:
    """Generate a changelog from git history using AI."""
    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Get commits
    commits = get_git_commits()
    if not commits:
        return "No changes found"

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Generate changelog using AI
    prompt = f"""Generate a changelog from these git commits:

{commits}

Format the output as follows:
## Changes
- Feature changes
- Bug fixes
- Documentation updates
- Other changes

Use clear, concise language and group similar changes together."""

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates changelogs from git commits."},
            {"role": "user", "content": prompt}
        ]
    )

    changelog = response.choices[0].message.content

    # Write to CHANGELOG.md
    with open("CHANGELOG.md", "a") as f:
        f.write(f"\n\n## {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(changelog)

    return changelog 