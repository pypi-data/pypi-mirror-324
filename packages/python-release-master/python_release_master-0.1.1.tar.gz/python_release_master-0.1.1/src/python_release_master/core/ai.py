"""AI integration for changelog generation."""

import json
import os
import subprocess
from datetime import datetime
from typing import List, Optional, Dict, Any

from openai import OpenAI
from rich.console import Console

console = Console()


def get_uncommitted_changes() -> List[str]:
    """Get all uncommitted changes."""
    try:
        # Get staged changes
        staged = subprocess.run(
            ["git", "diff", "--staged", "--name-status"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        
        # Get unstaged changes
        unstaged = subprocess.run(
            ["git", "diff", "--name-status"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        
        # Get untracked files
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        
        changes = []
        if staged:
            changes.extend(f"[Staged] {change}" for change in staged)
        if unstaged:
            changes.extend(f"[Unstaged] {change}" for change in unstaged)
        if untracked:
            changes.extend(f"[Untracked] {file}" for file in untracked)
        
        return changes
    except subprocess.CalledProcessError:
        return []


def commit_changes_with_ai() -> Optional[str]:
    """Generate commit message and commit changes using AI."""
    changes = get_uncommitted_changes()
    if not changes:
        return None
    
    client = OpenAI()
    
    # Generate commit message
    prompt = f"""Based on the following changes, generate a commit message that follows conventional commits format.
The changes are:

{chr(10).join(changes)}

Return a JSON object with the following structure:
{{
    "type": "feat|fix|docs|style|refactor|test|chore",
    "scope": "optional scope in parentheses",
    "description": "concise description",
    "body": "optional detailed description",
    "breaking": boolean
}}"""

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates conventional commit messages based on code changes.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    commit_data = json.loads(response.choices[0].message.content)
    
    # Format commit message
    commit_msg = f"{commit_data['type']}"
    if commit_data.get("scope") and commit_data["scope"] is not None:
        commit_msg += f"({commit_data['scope']})"
    if commit_data.get("breaking"):
        commit_msg += "!"
    commit_msg += f": {commit_data['description']}"
    if commit_data.get("body"):
        commit_msg += f"\n\n{commit_data['body']}"
    
    # Stage and commit changes
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        return commit_msg
    except subprocess.CalledProcessError:
        return None


def get_commits_since_last_tag() -> List[str]:
    """Get all commit messages since the last tag."""
    try:
        # Get the last tag
        last_tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        # No tags found, get all commits
        last_tag = None

    # Get commits
    cmd = ["git", "log", "--pretty=format:%h %s"]
    if last_tag:
        cmd.append(f"{last_tag}..HEAD")

    commits = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    return commits


def get_pull_requests_since_last_tag() -> List[dict]:
    """Get all merged pull requests since the last tag."""
    try:
        # Get the last tag's date
        last_tag_date = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        last_tag_date = subprocess.run(
            ["git", "log", "-1", "--format=%ai", last_tag_date],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        last_tag_date = datetime.strptime(last_tag_date, "%Y-%m-%d %H:%M:%S %z")
    except subprocess.CalledProcessError:
        # No tags found, use all PRs
        last_tag_date = None

    # Get merged PRs
    cmd = ["gh", "pr", "list", "--state", "merged", "--json", "title,body,number,mergedAt"]
    if last_tag_date:
        cmd.extend(["--search", f"merged:>={last_tag_date.strftime('%Y-%m-%d')}"])

    try:
        prs = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return prs if not prs else json.loads(prs)
    except subprocess.CalledProcessError:
        console.print("[yellow]GitHub CLI not available, skipping PR analysis[/yellow]")
        return []


def generate_changelog_with_ai(sections: List[str], model: str = "gpt-4-0125-preview") -> Dict[str, Any]:
    """Generate a changelog using OpenAI with structured output."""
    # Handle uncommitted changes first
    commit_msg = commit_changes_with_ai()
    if commit_msg:
        console.print(f"[green]Committed changes: {commit_msg}[/green]")

    client = OpenAI()

    # Get commits and PRs
    commits = get_commits_since_last_tag()
    prs = get_pull_requests_since_last_tag()

    # Prepare context
    context = "Here are the changes since the last release:\n\n"
    if commits:
        context += "Commits:\n" + "\n".join(f"- {c}" for c in commits) + "\n\n"
    if prs:
        context += "Pull Requests:\n" + "\n".join(
            f"- #{pr['number']}: {pr['title']}\n  {pr['body']}" for pr in prs
        )

    # Generate changelog
    prompt = f"""Based on the following changes, analyze the changes and return a structured changelog.
Available sections are: {', '.join(sections)}.

{context}

Return a JSON object with the following structure:
{{
    "version_bump": "major|minor|patch",
    "bump_reason": "explanation of why this bump type was chosen",
    "changes": [
        {{
            "title": "commit/PR title",
            "description": "detailed description",
            "section": "one of the available sections",
            "type": "feat|fix|docs|style|refactor|test|chore",
            "breaking": boolean
        }}
    ],
    "changelog_md": "final markdown formatted changelog with sections"
}}"""

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes code changes and generates clear, structured changelogs.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return json.loads(response.choices[0].message.content)