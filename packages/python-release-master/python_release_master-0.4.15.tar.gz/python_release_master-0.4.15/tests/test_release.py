"""Tests for the release module."""

import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import pytest

from python_release_master.core.config import Config, ChangelogConfig
from python_release_master.core.release import (
    create_release,
    bump_version,
    get_current_version,
    update_version_in_file,
    generate_changelog,
    build_package,
    publish_to_pypi,
    create_git_release,
)


@pytest.fixture
def basic_config():
    """Create a basic configuration for testing."""
    return Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(),
    )


def test_get_current_version():
    """Test version extraction from file."""
    content = 'version = "1.2.3"\n'
    with patch("builtins.open", mock_open(read_data=content)):
        version = get_current_version("pyproject.toml")
        assert version == "1.2.3"


def test_update_version_in_file():
    """Test version update in file."""
    content = 'version = "1.2.3"\n'
    mock_file = mock_open(read_data=content)
    with patch("builtins.open", mock_file):
        update_version_in_file("pyproject.toml", "1.2.4")
        mock_file().write.assert_called_once_with('version = "1.2.4"\n')


def test_bump_version_major():
    """Test major version bump."""
    content = 'version = "1.2.3"\n'
    mock_file = mock_open(read_data=content)
    with patch("builtins.open", mock_file):
        bump_version("major", ["pyproject.toml"])
        mock_file().write.assert_called_once_with('version = "2.0.0"\n')


def test_bump_version_minor():
    """Test minor version bump."""
    content = 'version = "1.2.3"\n'
    mock_file = mock_open(read_data=content)
    with patch("builtins.open", mock_file):
        bump_version("minor", ["pyproject.toml"])
        mock_file().write.assert_called_once_with('version = "1.3.0"\n')


def test_bump_version_patch():
    """Test patch version bump."""
    content = 'version = "1.2.3"\n'
    mock_file = mock_open(read_data=content)
    with patch("builtins.open", mock_file):
        bump_version("patch", ["pyproject.toml"])
        mock_file().write.assert_called_once_with('version = "1.2.4"\n')


def test_bump_version_invalid():
    """Test invalid version bump type."""
    with pytest.raises(ValueError, match="Invalid bump type"):
        bump_version("invalid", ["pyproject.toml"])


def test_generate_changelog_ai_success(basic_config):
    """Test AI-powered changelog generation."""
    expected_changelog = "## Features\n- Add feature"
    with patch("python_release_master.core.release.generate_changelog_with_ai") as mock_ai:
        mock_ai.return_value = expected_changelog
        result = generate_changelog(basic_config)
        assert result == expected_changelog
        mock_ai.assert_called_once_with(basic_config)


def test_generate_changelog_ai_failure(basic_config):
    """Test fallback when AI changelog generation fails."""
    with patch("python_release_master.core.release.generate_changelog_with_ai") as mock_ai, \
         patch("python_release_master.core.changelog.generate_changelog") as mock_fallback:
        mock_ai.return_value = ""
        mock_fallback.return_value = "## Features\n- Add feature"
        result = generate_changelog(basic_config)
        assert result == "## Features\n- Add feature"
        mock_ai.assert_called_once_with(basic_config)
        mock_fallback.assert_called_once()


def test_build_package_success(tmp_path):
    """Test successful package build."""
    os.chdir(tmp_path)
    os.makedirs("dist")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        # Create dummy dist files
        with open("dist/package-0.1.0-py3-none-any.whl", "w") as f:
            f.write("dummy wheel")
        with open("dist/package-0.1.0.tar.gz", "w") as f:
            f.write("dummy sdist")

        success, message = build_package()
        assert success
        assert "Package built successfully" in message
        assert mock_run.call_count == 1
        assert mock_run.call_args[0][0] == ["python", "-m", "build", "--wheel", "--sdist"]


