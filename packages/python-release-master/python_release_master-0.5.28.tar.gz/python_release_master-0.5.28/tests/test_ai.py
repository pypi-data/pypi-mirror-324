"""Tests for the AI module."""

import json
import os
from unittest.mock import patch, MagicMock
import subprocess

import pytest
from python_release_master.core.ai import (
    get_uncommitted_changes,
    commit_changes_with_ai,
    get_commits_since_last_tag,
    get_pull_requests_since_last_tag,
    generate_changelog_with_ai,
    OpenAI
)
from python_release_master.core.config import Config, ChangelogConfig


def test_get_uncommitted_changes():
    """Test getting uncommitted changes."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="file1.py\n"),  # staged
            MagicMock(stdout="file2.py\n"),  # unstaged
            MagicMock(stdout="file3.py\n"),  # untracked
        ]
        changes = get_uncommitted_changes()
        assert changes == ["file1.py", "file2.py", "file3.py"]


def test_commit_changes_with_ai():
    """Test committing changes with AI-generated message."""
    changes = ["file1.py", "file2.py"]
    commit_data = {
        "type": "feat",
        "scope": None,
        "description": "add new feature",
        "body": "Detailed description",
        "breaking": False
    }
    expected_msg = "feat: add new feature\n\nDetailed description"

    with patch("python_release_master.core.ai.get_uncommitted_changes") as mock_changes, \
         patch("openai.OpenAI") as mock_openai, \
         patch("subprocess.run") as mock_run:
        mock_changes.return_value = changes
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(commit_data)
        mock_openai.return_value = mock_client
        mock_run.return_value = MagicMock(returncode=0)

        commit_changes_with_ai()
        mock_run.assert_called_with(
            ["git", "commit", "-m", expected_msg],
            check=True,
            capture_output=True,
            text=True
        )


def test_get_commits_since_last_tag_with_tag():
    """Test getting commits when a tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="v1.0.0\n"),  # git describe
            MagicMock(stdout="abc123 Fix bug\ndef456 Add feature\n"),  # git log
        ]
        commits = get_commits_since_last_tag()
        assert commits == ["abc123 Fix bug", "def456 Add feature"]


def test_get_commits_since_last_tag_no_tag():
    """Test getting commits when no tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="No tags found"),  # git describe fails
            MagicMock(stdout="abc123 Initial commit\n"),  # git log
        ]
        commits = get_commits_since_last_tag()
        assert commits == ["abc123 Initial commit"]


def test_get_pull_requests_since_last_tag_with_tag():
    """Test getting PRs when a tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="gh version 2.0.0\n"),  # gh version
            MagicMock(stdout="v1.0.0\n"),  # git describe
            MagicMock(stdout="2023-01-01 00:00:00 +0000\n"),  # git log
            MagicMock(stdout='[{"number": 1, "title": "Add feature"}]'),  # gh pr list
        ]
        prs = get_pull_requests_since_last_tag()
        assert prs == [{"number": 1, "title": "Add feature"}]


def test_get_pull_requests_since_last_tag_no_tag():
    """Test getting PRs when no tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="gh version 2.0.0\n"),  # gh version
            MagicMock(returncode=1, stderr="No tags found"),  # git describe fails
            MagicMock(stdout='[{"number": 1, "title": "Initial PR"}]'),  # gh pr list
        ]
        prs = get_pull_requests_since_last_tag()
        assert prs == [{"number": 1, "title": "Initial PR"}]


def test_get_pull_requests_since_last_tag_no_gh_cli():
    """Test getting PRs when GitHub CLI is not available."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "gh --version", stderr="gh: command not found")
        prs = get_pull_requests_since_last_tag()
        assert prs == []


def test_generate_changelog_with_ai():
    """Test changelog generation with OpenAI."""
    config = Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(
            ai_powered=True,
            openai_model="gpt-4",
            sections=["Features", "Bug Fixes"]
        )
    )

    with patch("python_release_master.core.ai.get_commits_since_last_tag") as mock_commits, \
         patch("openai.OpenAI") as mock_openai:
        mock_commits.return_value = ["abc123 Fix bug", "def456 Add feature"]

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = "## Features\n- Add feature\n\n## Bug Fixes\n- Fix bug"
        mock_openai.return_value = mock_client

        changelog = generate_changelog_with_ai(config)
        assert "## Features" in changelog
        assert "## Bug Fixes" in changelog
        assert "Add feature" in changelog
        assert "Fix bug" in changelog


def test_generate_changelog_with_ai_custom_model():
    """Test changelog generation with custom model."""
    config = Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(
            ai_powered=True,
            openai_model="gpt-3.5-turbo",
            sections=["Features", "Bug Fixes"]
        )
    )

    with patch("python_release_master.core.ai.get_commits_since_last_tag") as mock_commits, \
         patch("openai.OpenAI") as mock_openai:
        mock_commits.return_value = ["abc123 Fix bug"]

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = "## Bug Fixes\n- Fix bug"
        mock_openai.return_value = mock_client

        changelog = generate_changelog_with_ai(config)
        assert "## Bug Fixes" in changelog
        assert "Fix bug" in changelog


def test_openai_generate_changelog():
    """Test OpenAI changelog generation."""
    api_key = os.environ.get("OPENAI_API_KEY", "test-key")
    client = OpenAI(api_key=api_key)
    commits = ["abc123 Fix bug", "def456 Add feature"]

    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = "## Features\n- Add feature\n\n## Bug Fixes\n- Fix bug"
        mock_openai.return_value = mock_client

        changelog = client.generate_changelog(commits, ["Features", "Bug Fixes"])
        assert "## Features" in changelog
        assert "## Bug Fixes" in changelog
        assert "Add feature" in changelog
        assert "Fix bug" in changelog


def test_openai_generate_commit_message():
    """Test OpenAI commit message generation."""
    api_key = os.environ.get("OPENAI_API_KEY", "test-key")
    client = OpenAI(api_key=api_key)
    changes = ["file1.py", "file2.py"]

    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps({
            "type": "feat",
            "scope": None,
            "description": "add new feature",
            "body": "Detailed description",
            "breaking": False
        })
        mock_openai.return_value = mock_client

        commit_msg = client.generate_commit_message(changes)
        assert "feat: add new feature" in commit_msg
        assert "Detailed description" in commit_msg 