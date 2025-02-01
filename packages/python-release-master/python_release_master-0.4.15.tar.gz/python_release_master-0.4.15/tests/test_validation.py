"""Tests for the validation module."""

import os
from pathlib import Path

import pytest

from python_release_master.core.config import Config, ChangelogConfig
from python_release_master.core.validation import validate_environment, validate_package


@pytest.fixture
def basic_config():
    """Create a basic configuration for testing."""
    return Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(),
    )


def test_validate_environment_missing_pypi_token(basic_config, monkeypatch):
    """Test validation fails when PYPI_TOKEN is missing."""
    monkeypatch.delenv("PYPI_TOKEN", raising=False)
    with pytest.raises(ValueError, match="PYPI_TOKEN environment variable is required"):
        validate_environment(basic_config)


def test_validate_environment_missing_openai_key(basic_config, monkeypatch):
    """Test validation fails when OPENAI_API_KEY is missing for AI changelog."""
    monkeypatch.setenv("PYPI_TOKEN", "dummy-token")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is required"):
        validate_environment(basic_config)


def test_validate_environment_missing_version_file(basic_config, monkeypatch, tmp_path):
    """Test validation fails when version file is missing."""
    monkeypatch.setenv("PYPI_TOKEN", "dummy-token")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    os.chdir(tmp_path)  # Move to empty directory
    with pytest.raises(ValueError, match="Version file not found"):
        validate_environment(basic_config)


def test_validate_package_missing_files(tmp_path, basic_config):
    """Test package validation fails when required files are missing."""
    os.chdir(tmp_path)
    with pytest.raises(ValueError, match="Required file not found"):
        validate_package(basic_config)


def test_validate_package_missing_src(tmp_path, basic_config):
    """Test package validation fails when src directory is missing."""
    os.chdir(tmp_path)
    Path("pyproject.toml").touch()
    Path("README.md").touch()
    Path("LICENSE").touch()
    with pytest.raises(ValueError, match="No Python package found in src directory"):
        validate_package(basic_config)


def test_validate_package_missing_tests(tmp_path, basic_config):
    """Test package validation fails when tests directory is missing."""
    os.chdir(tmp_path)
    Path("pyproject.toml").touch()
    Path("README.md").touch()
    Path("LICENSE").touch()
    Path("src/package/__init__.py").mkdir(parents=True)
    with pytest.raises(ValueError, match="No tests directory found"):
        validate_package(basic_config)


def test_validate_package_missing_docs(tmp_path, basic_config):
    """Test package validation fails when docs directory is missing."""
    os.chdir(tmp_path)
    Path("pyproject.toml").touch()
    Path("README.md").touch()
    Path("LICENSE").touch()
    Path("src/package/__init__.py").mkdir(parents=True)
    Path("tests").mkdir()
    with pytest.raises(ValueError, match="No documentation directory found"):
        validate_package(basic_config) 