def test_build_package_failure():
    """Test package build failure."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "python -m build", stderr="Build failed")
        success, message = build_package()
        assert not success
        assert "Build command failed" in message


def test_build_package_missing_files(tmp_path):
    """Test build with missing package files."""
    os.chdir(tmp_path)
    os.makedirs("dist")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        success, message = build_package()
        assert not success
        assert "No package files were created" in message


def test_publish_to_pypi_success():
    """Test successful PyPI publication."""
    with patch("subprocess.run") as mock_run, \
         patch.dict(os.environ, {"PYPI_TOKEN": "dummy_token"}), \
         patch("os.path.exists") as mock_exists, \
         patch("os.listdir") as mock_listdir:
        mock_run.return_value = MagicMock(returncode=0)
        mock_exists.return_value = True
        mock_listdir.return_value = ["package.whl"]

        success, message = publish_to_pypi()
        assert success
        assert "successfully" in message
        mock_run.assert_called_once()


def test_publish_to_pypi_failure():
    """Test PyPI publication failure."""
    with patch("subprocess.run") as mock_run, \
         patch.dict(os.environ, {"PYPI_TOKEN": "dummy_token"}), \
         patch("os.path.exists") as mock_exists, \
         patch("os.listdir") as mock_listdir:
        mock_exists.return_value = True
        mock_listdir.return_value = ["package.whl"]
        mock_run.side_effect = subprocess.CalledProcessError(1, "twine upload", stderr="Upload failed")

        success, message = publish_to_pypi()
        assert not success
        assert "Failed to publish package" in message


def test_publish_to_pypi_no_token():
    """Test PyPI publication without token."""
    with patch.dict(os.environ, {}, clear=True):
        success, message = publish_to_pypi()
        assert not success
        assert "PYPI_TOKEN" in message


def test_create_git_release_success():
    """Test successful Git release creation."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        success, message = create_git_release("1.0.0", "Release v1.0.0", "Description")
        assert success
        assert "v1.0.0" in message
        assert mock_run.call_count >= 3  # tag create, tag push, release create


def test_create_git_release_no_gh():
    """Test Git release creation without GitHub CLI."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(127, "gh --version", stderr="gh: command not found")
        success, message = create_git_release("1.0.0", "Release v1.0.0", "Description")
        assert not success
        assert "GitHub CLI not installed" in message


def test_create_release_all_steps(tmp_path):
    """Test full release process with all steps."""
    os.chdir(tmp_path)
    os.makedirs("dist")

    config = Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(
            ai_powered=True,
            openai_model="gpt-4",
            sections=["Features", "Bug Fixes"]
        )
    )

    with patch("python_release_master.core.release.bump_version") as mock_bump, \
         patch("python_release_master.core.release.get_current_version") as mock_version, \
         patch("python_release_master.core.release.generate_changelog") as mock_changelog, \
         patch("python_release_master.core.release.build_package") as mock_build, \
         patch("python_release_master.core.release.publish_to_pypi") as mock_publish, \
         patch("python_release_master.core.release.create_git_release") as mock_git:

        mock_version.return_value = "1.0.0"
        mock_changelog.return_value = "## Features\n- Add feature"
        mock_build.return_value = (True, "Package built successfully")
        mock_publish.return_value = (True, "Package published successfully")
        mock_git.return_value = (True, "Release created successfully")

        create_release("minor", "Release 1.0.0", "Test release", config)

        mock_bump.assert_called_once_with("minor", ["pyproject.toml"])
        mock_version.assert_called_once_with("pyproject.toml")
        mock_changelog.assert_called_once_with(config)
        mock_build.assert_called_once()
        mock_publish.assert_called_once()
        mock_git.assert_called_once_with("1.0.0", "Release 1.0.0", "Test release\n\n## Features\n- Add feature")


def test_create_release_skip_steps(tmp_path):
    """Test release process with skipped steps."""
    os.chdir(tmp_path)
    os.makedirs("dist")

    config = Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(
            ai_powered=True,
            openai_model="gpt-4",
            sections=["Features", "Bug Fixes"]
        )
    )

    with patch("python_release_master.core.release.bump_version") as mock_bump, \
         patch("python_release_master.core.release.get_current_version") as mock_version, \
         patch("python_release_master.core.release.generate_changelog") as mock_changelog, \
         patch("python_release_master.core.release.build_package") as mock_build, \
         patch("python_release_master.core.release.publish_to_pypi") as mock_publish, \
         patch("python_release_master.core.release.create_git_release") as mock_git:

        mock_version.return_value = "1.0.0"
        mock_changelog.return_value = "## Features\n- Add feature"
        mock_build.return_value = (True, "Package built successfully")
        mock_publish.return_value = (True, "Package published successfully")
        mock_git.return_value = (True, "Release created successfully")

        create_release("minor", "Release 1.0.0", "Test release", config, skip_steps=["build", "publish"])

        mock_bump.assert_called_once_with("minor", ["pyproject.toml"])
        mock_version.assert_called_once_with("pyproject.toml")
        mock_changelog.assert_called_once_with(config)
        mock_build.assert_not_called()
        mock_publish.assert_not_called()
        mock_git.assert_called_once_with("1.0.0", "Release 1.0.0", "Test release\n\n## Features\n- Add feature")


def test_get_current_version():
    """Test getting current version."""
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = 'version = "1.0.0"'
        version = get_current_version("pyproject.toml")
        assert version == "1.0.0"


def test_bump_version():
    """Test version bumping."""
    content = 'version = "1.0.0"'
    with patch("builtins.open", create=True) as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = content
        mock_open.return_value.__enter__.return_value = mock_file

        bump_version("minor", ["pyproject.toml"])
        
        # Check that the file was written with the new version
        mock_file.write.assert_called_once()
        assert 'version = "1.1.0"' in mock_file.write.call_args[0][0] 