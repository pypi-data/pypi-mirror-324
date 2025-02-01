"""Validation utilities for Python Release Master."""

import logging
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set, Dict

from python_release_master.core.config import Config
from python_release_master.core.templates import (
    PYPROJECT_TOML,
    README_MD,
    LICENSE,
    INIT_PY,
    CLI_PY,
    TEST_BASIC,
)
from python_release_master.core.logger import logger
from python_release_master.core.errors import ReleaseError, ErrorCode

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
        logger.warning(f"Failed to get git changed files: {e}")
        return set()

def create_file_from_template(
    path: Path,
    template: str,
    context: Dict[str, str],
    error_prefix: str
) -> None:
    """Create a file from a template.
    
    Args:
        path: Path to create file at
        template: Template string
        context: Template context
        error_prefix: Prefix for error messages
    
    Raises:
        ReleaseError: If file creation fails
    """
    try:
        content = template.format(**context)
        path.write_text(content)
        logger.debug(f"Created {path}")
    except KeyError as e:
        raise ReleaseError(
            code=ErrorCode.PKG_FILE_INVALID,
            message=f"{error_prefix}: Missing required value {e}",
            context={"file": str(path)},
            fix_instructions=["Check the template context contains all required values"]
        )
    except OSError as e:
        raise ReleaseError(
            code=ErrorCode.SYSTEM_IO_ERROR,
            message=f"{error_prefix}: {e}",
            context={"file": str(path)},
            fix_instructions=["Check file permissions and disk space"],
            cause=e
        )

def ensure_package_structure(config: Config) -> None:
    """Ensure all required files and directories exist.
    
    Args:
        config: Configuration object
    
    Raises:
        ReleaseError: If package structure is invalid
    """
    path = Path(".")
    package_name = config.github.repo_name
    if not package_name:
        raise ReleaseError(
            code=ErrorCode.CONFIG_MISSING_REQUIRED,
            message="Package name not configured",
            fix_instructions=["Set github.repo_name in .release-master.yaml"]
        )
    
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
        create_file_from_template(
            path / "pyproject.toml",
            PYPROJECT_TOML,
            context,
            "Failed to create pyproject.toml"
        )
    
    if not (path / "README.md").exists():
        create_file_from_template(
            path / "README.md",
            README_MD,
            context,
            "Failed to create README.md"
        )
    
    if not (path / "LICENSE").exists():
        create_file_from_template(
            path / "LICENSE",
            LICENSE,
            context,
            "Failed to create LICENSE"
        )
    
    # Create package structure
    pkg_path = path / "src" / context["module_name"]
    try:
        pkg_path.parent.mkdir(exist_ok=True)
        pkg_path.mkdir(exist_ok=True)
        
        # Create __init__.py
        if not (pkg_path / "__init__.py").exists():
            create_file_from_template(
                pkg_path / "__init__.py",
                INIT_PY,
                context,
                "Failed to create __init__.py"
            )
        
        # Create cli.py
        if not (pkg_path / "cli.py").exists():
            create_file_from_template(
                pkg_path / "cli.py",
                CLI_PY,
                context,
                "Failed to create cli.py"
            )
    except OSError as e:
        raise ReleaseError(
            code=ErrorCode.SYSTEM_IO_ERROR,
            message=f"Failed to create package structure: {e}",
            fix_instructions=["Check directory permissions and disk space"],
            cause=e
        )
    
    # Create tests directory
    try:
        (path / "tests").mkdir(exist_ok=True)
        test_init = path / "tests" / "__init__.py"
        test_init.touch(exist_ok=True)
        
        # Create test_basic.py
        if not (path / "tests" / "test_basic.py").exists():
            create_file_from_template(
                path / "tests" / "test_basic.py",
                TEST_BASIC,
                context,
                "Failed to create test_basic.py"
            )
    except OSError as e:
        raise ReleaseError(
            code=ErrorCode.SYSTEM_IO_ERROR,
            message=f"Failed to create tests directory: {e}",
            fix_instructions=["Check directory permissions and disk space"],
            cause=e
        )

