"""AI module for Python Release Master."""

import os
import subprocess
from typing import Dict, List, Any, Optional
import openai
from .config import Config, load_config
import json


def generate_changelog_with_ai(config: Config) -> str:
    """Generate changelog from git commits using OpenAI.
    
    Args:
        config: Configuration object with OpenAI settings
        
    Returns:
        Generated changelog text
    """
    # Get git commits since last tag
    commits = get_commits_since_last_tag()
    if not commits:
        return "No changes since last release"
    
    # Initialize OpenAI client
    client = OpenAI()
    
    # Generate changelog
    try:
        return client.generate_changelog(
            "\n".join(commits),
            model=config.changelog.openai_model
        )
    except ValueError as e:
        raise ValueError(f"Failed to generate changelog: {str(e)}")


def commit_changes_with_ai(model: str = "gpt-4") -> Optional[str]:
    """Generate and apply commit message using AI.
    
    Args:
        model: OpenAI model to use
        
    Returns:
        Generated commit message if successful, None otherwise
    """
    try:
        # Get uncommitted changes
        changes = get_uncommitted_changes()
        if not changes:
            return None
        
        # Initialize OpenAI client
        client = OpenAI()
        
        # Generate commit message
        commit_msg = client.generate_commit_message(changes, model=model)
        
        # Stage and commit changes
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        return commit_msg
    except (subprocess.CalledProcessError, ValueError) as e:
        raise ValueError(f"Failed to commit changes: {str(e)}")


