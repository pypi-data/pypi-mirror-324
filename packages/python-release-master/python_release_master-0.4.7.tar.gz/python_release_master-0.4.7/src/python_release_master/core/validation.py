"""Validation utilities for Python Release Master."""

import logging
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set, Dict

from rich.console import Console

from python_release_master.core.config import Config
from python_release_master.core.templates import (
    PYPROJECT_TOML,
    README_MD,
    LICENSE,
    INIT_PY,
    CLI_PY,
    TEST_BASIC,
)

log = logging.getLogger(__name__)
console = Console()

@dataclass
class ValidationError:
    """Validation error details."""
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    fix_instructions: Optional[str] = None

    def __str__(self) -> str:
        """Format error message."""
        parts = [self.message]
        if self.file:
            parts.append(f"File: {self.file}")
        if self.line:
            parts.append(f"Line: {self.line}")
        if self.fix_instructions:
            parts.append(f"\nTo fix: {self.fix_instructions}")
        return "\n".join(parts)

def get_git_changed_files() -> Set[str]:
    """Get list of files that have changes in git."""
    try:
        # Get staged files
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, check=True
        ).stdout.splitlines()
        
        # Get unstaged files
        unstaged = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True, check=True
        ).stdout.splitlines()
        
        # Get untracked files
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True
        ).stdout.splitlines()
        
        return set(staged + unstaged + untracked)
    except subprocess.CalledProcessError as e:
        log.warning("Failed to get git changed files: %s", e)
        return set()

def create_file_from_template(
    path: Path,
    template: str,
    context: Dict[str, str],
    error_prefix: str
) -> Optional[ValidationError]:
    """Create a file from a template.
    
    Args:
        path: Path to create file at
        template: Template string
        context: Template context
        error_prefix: Prefix for error messages
    
    Returns:
        ValidationError if creation failed, None otherwise
    """
    try:
        content = template.format(**context)
        path.write_text(content)
        log.debug("Created %s", path)
        return None
    except KeyError as e:
        return ValidationError(
            f"{error_prefix}: Missing required value {e}",
            str(path),
            fix_instructions="Check the template context contains all required values"
        )
    except OSError as e:
        return ValidationError(
            f"{error_prefix}: {e}",
            str(path),
            fix_instructions="Check file permissions and disk space"
        )

def ensure_package_structure(config: Config) -> List[ValidationError]:
    """Ensure all required files and directories exist.
    
    Args:
        config: Configuration object
    
    Returns:
        List of validation errors
    """
    errors = []
    path = Path(".")
    package_name = config.github.repo_name
    if not package_name:
        return [ValidationError(
            "Package name not configured",
            fix_instructions="Set github.repo_name in .release-master.yaml"
        )]
    
    # Prepare template context
    context = {
        "package_name": package_name,
        "module_name": package_name.replace("-", "_"),
        "title": package_name.replace("-", " ").title(),
        "description": config.github.description or f"Python package for {package_name.replace('-', ' ').title()}",
        "version": "0.1.0",
        "year": datetime.now().year,
        "owner": config.github.owner or "your-username",
        "cli_name": package_name.replace("-", "-"),
    }
    
    # Create required files
    if not (path / "pyproject.toml").exists():
        if error := create_file_from_template(
            path / "pyproject.toml",
            PYPROJECT_TOML,
            context,
            "Failed to create pyproject.toml"
        ):
            errors.append(error)
    
    if not (path / "README.md").exists():
        if error := create_file_from_template(
            path / "README.md",
            README_MD,
            context,
            "Failed to create README.md"
        ):
            errors.append(error)
    
    if not (path / "LICENSE").exists():
        if error := create_file_from_template(
            path / "LICENSE",
            LICENSE,
            context,
            "Failed to create LICENSE"
        ):
            errors.append(error)
    
    # Create package structure
    pkg_path = path / "src" / context["module_name"]
    try:
        pkg_path.parent.mkdir(exist_ok=True)
        pkg_path.mkdir(exist_ok=True)
        
        # Create __init__.py
        if not (pkg_path / "__init__.py").exists():
            if error := create_file_from_template(
                pkg_path / "__init__.py",
                INIT_PY,
                context,
                "Failed to create __init__.py"
            ):
                errors.append(error)
        
        # Create cli.py
        if not (pkg_path / "cli.py").exists():
            if error := create_file_from_template(
                pkg_path / "cli.py",
                CLI_PY,
                context,
                "Failed to create cli.py"
            ):
                errors.append(error)
    except OSError as e:
        errors.append(ValidationError(
            f"Failed to create package structure: {e}",
            fix_instructions="Check directory permissions and disk space"
        ))
    
    # Create tests directory
    try:
        (path / "tests").mkdir(exist_ok=True)
        test_init = path / "tests" / "__init__.py"
        test_init.touch(exist_ok=True)
        
        # Create test_basic.py
        if not (path / "tests" / "test_basic.py").exists():
            if error := create_file_from_template(
                path / "tests" / "test_basic.py",
                TEST_BASIC,
                context,
                "Failed to create test_basic.py"
            ):
                errors.append(error)
    except OSError as e:
        errors.append(ValidationError(
            f"Failed to create tests directory: {e}",
            fix_instructions="Check directory permissions and disk space"
        ))
    
    return errors

def validate_environment(config: Config) -> List[ValidationError]:
    """Validate the environment before running operations.
    
    Args:
        config: Configuration object
    
    Returns:
        List of validation errors
    """
    errors = []
    
    # Check for required environment variables
    if "PYPI_TOKEN" not in os.environ:
        errors.append(ValidationError(
            "PYPI_TOKEN environment variable is required",
            fix_instructions="Set PYPI_TOKEN environment variable with your PyPI API token"
        ))
    
    # Validate OpenAI configuration if AI-powered changelog is enabled
    if config.changelog.ai.enabled and "OPENAI_API_KEY" not in os.environ:
        errors.append(ValidationError(
            "OPENAI_API_KEY environment variable is required for AI-powered changelog",
            fix_instructions="Set OPENAI_API_KEY environment variable or disable AI-powered changelog in config"
        ))
    
    # Validate GitHub configuration if auto-create is enabled
    if config.github.auto_create and "GITHUB_TOKEN" not in os.environ:
        errors.append(ValidationError(
            "GITHUB_TOKEN environment variable is required for GitHub auto-creation",
            fix_instructions="Set GITHUB_TOKEN environment variable or disable GitHub auto-creation in config"
        ))
    
    # Validate version files exist
    for file in config.version.files:
        if not Path(file).exists():
            errors.append(ValidationError(
                f"Version file not found: {file}",
                file,
                fix_instructions="Create the file or update version.files in config"
            ))
    
    return errors

def validate_package(config: Config) -> List[ValidationError]:
    """Validate a Python package structure and configuration.
    
    Args:
        config: Configuration object
    
    Returns:
        List of validation errors
    """
    errors = []
    
    # Check for required files
    required_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
    ]
    
    for file in required_files:
        if not Path(file).exists():
            errors.append(ValidationError(
                f"Required file not found: {file}",
                file,
                fix_instructions=f"Create {file} file"
            ))
    
    # Validate package structure
    if not any(Path().glob("src/*/__init__.py")):
        errors.append(ValidationError(
            "No Python package found in src directory",
            fix_instructions="Create package directory in src/ with __init__.py"
        ))
    
    # Validate test directory
    if not Path("tests").exists():
        errors.append(ValidationError(
            "No tests directory found",
            fix_instructions="Create tests directory"
        ))
    
    return errors 