"""Validation utilities for Python Release Master."""

import os
from pathlib import Path
from typing import List, Optional

from python_release_master.core.config import Config


def validate_environment(config: Config) -> None:
    """Validate the environment before running operations."""
    # Check for required environment variables
    if "PYPI_TOKEN" not in os.environ:
        raise ValueError("PYPI_TOKEN environment variable is required")

    # Validate OpenAI configuration if AI-powered changelog is enabled
    if config.changelog.ai_powered and "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable is required for AI-powered changelog")

    # Validate version files exist
    for file in config.version_files:
        if not Path(file).exists():
            raise ValueError(f"Version file not found: {file}")


def validate_package(config: Config) -> None:
    """Validate a Python package structure and configuration."""
    # Check for required files
    required_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
    ]
    
    for file in required_files:
        if not Path(file).exists():
            raise ValueError(f"Required file not found: {file}")
    
    # Validate package structure
    if not any(Path().glob("src/*/__init__.py")):
        raise ValueError("No Python package found in src directory")
    
    # Validate test directory
    if not Path("tests").exists():
        raise ValueError("No tests directory found")
    
    # Validate documentation
    if not Path("docs").exists():
        raise ValueError("No documentation directory found") 