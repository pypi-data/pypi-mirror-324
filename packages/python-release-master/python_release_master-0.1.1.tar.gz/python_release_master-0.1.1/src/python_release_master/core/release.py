"""Release management utilities for Python Release Master."""

import re
import subprocess
from pathlib import Path
from typing import List, Optional

from rich.console import Console

from python_release_master.core.ai import generate_changelog_with_ai
from python_release_master.core.config import Config

console = Console()


def create_release(
    bump_type: str,
    title: str,
    description: Optional[str],
    config: Config,
    skip_steps: Optional[List[str]] = None,
) -> None:
    """Create a new release."""
    skip_steps = skip_steps or []
    
    # Update version
    if "version" not in skip_steps:
        bump_version(bump_type, config.version_files)
    
    # Generate changelog
    if "changelog" not in skip_steps:
        changelog = generate_changelog(config)
        if description:
            changelog = f"{description}\n\n{changelog}"
    
    # Build package
    if "build" not in skip_steps:
        build_package()
    
    # Publish to PyPI
    if "publish" not in skip_steps:
        publish_to_pypi()
    
    # Create git tag and release
    if "git" not in skip_steps:
        create_git_release(title, changelog if "changelog" not in skip_steps else description)


def bump_version(bump_type: str, version_files: List[str]) -> None:
    """Bump version in all specified files."""
    console.print(f"Bumping {bump_type} version...")
    
    if bump_type not in ["major", "minor", "patch"]:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    # Get current version
    version = get_current_version(version_files[0])
    major, minor, patch = map(int, version.split("."))
    
    # Calculate new version
    if bump_type == "major":
        new_version = f"{major + 1}.0.0"
    elif bump_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    else:  # patch
        new_version = f"{major}.{minor}.{patch + 1}"
    
    # Update version in all files
    for file in version_files:
        update_version_in_file(file, new_version)
    
    console.print(f"[green]Version bumped to {new_version}[/green]")


def get_current_version(version_file: str) -> str:
    """Extract current version from a file."""
    with open(version_file) as f:
        content = f.read()
    
    # Try different version patterns
    patterns = [
        r'version\s*=\s*["\']([^"\']+)["\']',  # pyproject.toml
        r'__version__\s*=\s*["\']([^"\']+)["\']',  # __init__.py
        r'VERSION\s*=\s*["\']([^"\']+)["\']',  # Other common formats
    ]
    
    for pattern in patterns:
        if match := re.search(pattern, content):
            return match.group(1)
    
    raise ValueError(f"Could not find version in {version_file}")


def update_version_in_file(file_path: str, new_version: str) -> None:
    """Update version string in a file."""
    with open(file_path) as f:
        content = f.read()
    
    # Update version using appropriate pattern
    patterns = {
        r'version\s*=\s*["\']([^"\']+)["\']': f'version = "{new_version}"',
        r'__version__\s*=\s*["\']([^"\']+)["\']': f'__version__ = "{new_version}"',
        r'VERSION\s*=\s*["\']([^"\']+)["\']': f'VERSION = "{new_version}"',
    }
    
    for pattern, replacement in patterns.items():
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            break
    else:
        raise ValueError(f"Could not find version pattern in {file_path}")
    
    with open(file_path, "w") as f:
        f.write(content)


def generate_changelog(config: Config) -> str:
    """Generate changelog using AI if enabled."""
    console.print("Generating changelog...")
    
    if config.changelog.ai_powered:
        try:
            changelog = generate_changelog_with_ai(config.changelog.sections)
            console.print("[green]Changelog generated successfully[/green]")
            return changelog
        except Exception as e:
            console.print(f"[yellow]AI-powered changelog generation failed: {str(e)}[/yellow]")
            console.print("[yellow]Falling back to commit list[/yellow]")
    
    # Fallback to simple commit list
    commits = subprocess.run(
        ["git", "log", "--pretty=format:- %s", "HEAD^..HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    
    return f"## Changes\n\n{commits}"


def build_package() -> None:
    """Build the Python package."""
    console.print("Building package...")
    
    try:
        subprocess.run(
            ["python", "-m", "build"],
            check=True,
            capture_output=True,
            text=True,
        )
        console.print("[green]Package built successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Package build failed:\n{e.stdout}\n{e.stderr}")


def publish_to_pypi() -> None:
    """Publish the package to PyPI."""
    console.print("Publishing to PyPI...")
    
    try:
        subprocess.run(
            ["python", "-m", "twine", "upload", "dist/*"],
            check=True,
            capture_output=True,
            text=True,
            env={"TWINE_USERNAME": "__token__", "TWINE_PASSWORD": "${PYPI_TOKEN}"},
        )
        console.print("[green]Package published successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Package upload failed:\n{e.stdout}\n{e.stderr}")


def create_git_release(title: str, description: Optional[str] = None) -> None:
    """Create a Git tag and release."""
    console.print("Creating Git release...")
    
    try:
        # Create and push tag
        version = get_current_version("pyproject.toml")
        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", title],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "push", "origin", f"v{version}"],
            check=True,
            capture_output=True,
            text=True,
        )
        
        # Create GitHub release if gh CLI is available
        if description:
            try:
                subprocess.run(
                    [
                        "gh", "release", "create",
                        f"v{version}",
                        "--title", title,
                        "--notes", description,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                console.print("[green]GitHub release created successfully[/green]")
            except subprocess.CalledProcessError:
                console.print("[yellow]GitHub CLI not available, skipping release creation[/yellow]")
        
        console.print("[green]Git release created successfully[/green]")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Git release failed:\n{e.stdout}\n{e.stderr}") 