"""Validation functionality for python-release-master."""
import os
import subprocess
from typing import List, Dict, Any, Optional

from . import version
from .config import Config

def validate_environment(config: Config) -> None:
    """Validate environment variables and dependencies."""
    # Check PyPI token
    if not os.getenv("PYPI_TOKEN"):
        raise ValueError("PYPI_TOKEN environment variable is required")

    # Check OpenAI API key if AI-powered changelog is enabled
    if config.changelog.ai_powered and not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required for AI-powered changelog")

    # Check version files exist
    for version_file in config.version_files:
        if not os.path.exists(version_file):
            raise ValueError("Version file not found")

def validate_package(config: Config) -> None:
    """Validate package structure and required files."""
    package_dir = "."

    # Check required files
    required_files = ["pyproject.toml", "README.md", "LICENSE"]
    for file in required_files:
        if not os.path.exists(os.path.join(package_dir, file)):
            raise ValueError("Required file not found")

    # Check src directory
    src_dir = os.path.join(package_dir, "src")
    if not os.path.exists(src_dir) or not any(
        os.path.isdir(os.path.join(src_dir, d)) for d in os.listdir(src_dir)
    ):
        raise ValueError("No Python package found in src directory")

    # Check tests directory
    if not os.path.exists(os.path.join(package_dir, "tests")):
        raise ValueError("No tests directory found")

    # Check docs directory
    if not os.path.exists(os.path.join(package_dir, "docs")):
        raise ValueError("No documentation directory found")

def validate_git_status() -> Dict[str, bool]:
    """Validate git repository status."""
    results = {
        "is_git_repo": False,
        "clean_working_tree": False,
        "has_remote": False,
    }
    
    try:
        # Check if it's a git repo
        subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=True)
        results["is_git_repo"] = True
        
        # Check for uncommitted changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        results["clean_working_tree"] = not bool(status.stdout.strip())
        
        # Check for remote
        remotes = subprocess.run(["git", "remote"], capture_output=True, text=True, check=True)
        results["has_remote"] = bool(remotes.stdout.strip())
        
    except subprocess.CalledProcessError:
        pass
    
    return results 