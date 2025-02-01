"""AI-powered utilities for Python Release Master."""

import json
import os
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional

from openai import OpenAI
from pydantic import BaseModel
from rich.console import Console

from python_release_master.core.config import Config

console = Console()


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


def commit_changes_with_ai() -> None:
    """Commit changes with AI-generated message."""
    changes = get_uncommitted_changes()
    if not changes:
        console.print("No changes to commit")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    commit_msg = client.generate_commit_message(changes)
    
    subprocess.run(
        ["git", "commit", "-m", commit_msg],
        check=True,
        capture_output=True,
        text=True
    )


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


def analyze_changes_for_version_bump() -> str:
    """Analyze changes to determine version bump type.
    
    Returns:
        Version bump type (major, minor, patch)
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
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
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes code changes to determine the appropriate version bump type following semantic versioning."
            },
            {
                "role": "user",
                "content": f"Analyze these changes and determine if they require a major, minor, or patch version bump:\n\n{chr(10).join(context)}"
            }
        ],
        response_format=VersionBumpAnalysis
    )
    
    analysis = completion.choices[0].message.parsed
    console.print(f"[yellow]Version bump analysis: {analysis.reason}[/yellow]")
    return analysis.bump_type


def generate_release_title(version: str, changelog: str) -> str:
    """Generate release title from version and changelog.
    
    Args:
        version: Version string
        changelog: Generated changelog text
    
    Returns:
        Generated release title
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates concise and informative release titles based on version and changelog information."
            },
            {
                "role": "user",
                "content": f"Generate a release title for version {version} based on this changelog:\n\n{changelog}"
            }
        ],
        response_format=ReleaseTitle
    )
    
    title_data = completion.choices[0].message.parsed
    return title_data.title


def generate_changelog_with_ai(config: Config) -> str:
    """Generate changelog using OpenAI.
    
    Args:
        config: Configuration object
    
    Returns:
        Generated changelog text
    """
    client = OpenAI()
    commits = get_commits_since_last_tag()
    prs = get_pull_requests_since_last_tag()
    
    if not commits and not prs:
        return "No changes since last release"
    
    # Prepare context
    context = []
    if commits:
        context.append("Commits:")
        context.extend(f"- {commit}" for commit in commits)
    if prs:
        context.append("\nPull Requests:")
        context.extend(f"- #{pr['number']}: {pr['title']}" for pr in prs)
    
    # Generate changelog entries for each section
    entries = []
    for section in config.changelog.sections:
        entry = client.generate_changelog_entry(
            commits=commits,
            prs=prs,
            section=section,
            commit_conventions=config.changelog.commit_conventions
        )
        if entry.changes:
            entries.append(entry)
    
    # Format changelog
    changelog = []
    for entry in entries:
        changelog.append(f"## {entry.section}")
        for change in entry.changes:
            line = f"- {change.title}"
            if change.pr_number:
                line += f" (#{change.pr_number})"
            if change.description:
                line += f"\n  {change.description}"
            changelog.append(line)
        changelog.append("")
    
    return "\n".join(changelog).strip()


class OpenAI:
    """OpenAI client wrapper."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)

    def generate_changelog_entry(
        self,
        commits: List[str],
        prs: List[Dict[str, Any]],
        section: str,
        commit_conventions: Dict[str, str]
    ) -> ChangelogEntry:
        """Generate changelog entry for a section using OpenAI.
        
        Args:
            commits: List of commit messages
            prs: List of pull requests
            section: Section name
            commit_conventions: Mapping of commit types to sections
        
        Returns:
            Changelog entry
        """
        # Filter commits and PRs for this section
        section_commits = []
        for commit in commits:
            for commit_type, section_name in commit_conventions.items():
                if section_name == section and commit.startswith(f"{commit_type}:"):
                    section_commits.append(commit)
        
        section_prs = [pr for pr in prs if any(
            commit_type for commit_type, section_name in commit_conventions.items()
            if section_name == section and pr["title"].startswith(f"{commit_type}:")
        )]
        
        if not section_commits and not section_prs:
            return ChangelogEntry(section=section, changes=[])
        
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that generates changelog entries for the {section} section."
                },
                {
                    "role": "user",
                    "content": f"Generate a changelog entry from these changes:\n\nCommits:\n{chr(10).join(section_commits)}\n\nPull Requests:\n{json.dumps(section_prs, indent=2)}"
                }
            ],
            response_format=ChangelogEntry
        )
        
        return completion.choices[0].message.parsed

    def generate_commit_message(self, changes: List[str]) -> str:
        """Generate commit message from changes using OpenAI.
        
        Args:
            changes: List of changed files
        
        Returns:
            Generated commit message
        """
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates conventional commit messages from file changes."
                },
                {
                    "role": "user",
                    "content": f"Generate a conventional commit message for these changes:\n{chr(10).join(changes)}"
                }
            ],
            response_format=CommitMessage
        )
        
        commit_data = completion.choices[0].message.parsed
        
        # Format commit message
        msg = f"{commit_data.type}"
        if commit_data.scope:
            msg += f"({commit_data.scope})"
        msg += f": {commit_data.description}"
        if commit_data.breaking:
            msg += "\n\nBREAKING CHANGE: "
        if commit_data.body:
            msg += f"\n\n{commit_data.body}"
        
        return msg