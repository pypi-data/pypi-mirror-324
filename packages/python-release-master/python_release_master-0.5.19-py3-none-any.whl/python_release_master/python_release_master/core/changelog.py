"""Changelog generation utilities."""

import subprocess
from typing import List, Optional

from rich.console import Console

from python_release_master.core.ai import get_commits_since_last_tag, get_pull_requests_since_last_tag

console = Console()


def generate_changelog(sections: List[str], ai_powered: bool = False) -> str:
    """Generate changelog from git history.
    
    Args:
        sections: List of changelog sections
        ai_powered: Whether to use AI for changelog generation
    
    Returns:
        Generated changelog text
    """
    # Get commits and PRs
    commits = get_commits_since_last_tag()
    prs = get_pull_requests_since_last_tag()
    
    if not commits and not prs:
        return "No changes since last release"
    
    # Build changelog sections
    changelog = []
    for section in sections:
        section_changes = []
        
        # Add commits to appropriate sections
        for commit in commits:
            if _matches_section(commit, section):
                section_changes.append(f"- {_format_commit(commit)}")
        
        # Add PRs to appropriate sections
        for pr in prs:
            if _matches_section(pr["title"], section):
                section_changes.append(f"- #{pr['number']}: {pr['title']}")
        
        if section_changes:
            changelog.extend([f"## {section}", *section_changes, ""])
    
    return "\n".join(changelog).strip()


def _matches_section(text: str, section: str) -> bool:
    """Check if text matches a changelog section.
    
    Args:
        text: Text to check
        section: Section name
    
    Returns:
        True if text matches section
    """
    section_keywords = {
        "Features": ["feat", "feature", "add", "new"],
        "Bug Fixes": ["fix", "bug", "issue", "resolve"],
        "Documentation": ["doc", "docs", "document"],
        "Internal Changes": ["chore", "refactor", "test", "ci", "build"],
    }
    
    keywords = section_keywords.get(section, [section.lower()])
    text_lower = text.lower()
    
    return any(keyword in text_lower for keyword in keywords)


def _format_commit(commit: str) -> str:
    """Format commit message for changelog.
    
    Args:
        commit: Raw commit message
    
    Returns:
        Formatted commit message
    """
    # Remove commit hash
    if " " in commit:
        commit = commit.split(" ", 1)[1]
    
    # Clean up conventional commit prefixes
    prefixes = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    for prefix in prefixes:
        if commit.startswith(f"{prefix}:"):
            commit = commit[len(prefix) + 1:].strip()
            break
        if commit.startswith(f"{prefix}("):
            scope_end = commit.find(")")
            if scope_end != -1:
                commit = commit[scope_end + 2:].strip()
                break
    
    # Capitalize first letter
    if commit:
        commit = commit[0].upper() + commit[1:]
    
    return commit 