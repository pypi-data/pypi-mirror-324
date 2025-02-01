"""Tests for the configuration module."""

from pathlib import Path

import pytest
import yaml

from python_release_master.core.config import Config, ChangelogConfig, load_config


def test_changelog_config_defaults():
    """Test ChangelogConfig default values."""
    config = ChangelogConfig()
    assert config.ai_powered is True
    assert config.openai_model == "gpt-4"
    assert config.sections == ["Features", "Bug Fixes", "Documentation", "Internal Changes"]


def test_changelog_config_from_dict():
    """Test ChangelogConfig creation from dictionary."""
    data = {
        "ai_powered": False,
        "openai_model": "gpt-3.5-turbo",
        "sections": ["Added", "Changed", "Removed"],
    }
    config = ChangelogConfig.from_dict(data)
    assert config.ai_powered is False
    assert config.openai_model == "gpt-3.5-turbo"
    assert config.sections == ["Added", "Changed", "Removed"]


def test_config_from_dict():
    """Test Config creation from dictionary."""
    data = {
        "version_files": ["pyproject.toml", "src/package/__init__.py"],
        "changelog": {
            "ai_powered": True,
            "openai_model": "gpt-4",
            "sections": ["Features", "Fixes"],
        },
        "skip_steps": ["docker_tests"],
    }
    config = Config.from_dict(data)
    assert config.version_files == ["pyproject.toml", "src/package/__init__.py"]
    assert config.changelog.ai_powered is True
    assert config.changelog.sections == ["Features", "Fixes"]
    assert config.skip_steps == ["docker_tests"]


def test_load_config_default(tmp_path):
    """Test loading default configuration when no file exists."""
    config = load_config(tmp_path)
    assert config.version_files == ["pyproject.toml"]
    assert config.changelog.ai_powered is True
    assert config.skip_steps is None


def test_load_config_from_file(tmp_path):
    """Test loading configuration from file."""
    config_data = {
        "version_files": ["setup.py"],
        "changelog": {"ai_powered": False},
        "skip_steps": ["tests"],
    }
    config_file = tmp_path / ".release-master.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    
    config = load_config(tmp_path)
    assert config.version_files == ["setup.py"]
    assert config.changelog.ai_powered is False
    assert config.skip_steps == ["tests"] 