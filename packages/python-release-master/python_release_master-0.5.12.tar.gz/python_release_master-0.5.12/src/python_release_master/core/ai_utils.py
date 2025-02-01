"""AI utility functions for Python Release Master."""

import json
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
import httpx
from openai import OpenAI
from pydantic import BaseModel
from rich.console import Console

# IMPORTANT: We use OpenAI's parse method for structured outputs as it provides:
# 1. Type safety and validation through response_format
# 2. Guaranteed schema compliance
# 3. Better reliability and consistency in outputs
# 4. Built-in error handling for malformed responses
# 5. Future compatibility with OpenAI's structured output features
#
# DO NOT replace this with regular chat completions as it would:
# - Remove type safety
# - Make outputs less reliable
# - Require complex JSON parsing and error handling
# - Break forward compatibility with OpenAI's features

console = Console()

def get_openai_client() -> OpenAI:
    """Get OpenAI client instance.
    
    Returns:
        OpenAI client instance
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Create httpx client with default settings
    http_client = httpx.Client(
        timeout=60.0,
        follow_redirects=True
    )
    
    # Create OpenAI client with custom httpx client
    client = OpenAI(
        api_key=api_key,
        http_client=http_client
    )
    
    return client


class CommitMessage(BaseModel):
    """Commit message model."""
    type: str
    scope: Optional[str] = None
    description: str
    body: Optional[str] = None
    breaking: bool = False


class ChangelogChange(BaseModel):
    """Changelog change model."""
    title: str
    description: Optional[str] = None
    pr_number: Optional[int] = None


class ChangelogEntry(BaseModel):
    """Changelog entry model."""
    section: str
    changes: List[ChangelogChange]


class VersionBumpAnalysis(BaseModel):
    """Version bump analysis model."""
    bump_type: str
    reason: str
    has_breaking_changes: bool


class ReleaseTitle(BaseModel):
    """Release title model."""
    title: str
    highlights: List[str]


def get_uncommitted_changes() -> List[str]:
    """Get list of uncommitted changes."""
    changes = []
    
    # Get staged changes
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        check=True,
        capture_output=True,
        text=True
    ).stdout.strip().split("\n")
    if staged and staged[0]:
        changes.extend(staged)
    
    # Get unstaged changes
    unstaged = subprocess.run(
        ["git", "diff", "--name-only"],
        check=True,
        capture_output=True,
        text=True
    ).stdout.strip().split("\n")
    if unstaged and unstaged[0]:
        changes.extend(unstaged)
    
    # Get untracked files
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True
    ).stdout.strip().split("\n")
    if untracked and untracked[0]:
        changes.extend(untracked)
    
    return sorted(list(set(changes)))


def get_commits_since_last_tag() -> List[str]:
    """Get all commits since the last tag."""
    try:
        # Get the last tag
        last_tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Get commits since last tag
        commits = subprocess.run(
            ["git", "log", f"{last_tag}..HEAD", "--oneline"],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        # No tags found, get all commits
        commits = subprocess.run(
            ["git", "log", "--oneline"],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip().split("\n")
    
    return commits if commits and commits[0] else []


def get_pull_requests_since_last_tag() -> List[Dict[str, Any]]:
    """Get all merged pull requests since the last tag."""
    try:
        # Check if GitHub CLI is available
        subprocess.run(
            ["gh", "--version"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Get the last tag's date
        try:
            last_tag = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            last_tag_date = subprocess.run(
                ["git", "log", "-1", "--format=%ai", last_tag],
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            # Parse the date
            last_tag_date = datetime.strptime(last_tag_date, "%Y-%m-%d %H:%M:%S %z")
            date_filter = f"--created-after={last_tag_date.strftime('%Y-%m-%d')}"
        except subprocess.CalledProcessError:
            # No tags found, don't use date filter
            date_filter = ""
        
        # Get merged PRs
        prs_json = subprocess.run(
            ["gh", "pr", "list", "--state", "merged", "--json", "number,title", date_filter],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        return json.loads(prs_json) if prs_json else []
    except subprocess.CalledProcessError:
        console.print("GitHub CLI not available, skipping PR analysis")
        return []


def analyze_changes_for_version_bump(model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """Analyze git changes to determine version bump type.
    
    Args:
        model: OpenAI model to use
        temperature: Model temperature
    
    Returns:
        Version bump type (major, minor, patch)
    """
    client = get_openai_client()
    commits = get_commits_since_last_tag()
    prs = get_pull_requests_since_last_tag()
    
    if not commits and not prs:
        return "patch"  # Default to patch if no changes
    
    # Prepare context
    context = []
    if commits:
        context.append("Commits:")
        context.extend(f"- {commit}" for commit in commits)
    if prs:
        context.append("\nPull Requests:")
        context.extend(f"- #{pr['number']}: {pr['title']}" for pr in prs)
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes code changes to determine the appropriate version bump type following semantic versioning. Respond with a JSON object containing: bump_type (string), reason (string), and has_breaking_changes (boolean)."
            },
            {
                "role": "user",
                "content": f"Analyze these changes and determine if they require a major, minor, or patch version bump:\n\n{chr(10).join(context)}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=temperature
    )
    
    response = json.loads(completion.choices[0].message.content)
    return response["bump_type"]


def generate_release_title(version: str, changelog: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """Generate a release title based on version and changelog.
    
    Args:
        version: Version string
        changelog: Changelog text
        model: OpenAI model to use
        temperature: Model temperature
    
    Returns:
        Generated release title
    """
    client = get_openai_client()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates concise and informative release titles based on version and changelog information. Respond with a JSON object containing: title (string) and highlights (array of strings)."
            },
            {
                "role": "user",
                "content": f"Generate a release title for version {version} based on this changelog:\n\n{changelog}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=temperature
    )
    
    response = json.loads(completion.choices[0].message.content)
    title = ReleaseTitle(**response)
    return f"{title.title} ({', '.join(title.highlights)})"


def generate_changelog_with_ai(model: str = "gpt-4o-mini", temperature: float = 0.7, sections: List[str] = None) -> str:
    """Generate changelog using AI.
    
    Args:
        model: OpenAI model to use
        temperature: Model temperature
        sections: Optional list of changelog sections
    
    Returns:
        Generated changelog text
    """
    client = get_openai_client()
    commits = get_commits_since_last_tag()
    prs = get_pull_requests_since_last_tag()
    
    if not commits and not prs:
        return "No changes to document"
    
    # Prepare context
    context = []
    if commits:
        context.append("Commits:")
        context.extend(f"- {commit}" for commit in commits)
    if prs:
        context.append("\nPull Requests:")
        context.extend(f"- #{pr['number']}: {pr['title']}" for pr in prs)
    
    # Default sections if none provided
    if sections is None:
        sections = [
            "Features",
            "Bug Fixes",
            "Documentation",
            "Internal Changes"
        ]
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that generates changelogs from Git history. Please organize the changes into these sections: {', '.join(sections)}. Respond with a JSON object containing an 'entries' array, where each entry has: section (string) and changes (array of objects with title, description, and pr_number fields)."
            },
            {
                "role": "user",
                "content": f"Generate a changelog from these changes:\n\n{chr(10).join(context)}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=temperature
    )
    
    response = json.loads(completion.choices[0].message.content)
    entries = [ChangelogEntry(**entry) for entry in response["entries"]]
    
    # Format changelog
    lines = []
    for entry in entries:
        if not entry.changes:
            continue
            
        lines.append(f"## {entry.section}")
        lines.append("")
        
        for change in entry.changes:
            line = f"- {change.title}"
            if change.description:
                line += f": {change.description}"
            if change.pr_number:
                line += f" (#{change.pr_number})"
            lines.append(line)
        
        lines.append("")
    
    return "\n".join(lines).strip() 