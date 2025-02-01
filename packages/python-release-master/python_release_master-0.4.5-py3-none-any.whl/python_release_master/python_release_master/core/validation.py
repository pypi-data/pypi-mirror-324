"""Validation utilities for Python Release Master."""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Set

from python_release_master.core.config import Config

# Maximum file size for code files (10MB)
MAX_CODE_FILE_SIZE = 10 * 1024 * 1024

# Common binary file extensions that should be ignored
BINARY_EXTENSIONS = {
    '.pkl', '.h5', '.parquet', '.feather', '.arrow', '.dat', '.db', '.sqlite',
    '.model', '.bin', '.pt', '.pth', '.onnx', '.mlmodel', '.exe', '.dll', '.so',
    '.dylib', '.zip', '.tar', '.gz', '.rar', '.7z', '.iso'
}

# Common data file extensions
DATA_FILE_EXTENSIONS = {
    '.csv', '.json', '.xlsx', '.xls', '.tsv', '.xml', '.yaml', '.yml'
}

# Directories that should typically be ignored
IGNORED_DIRS = {
    '__pycache__', 'build', 'dist', 'venv', 'env', '.env', '.venv',
    'node_modules', '.git', '.idea', '.vscode', '.tox', '.eggs',
    'data', 'datasets', 'models', 'checkpoints', 'tmp', 'temp'
}

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
    except subprocess.CalledProcessError:
        return set()

def is_binary_file(file_path: str) -> bool:
    """Check if a file is likely to be binary."""
    extension = os.path.splitext(file_path)[1].lower()
    if extension in BINARY_EXTENSIONS:
        return True
    
    # Check first few bytes for null bytes
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except:
        return True

def get_file_issues(file_path: str) -> List[str]:
    """Get list of issues with a file."""
    issues = []
    
    try:
        size = os.path.getsize(file_path)
        if size > MAX_CODE_FILE_SIZE:
            issues.append(f"File is too large ({size / 1024 / 1024:.1f}MB > {MAX_CODE_FILE_SIZE / 1024 / 1024}MB)")
        
        extension = os.path.splitext(file_path)[1].lower()
        if extension in BINARY_EXTENSIONS:
            issues.append(f"Binary file detected (extension: {extension})")
        elif extension in DATA_FILE_EXTENSIONS and size > 1024 * 1024:  # 1MB
            issues.append(f"Large data file detected ({size / 1024 / 1024:.1f}MB)")
        
        if is_binary_file(file_path):
            issues.append("Binary content detected")
    except Exception as e:
        issues.append(f"Error checking file: {str(e)}")
    
    return issues

def validate_repository(root_dir: str = '.') -> Tuple[bool, List[str]]:
    """Validate the repository state.
    
    Args:
        root_dir: Root directory to check
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Get files with changes
    changed_files = get_git_changed_files()
    if not changed_files:
        return True, []  # No changes to validate
    
    # Check files with changes
    for file_path in changed_files:
        abs_path = os.path.join(root_dir, file_path)
        if not os.path.exists(abs_path):
            continue
        
        # Skip ignored directories
        if any(ignored_dir in file_path.split(os.sep) for ignored_dir in IGNORED_DIRS):
            continue
        
        # Check for issues
        file_issues = get_file_issues(abs_path)
        if file_issues:
            issues.append(f"Issues with {file_path}:")
            for issue in file_issues:
                issues.append(f"  - {issue}")
    
    return len(issues) == 0, issues

def validate_environment(config: Config) -> None:
    """Validate the environment before running operations."""
    # Check for required environment variables
    if "PYPI_TOKEN" not in os.environ:
        raise ValueError("PYPI_TOKEN environment variable is required")

    # Validate OpenAI configuration if AI-powered changelog is enabled
    if config.changelog.ai.enabled and "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable is required for AI-powered changelog")

    # Validate version files exist
    for file in config.version.files:
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