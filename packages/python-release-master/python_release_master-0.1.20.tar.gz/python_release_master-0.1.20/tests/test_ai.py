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
        assert len(changes) == 3
        assert "file1.py" in changes
        assert "file2.py" in changes
        assert "file3.py" in changes


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
         patch("python_release_master.core.ai.OpenAI") as mock_openai, \
         patch("subprocess.run") as mock_run:
        mock_changes.return_value = changes

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_client.generate_commit_message.return_value = expected_msg
        mock_openai.return_value = mock_client

        commit_msg = commit_changes_with_ai()

        assert commit_msg == expected_msg
        mock_run.assert_any_call(["git", "add", "."], check=True)
        mock_run.assert_any_call(["git", "commit", "-m", expected_msg], check=True)


def test_get_commits_since_last_tag_with_tag():
    """Test getting commits when a tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="v1.0.0\n"),  # git describe
            MagicMock(stdout="abc123 Fix bug\ndef456 Add feature\n"),  # git log
        ]
        commits = get_commits_since_last_tag()
        assert commits == "abc123 Fix bug\ndef456 Add feature"


def test_get_commits_since_last_tag_no_tag():
    """Test getting commits when no tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="No tags found"),  # git describe fails
            MagicMock(stdout="abc123 Initial commit\n"),  # git log
        ]
        commits = get_commits_since_last_tag()
        assert commits == "abc123 Initial commit"


def test_get_pull_requests_since_last_tag_with_tag():
    """Test getting PRs when a tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="gh version 2.0.0\n"),  # gh version
            MagicMock(stdout="v1.0.0\n"),  # git describe
            MagicMock(stdout='[{"number": 1, "title": "Add feature"}]'),  # gh pr list
        ]
        prs = get_pull_requests_since_last_tag()
        assert prs == '[{"number": 1, "title": "Add feature"}]'


def test_get_pull_requests_since_last_tag_no_tag():
    """Test getting PRs when no tag exists."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(stdout="gh version 2.0.0\n"),  # gh version
            MagicMock(returncode=1, stderr="No tags found"),  # git describe fails
            MagicMock(stdout='[{"number": 1, "title": "Initial PR"}]'),  # gh pr list
        ]
        prs = get_pull_requests_since_last_tag()
        assert prs == '[{"number": 1, "title": "Initial PR"}]'


def test_get_pull_requests_since_last_tag_no_gh_cli():
    """Test getting PRs when GitHub CLI is not available."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "gh --version", stderr="gh: command not found")
        prs = get_pull_requests_since_last_tag()
        assert prs == "No pull requests found or GitHub CLI not available"


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
         patch("python_release_master.core.ai.OpenAI") as mock_openai:
        mock_commits.return_value = "abc123 Fix bug\ndef456 Add feature"

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_client.generate_changelog.return_value = "## Features\n- Add feature\n\n## Bug Fixes\n- Fix bug"
        mock_openai.return_value = mock_client

        changelog = generate_changelog_with_ai(config)
        assert changelog == "## Features\n- Add feature\n\n## Bug Fixes\n- Fix bug"


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
         patch("python_release_master.core.ai.OpenAI") as mock_openai:
        mock_commits.return_value = "abc123 Fix bug"

        # Mock OpenAI response
        mock_client = MagicMock()
        mock_client.generate_changelog.return_value = "## Bug Fixes\n- Fix bug"
        mock_openai.return_value = mock_client

        changelog = generate_changelog_with_ai(config)
        assert changelog == "## Bug Fixes\n- Fix bug"


def test_openai_generate_changelog():
    """Test OpenAI changelog generation."""
    client = OpenAI()
    commits = "abc123 Fix bug\ndef456 Add feature"

    with patch.object(client, "client") as mock_client:
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "version_bump": "minor",
                        "changes": [
                            {
                                "title": "Add feature",
                                "description": "New feature added",
                                "section": "Features",
                                "type": "feat",
                                "breaking": False
                            }
                        ],
                        "changelog_md": "## Features\n- Add feature"
                    })
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        changelog = client.generate_changelog(commits)
        assert changelog == "## Features\n- Add feature"


def test_openai_generate_commit_message():
    """Test OpenAI commit message generation."""
    client = OpenAI()
    changes = ["file1.py", "file2.py"]

    with patch.object(client, "client") as mock_client:
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "type": "feat",
                        "scope": "core",
                        "description": "add new feature",
                        "body": "Detailed description",
                        "breaking": False
                    })
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        commit_msg = client.generate_commit_message(changes)
        assert commit_msg == "feat(core): add new feature\n\nDetailed description" 