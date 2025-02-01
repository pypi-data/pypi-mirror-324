"""Release management utilities for Python Release Master."""

import re
import subprocess
import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from rich.console import Console

from python_release_master.core.config import Config
from python_release_master.core.changelog import generate_changelog
from python_release_master.core.verification import verify_current_package
from python_release_master.core.validation import validate_environment
from python_release_master.core.ai_utils import (
    analyze_changes_for_version_bump,
    generate_release_title,
    generate_changelog_with_ai,
)

console = Console()


def create_release(config: Config) -> None:
    """Create a new release.
    
    Args:
        config: Configuration object
    """
    # Validate environment
    validate_environment(config)
    
    # Analyze changes and determine version bump
    bump_type = analyze_changes_for_version_bump(
        model=config.changelog.ai.model,
        temperature=config.changelog.ai.temperature
    )
    
    # Bump version
    bump_version(bump_type, config.version.files)
    version = get_current_version(config.version.files[0])
    
    # Generate changelog
    try:
        if config.changelog.ai.enabled:
            changelog_text = generate_changelog_with_ai(
                model=config.changelog.ai.model,
                temperature=config.changelog.ai.temperature,
                sections=config.changelog.sections
            )
        else:
            changelog_text = generate_changelog(config.changelog.sections, False)
    except Exception as e:
        console.print(f"[yellow]Error generating changelog: {e}[/yellow]")
        console.print("[yellow]Falling back to manual changelog generation[/yellow]")
        changelog_text = generate_changelog(config.changelog.sections, False)
    
    # Generate release title
    title = generate_release_title(
        version,
        changelog_text,
        model=config.changelog.ai.model,
        temperature=config.changelog.ai.temperature
    )
    
    # Build package
    success, message = build_package()
    if not success:
        raise RuntimeError(f"Failed to build package: {message}")
    
    # Run tests in Docker
    if config.testing.run_before_release:
        success, message = verify_current_package()
        if not success:
            raise RuntimeError(f"Package verification failed: {message}")
    
    # Publish to PyPI
    if config.pypi.publish:
        success, message = publish_to_pypi(config)
        if not success:
            raise RuntimeError(f"Failed to publish package: {message}")
    
    # Create Git release
    if config.git.release.enabled:
        success, message = create_git_release(version, title, changelog_text, config)
        if not success:
            raise RuntimeError(f"Failed to create Git release: {message}")


def bump_version(bump_type: str, version_files: List[str]) -> None:
    """Bump version in specified files.
    
    Args:
        bump_type: Type of version bump (major, minor, patch)
        version_files: List of files containing version strings
    """
    current_version = get_current_version(version_files[0])
    if not current_version:
        raise ValueError("Could not determine current version")
    
    # Parse version components
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", current_version)
    if not match:
        raise ValueError(f"Invalid version format: {current_version}")
    
    major, minor, patch = map(int, match.groups())
    
    # Calculate new version
    if bump_type == "major":
        new_version = f"{major + 1}.0.0"
    elif bump_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    # Update version in files
    for file in version_files:
        update_version_in_file(file, current_version, new_version)


def get_current_version(version_file: str) -> str:
    """Get current version from file.
    
    Args:
        version_file: Path to file containing version string
    
    Returns:
        Current version string
    """
    with open(version_file) as f:
        content = f.read()
    
    # Try to find version string
    version_patterns = [
        r'version\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # Python version string
        r'"version":\s*"(\d+\.\d+\.\d+)"',  # JSON version string
        r'version:\s*(\d+\.\d+\.\d+)',  # YAML version string
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not find version string in {version_file}")


def update_version_in_file(file: str, old_version: str, new_version: str) -> None:
    """Update version string in file.
    
    Args:
        file: Path to file
        old_version: Current version string
        new_version: New version string
    """
    with open(file) as f:
        content = f.read()
    
    # Replace version string
    new_content = content.replace(old_version, new_version)
    
    with open(file, "w") as f:
        f.write(new_content)


def build_package() -> Tuple[bool, str]:
    """Build Python package.
    
    Returns:
        Tuple of (success, message)
    """
    console.print("Building package...")
    try:
        subprocess.run(
            ["python", "-m", "build"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Verify dist files exist
        dist_dir = Path("dist")
        if not dist_dir.exists() or not any(dist_dir.iterdir()):
            return False, "No distribution files found after build"
        
        console.print("Package built successfully")
        return True, "Package built successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Package build failed:\n{e.stdout}\n{e.stderr}"


def publish_to_pypi(config: Config) -> Tuple[bool, str]:
    """Publish package to PyPI.
    
    Args:
        config: Configuration object
    
    Returns:
        Tuple of (success, message)
    """
    console.print("Publishing to PyPI...")
    try:
        # Check for PyPI token
        if "PYPI_TOKEN" not in os.environ:
            return False, "PYPI_TOKEN environment variable not set"
        
        # Check for dist files
        dist_dir = Path("dist")
        if not dist_dir.exists() or not any(dist_dir.iterdir()):
            return False, "No distribution files found"
        
        # Upload to PyPI
        cmd = ["python", "-m", "twine", "upload", "dist/*"]
        if config.pypi.repository == "testpypi":
            cmd.extend(["--repository", "testpypi"])
        
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "TWINE_USERNAME": "__token__",
                "TWINE_PASSWORD": os.environ["PYPI_TOKEN"]
            }
        )
        
        console.print("Package published successfully")
        return True, "Package published successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Package upload failed:\n{e.stdout}\n{e.stderr}"


def create_git_release(version: str, title: str, description: str, config: Config) -> Tuple[bool, str]:
    """Create Git release.
    
    Args:
        version: Release version
        title: Release title
        description: Release description
        config: Configuration object
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Tag release
        tag_name = f"{config.git.tag_prefix}{version}"
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", title],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Push tag
        if config.git.push:
            subprocess.run(
                ["git", "push", "origin", tag_name],
                check=True,
                capture_output=True,
                text=True
            )
        
        # Create GitHub release if configured
        if config.github.auto_create:
            cmd = [
                "gh", "release", "create",
                tag_name,
                "--title", title,
                "--notes", description,
            ]
            
            if config.git.release.draft:
                cmd.append("--draft")
            if config.git.release.prerelease:
                cmd.append("--prerelease")
            if config.git.release.generate_notes:
                cmd.append("--generate-notes")
            
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        
        console.print("Git release created successfully")
        return True, "Git release created successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Git release failed:\n{e.stdout}\n{e.stderr}"