def get_commits_since_last_tag() -> str:
    """Get git commits since the last tag."""
    try:
        # Get the last tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True
        )
        last_tag = result.stdout.strip()

        # Get commits since last tag
        result = subprocess.run(
            ["git", "log", f"{last_tag}..HEAD", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # No tags found, get all commits
        result = subprocess.run(
            ["git", "log", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()


def get_pull_requests_since_last_tag() -> str:
    """Get merged pull requests since the last tag."""
    try:
        # Check for GitHub CLI
        try:
            subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            return "No pull requests found or GitHub CLI not available"

        # Get the last tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True
        )
        last_tag = result.stdout.strip()

        # Get PRs using GitHub CLI
        cmd = ["gh", "pr", "list", "--state", "merged", "--json", "number,title"]
        if last_tag:
            cmd.extend(["--search", f"merged:>={last_tag}"])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "No pull requests found or GitHub CLI not available"


def get_uncommitted_changes() -> List[str]:
    """Get a list of uncommitted changes in the working directory."""
    try:
        # Get staged changes
        staged = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        staged_files = staged.stdout.strip().split("\n") if staged.stdout.strip() else []
        
        # Get unstaged changes
        unstaged = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        unstaged_files = unstaged.stdout.strip().split("\n") if unstaged.stdout.strip() else []
        
        # Get untracked files
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        )
        untracked_files = untracked.stdout.strip().split("\n") if untracked.stdout.strip() else []
        
        # Combine all changes
        all_changes = list(set(staged_files + unstaged_files + untracked_files))
        return [f for f in all_changes if f]  # Remove empty strings
        
    except subprocess.CalledProcessError:
        return []


def generate_commit_message(changes: List[str], model: str = "gpt-4-0125-preview") -> str:
    """Generate a commit message using AI based on the changes."""
    if not changes:
        return "No changes to commit"
    
    # Get the diff for each file
    diffs = []
    for file in changes:
        try:
            diff = subprocess.run(
                ["git", "diff", "--", file],
                capture_output=True,
                text=True,
                check=True
            )
            if diff.stdout:
                diffs.append(f"File: {file}\n{diff.stdout}")
        except subprocess.CalledProcessError:
            continue
    
    if not diffs:
        return "No changes to commit"
    
    # Prepare prompt for OpenAI
    prompt = (
        "Generate a concise commit message based on the following changes:\n\n"
        + "\n".join(diffs)
        + "\n\nCommit message:"
    )
    
    # Call OpenAI API
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Auto-commit: {', '.join(changes)}"


def analyze_changes(changes: List[str], model: str = "gpt-4-0125-preview") -> Dict[str, Any]:
    """Analyze changes to determine version bump and changelog sections."""
    if not changes:
        return {
            "version_bump": "patch",
            "sections": {},
            "description": "No significant changes detected"
        }
    
    # Get the diff for each file
    diffs = []
    for file in changes:
        try:
            diff = subprocess.run(
                ["git", "diff", "--", file],
                capture_output=True,
                text=True,
                check=True
            )
            if diff.stdout:
                diffs.append(f"File: {file}\n{diff.stdout}")
        except subprocess.CalledProcessError:
            continue
    
    if not diffs:
        return {
            "version_bump": "patch",
            "sections": {},
            "description": "No significant changes detected"
        }
    
    # Prepare prompt for OpenAI
    prompt = (
        "Analyze the following changes and provide:\n"
        "1. Recommended version bump (major, minor, or patch)\n"
        "2. Changelog sections (features, fixes, etc.)\n"
        "3. Brief description of changes\n\n"
        + "\n".join(diffs)
    )
    
    # Call OpenAI API
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        # Parse response
        analysis = response.choices[0].message.content
        
        # Extract version bump
        if "major" in analysis.lower():
            version_bump = "major"
        elif "minor" in analysis.lower():
            version_bump = "minor"
        else:
            version_bump = "patch"
        
        # Extract sections (simplified)
        sections = {
            "features": [],
            "fixes": [],
            "other": []
        }
        
        return {
            "version_bump": version_bump,
            "sections": sections,
            "description": analysis
        }
        
    except Exception as e:
        return {
            "version_bump": "patch",
            "sections": {},
            "description": f"Error analyzing changes: {str(e)}"
        }


def generate_changelog_with_openai(
    context: str,
    sections: List[str],
    model: str = "gpt-4-0125-preview"
) -> str:
    """Generate changelog using OpenAI API."""
    import openai

    # Prepare the prompt
    prompt = f"""Based on the following git history, generate a changelog with these sections: {', '.join(sections)}

Context:
{context}

Format the changelog in markdown with sections as level 2 headers (##).
Only include relevant changes and group similar changes together.
Be concise but descriptive.
"""

    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates changelogs from git history."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")


class OpenAI:
    """OpenAI API wrapper for generating changelogs."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
        """
        if api_key:
            openai.api_key = api_key
        self.client = openai.Client()

    def generate_changelog(self, commits: str, model: str = "gpt-4") -> str:
        """Generate changelog from git commits using OpenAI.
        
        Args:
            commits: Git commit messages to summarize
            model: OpenAI model to use
            
        Returns:
            Generated changelog text
        """
        # Define the expected JSON structure
        json_structure = {
            "type": "object",
            "properties": {
                "version_bump": {
                    "type": "string",
                    "enum": ["major", "minor", "patch"],
                    "description": "Type of version bump based on changes"
                },
                "bump_reason": {
                    "type": "string",
                    "description": "Reason for the version bump"
                },
                "changes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "section": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["feat", "fix", "docs", "chore", "refactor"]
                            },
                            "breaking": {"type": "boolean"}
                        },
                        "required": ["title", "section", "type", "breaking"]
                    }
                },
                "changelog_md": {
                    "type": "string",
                    "description": "Formatted changelog in markdown"
                }
            },
            "required": ["version_bump", "changes", "changelog_md"]
        }

        prompt = f"""Analyze these git commits and generate a structured changelog.
Follow the JSON schema exactly. Include version bump recommendation and formatted markdown.

Commits:
{commits}

Response must be valid JSON matching this schema:
{json.dumps(json_structure, indent=2)}"""

        response = self.client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates changelogs from git commits. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            # Parse and validate the JSON response
            changelog_data = json.loads(response.choices[0].message.content)
            return changelog_data["changelog_md"]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {str(e)}")

    def generate_commit_message(self, changes: List[str], model: str = "gpt-4") -> str:
        """Generate commit message from changes using OpenAI.
        
        Args:
            changes: List of changed files and their status
            model: OpenAI model to use
            
        Returns:
            Generated commit message
        """
        # Define the expected JSON structure
        json_structure = {
            "type": {
                "type": "string",
                "enum": ["feat", "fix", "docs", "chore", "refactor"],
                "description": "Type of change"
            },
            "scope": {
                "type": ["string", "null"],
                "description": "Scope of the change (optional)"
            },
            "description": {
                "type": "string",
                "description": "Short description of the change"
            },
            "body": {
                "type": "string",
                "description": "Detailed description of the change"
            },
            "breaking": {
                "type": "boolean",
                "description": "Whether this is a breaking change"
            }
        }

        prompt = f"""Analyze these changes and generate a conventional commit message.
Follow the JSON schema exactly. The message should follow conventional commits format.

Changes:
{changes}

Response must be valid JSON matching this schema:
{json.dumps(json_structure, indent=2)}"""

        response = self.client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates conventional commit messages. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            # Parse and validate the JSON response
            commit_data = json.loads(response.choices[0].message.content)
            
            # Format conventional commit message
            scope = f"({commit_data['scope']})" if commit_data.get('scope') else ""
            breaking = "!" if commit_data.get('breaking') else ""
            message = f"{commit_data['type']}{scope}{breaking}: {commit_data['description']}"
            
            if commit_data.get('body'):
                message += f"\n\n{commit_data['body']}"
                
            return message
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {str(e)}") 