def validate_environment(config: Config) -> None:
    """Validate the environment before running operations.
    
    Args:
        config: Configuration object
    
    Raises:
        ReleaseError: If environment validation fails
    """
    errors = []
    
    # Check for required environment variables
    if config.pypi.publish:
        pypi_token = os.environ.get(config.pypi.token_env_var)
        if not pypi_token:
            raise ReleaseError(
                code=ErrorCode.PYPI_TOKEN_MISSING,
                message=f"{config.pypi.token_env_var} environment variable is required for publishing to PyPI",
                context={"env_var": config.pypi.token_env_var}
            )
        # Ensure the token will be available to UV
        if config.pypi.uv_token_env_var not in os.environ and config.pypi.uv_token_env_var != config.pypi.token_env_var:
            os.environ[config.pypi.uv_token_env_var] = pypi_token if pypi_token else ""
    
    # Validate OpenAI configuration if AI-powered changelog is enabled
    if config.changelog.ai.enabled and "OPENAI_API_KEY" not in os.environ:
        raise ReleaseError(
            code=ErrorCode.OPENAI_TOKEN_MISSING,
            message="OPENAI_API_KEY environment variable is required for AI-powered changelog"
        )
    
    # Validate GitHub configuration if auto-create is enabled
    if config.github.auto_create and config.github.token_env_var not in os.environ:
        raise ReleaseError(
            code=ErrorCode.GITHUB_TOKEN_MISSING,
            message=f"{config.github.token_env_var} environment variable is required for GitHub auto-creation",
            context={"env_var": config.github.token_env_var}
        )
    
    # Validate version files exist
    for file in config.version.files:
        if not Path(file).exists():
            raise ReleaseError(
                code=ErrorCode.PKG_FILE_MISSING,
                message=f"Version file not found: {file}",
                context={"file": file},
                fix_instructions=["Create the file or update version.files in config"]
            )

def validate_package(config: Config) -> None:
    """Validate a Python package structure and configuration.
    
    Args:
        config: Configuration object
    
    Raises:
        ReleaseError: If package validation fails
    """
    # Check for required files
    required_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
    ]
    
    for file in required_files:
        if not Path(file).exists():
            raise ReleaseError(
                code=ErrorCode.PKG_FILE_MISSING,
                message=f"Required file not found: {file}",
                context={"file": file},
                fix_instructions=[f"Create {file} file"]
            )
    
    # Validate package structure
    if not any(Path().glob("src/*/__init__.py")):
        raise ReleaseError(
            code=ErrorCode.PKG_STRUCTURE_INVALID,
            message="No Python package found in src directory",
            fix_instructions=["Create package directory in src/ with __init__.py"]
        )
    
    # Validate test directory
    if not Path("tests").exists():
        raise ReleaseError(
            code=ErrorCode.PKG_STRUCTURE_INVALID,
            message="No tests directory found",
            fix_instructions=["Create tests directory"]
        )

def validate_package_structure(config: Config, workspace_dir: Optional[Path] = None) -> None:
    """Validate package structure.
    
    Args:
        config: Configuration object
        workspace_dir: Optional workspace directory path
    
    Raises:
        ReleaseError: If validation fails
    """
    workspace_dir = Path(workspace_dir or os.getcwd())
    
    # Check for required files
    required_files = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "pyproject.toml",
        ".gitignore",
    ]
    
    for file in required_files:
        if not (workspace_dir / file).exists():
            raise ReleaseError(
                code=ErrorCode.PACKAGE_VALIDATION_ERROR,
                message=f"Required file {file} not found",
                fix_instructions=[f"Create {file} in project root"]
            )
    
    # Check for src directory
    src_dir = workspace_dir / "src"
    if not src_dir.exists():
        raise ReleaseError(
            code=ErrorCode.SRC_DIR_NOT_FOUND,
            message="src directory not found",
            fix_instructions=["Create src directory in project root"]
        )
    
    # Check for package directory
    package_name = config.package_name.replace("-", "_")
    package_dir = src_dir / package_name
    if not package_dir.exists():
        raise ReleaseError(
            code=ErrorCode.PACKAGE_DIR_NOT_FOUND,
            message=f"Package directory {package_name} not found in src/",
            fix_instructions=[f"Create src/{package_name} directory"]
        )
    
    # Check for __init__.py
    init_file = package_dir / "__init__.py"
    if not init_file.exists():
        raise ReleaseError(
            code=ErrorCode.INIT_PY_NOT_FOUND,
            message=f"__init__.py not found in {package_dir}",
            fix_instructions=[f"Create {init_file} file"]
        ) 