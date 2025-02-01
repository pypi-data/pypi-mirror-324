"""Release management utilities for Python Release Master."""

import logging
import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.status import Status

from python_release_master.core.config import Config
from python_release_master.core.changelog import generate_changelog
from python_release_master.core.validation import (
    validate_environment,
    ensure_package_structure,
    validate_package,
    ValidationError
)
from python_release_master.core.ai_utils import (
    analyze_changes_for_version_bump,
    generate_release_title,
    generate_changelog_with_ai,
)

log = logging.getLogger(__name__)
console = Console()

def handle_validation_errors(errors: List[ValidationError], context: str) -> None:
    """Handle validation errors by displaying them and optionally exiting.
    
    Args:
        errors: List of validation errors
        context: Context where the errors occurred
    """
    if not errors:
        return
    
    console.print(Panel(
        "\n".join([str(error) for error in errors]),
        title=f"[red]❌ {context} Failed[/red]",
        border_style="red"
    ))
    raise SystemExit(1)

def create_github_repository(config: Config) -> None:
    """Create GitHub repository if it doesn't exist.
    
    Args:
        config: Configuration object
    """
    if not config.github.auto_create:
        return
    
    token = os.environ.get(config.github.token_env_var)
    if not token:
        handle_validation_errors(
            [ValidationError(
                f"GitHub token not found in environment variable {config.github.token_env_var}",
                fix_instructions=f"Set {config.github.token_env_var} environment variable with your GitHub token"
            )],
            "GitHub Repository Creation"
        )
    
    try:
        with Status("[bold yellow]Checking GitHub repository..."):
            # Check if repository exists
            result = subprocess.run(
                ["gh", "repo", "view", f"{config.github.repo_name}"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log.info("Repository %s already exists", config.github.repo_name)
                return
        
        with Status("[bold yellow]Creating GitHub repository..."):
            # Create repository
            cmd = ["gh", "repo", "create", config.github.repo_name]
            if config.github.private:
                cmd.append("--private")
            else:
                cmd.append("--public")
            
            if config.github.description:
                cmd.extend(["--description", config.github.description])
            
            subprocess.run(cmd, check=True, capture_output=True)
            log.info("Created repository %s", config.github.repo_name)
        
        with Status("[bold yellow]Initializing Git repository..."):
            # Initialize git if needed
            if not Path(".git").exists():
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    check=True
                )
                subprocess.run(
                    ["git", "branch", "-M", "main"],
                    check=True
                )
                subprocess.run(
                    ["git", "remote", "add", "origin", f"https://github.com/{config.github.owner}/{config.github.repo_name}.git"],
                    check=True
                )
                subprocess.run(
                    ["git", "push", "-u", "origin", "main"],
                    check=True
                )
                log.info("Initialized Git repository and pushed initial commit")
    
    except subprocess.CalledProcessError as e:
        handle_validation_errors(
            [ValidationError(
                f"Failed to create GitHub repository: {e.stdout}\n{e.stderr}",
                fix_instructions="Check GitHub token permissions and repository name availability"
            )],
            "GitHub Repository Creation"
        )
    except Exception as e:
        handle_validation_errors(
            [ValidationError(
                f"Unexpected error creating GitHub repository: {e}",
                fix_instructions="Please report this issue with the full error message"
            )],
            "GitHub Repository Creation"
        )

def create_release(config: Config) -> None:
    """Create a new release.
    
    Args:
        config: Configuration object
    """
    try:
        # Validate environment and ensure package structure
        with Status("[bold yellow]Validating environment..."):
            errors = validate_environment(config)
            handle_validation_errors(errors, "Environment Validation")
        
        with Status("[bold yellow]Validating package structure..."):
            errors = validate_package(config)
            handle_validation_errors(errors, "Package Validation")
            
            errors = ensure_package_structure(config)
            handle_validation_errors(errors, "Package Structure Creation")
        
        # Create GitHub repository if needed
        create_github_repository(config)
        
        # Analyze changes and determine version bump
        with Status("[bold yellow]Analyzing changes for version bump..."):
            bump_type = analyze_changes_for_version_bump(
                model=config.changelog.ai.model,
                temperature=config.changelog.ai.temperature
            )
            log.info("Determined version bump type: %s", bump_type)
        
        # Bump version
        with Status("[bold yellow]Bumping version..."):
            bump_version(bump_type, config.version.files)
            version = get_current_version(config.version.files[0])
            log.info("Bumped version to %s", version)
        
        # Generate changelog
        with Status("[bold yellow]Generating changelog..."):
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
                log.warning("Error generating changelog: %s", e)
                log.warning("Falling back to manual changelog generation")
                changelog_text = generate_changelog(config.changelog.sections, False)
        
        # Generate release title
        with Status("[bold yellow]Generating release title..."):
            title = generate_release_title(
                version,
                changelog_text,
                model=config.changelog.ai.model,
                temperature=config.changelog.ai.temperature
            )
            log.info("Generated release title: %s", title)
        
        # Clean dist directory
        with Status("[bold yellow]Cleaning dist directory..."):
            clean_dist()
        
        # Build and publish package
        if config.pypi.publish:
            with Status("[bold yellow]Building and publishing package..."):
                build_and_publish_package()
        
        # Create Git release
        if config.git.release.enabled:
            with Status("[bold yellow]Creating Git release..."):
                create_git_release(version, title, changelog_text, config)
        
        console.print(Panel(
            f"[green]✓ Successfully created release {version}[/green]\n\n"
            f"Title: {title}\n\n"
            f"Changelog:\n{changelog_text}",
            title="[green]Release Complete[/green]",
            border_style="green"
        ))
    
    except Exception as e:
        handle_validation_errors(
            [ValidationError(
                f"Unexpected error during release: {e}",
                fix_instructions="Please report this issue with the full error message and logs"
            )],
            "Release Creation"
        )

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


def clean_dist() -> None:
    """Clean the dist directory."""
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            file.unlink()


def build_and_publish_package() -> None:
    """Build and publish package using uv."""
    console.print("Building and publishing package...")
    
    # Build package
    try:
        subprocess.run(
            ["uv", "build", "--no-sources"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to build package:\n{e.stdout}\n{e.stderr}")
    
    # Publish package
    try:
        subprocess.run(
            ["uv", "publish"],
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "UV_PUBLISH_TOKEN": os.environ.get("PYPI_TOKEN", "")
            }
        )
        console.print("Package published successfully")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to publish package:\n{e.stdout}\n{e.stderr}")


def create_git_release(version: str, title: str, description: str, config: Config) -> None:
    """Create Git release.
    
    Args:
        version: Release version
        title: Release title
        description: Release description
        config: Configuration object
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
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create Git release:\n{e.stdout}\n{e.stderr}")