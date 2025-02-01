"""Tests for the testing module."""

import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from python_release_master.core.config import Config, ChangelogConfig
from python_release_master.core.testing import (
    run_tests,
    run_unit_tests,
    run_integration_tests,
    run_docker_tests,
    TestError,
)


@pytest.fixture
def basic_config():
    """Create a basic configuration for testing."""
    return Config(
        version_files=["pyproject.toml"],
        changelog=ChangelogConfig(),
    )


def test_run_unit_tests_no_tests_dir(tmp_path):
    """Test unit tests are skipped when no tests directory exists."""
    os.chdir(tmp_path)
    run_unit_tests()  # Should not raise


def test_run_unit_tests_success(tmp_path):
    """Test successful unit test execution."""
    os.chdir(tmp_path)
    Path("tests").mkdir()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_unit_tests()
        mock_run.assert_called_once()


def test_run_unit_tests_failure(tmp_path):
    """Test unit test execution failure."""
    os.chdir(tmp_path)
    Path("tests").mkdir()
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "pytest", "Test failed")
        with pytest.raises(TestError, match="Unit tests failed"):
            run_unit_tests()


def test_run_integration_tests_no_tests(tmp_path):
    """Test integration tests are skipped when no integration tests exist."""
    os.chdir(tmp_path)
    run_integration_tests()  # Should not raise


def test_run_integration_tests_success(tmp_path):
    """Test successful integration test execution."""
    os.chdir(tmp_path)
    Path("tests/integration").mkdir(parents=True)
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_integration_tests()
        mock_run.assert_called_once()


def test_run_docker_tests_no_dockerfile(tmp_path):
    """Test Docker tests are skipped when no Dockerfile.test exists."""
    os.chdir(tmp_path)
    run_docker_tests()  # Should not raise


def test_run_docker_tests_success(tmp_path):
    """Test successful Docker test execution."""
    os.chdir(tmp_path)
    Path("Dockerfile.test").touch()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_docker_tests()
        assert mock_run.call_count == 2  # Build and run


def test_run_docker_tests_build_failure(tmp_path):
    """Test Docker test failure during build."""
    os.chdir(tmp_path)
    Path("Dockerfile.test").touch()
    
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "docker build", "Build failed")
        with pytest.raises(TestError, match="Docker tests failed"):
            run_docker_tests()


def test_run_all_tests_success(basic_config):
    """Test successful execution of all test suites."""
    with patch("python_release_master.core.testing.run_unit_tests") as mock_unit, \
         patch("python_release_master.core.testing.run_integration_tests") as mock_int, \
         patch("python_release_master.core.testing.run_docker_tests") as mock_docker:
        run_tests(basic_config)
        mock_unit.assert_called_once()
        mock_int.assert_called_once()
        mock_docker.assert_called_once() 