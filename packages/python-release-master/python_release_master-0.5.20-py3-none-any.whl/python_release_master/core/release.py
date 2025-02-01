"""Release management for Python packages."""

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from python_release_master.core.ai_utils import (
    analyze_changes_for_version_bump,
    generate_changelog_with_ai,
    generate_release_title,
)
from python_release_master.core.config import Config, load_config
from python_release_master.core.changelog import generate_changelog
from python_release_master.core.validation import (
    validate_environment,
    ensure_package_structure,
    validate_package,
)
from python_release_master.core.logger import logger
from python_release_master.core.errors import ErrorCode, ReleaseError
from python_release_master.core.validation_manager import ValidationManager
from python_release_master.core.version_manager import VersionManager
from python_release_master.core.git import GitManager

def create_github_repository(config: Config) -> None:
    """Create GitHub repository if it doesn't exist.
    
    Args:
        config: Configuration object
    
    Raises:
        ReleaseError: If repository creation fails
    """
    if not config.github.auto_create:
        return
    
    token = os.environ.get(config.github.token_env_var)
    if not token:
        raise ReleaseError(
            code=ErrorCode.GITHUB_TOKEN_MISSING,
            message=f"GitHub token not found in environment variable {config.github.token_env_var}",
            context={"env_var": config.github.token_env_var}
        )
    
    try:
        logger.start_operation("Checking GitHub repository...")
        cmd = ["gh", "repo", "view", f"{config.github.repo_name}"]
        logger.command(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.success(f"Repository {config.github.repo_name} already exists")
            return
        
        logger.start_operation("Creating GitHub repository...")
        cmd = ["gh", "repo", "create", config.github.repo_name]
        if config.github.private:
            cmd.append("--private")
        else:
            cmd.append("--public")
        
        if config.github.description:
            cmd.extend(["--description", config.github.description])
        
        logger.command(cmd)
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"Created repository {config.github.repo_name}")
        
        logger.start_operation("Initializing Git repository...")
        if not Path(".git").exists():
            cmds = [
                ["git", "init"],
                ["git", "add", "."],
                ["git", "commit", "-m", "Initial commit"],
                ["git", "branch", "-M", "main"],
                ["git", "remote", "add", "origin", f"https://github.com/{config.github.owner}/{config.github.repo_name}.git"],
                ["git", "push", "-u", "origin", "main"]
            ]
            for cmd in cmds:
                logger.command(cmd)
                subprocess.run(cmd, check=True)
            logger.success("Initialized Git repository and pushed initial commit")
    
    except subprocess.CalledProcessError as e:
        raise ReleaseError(
            code=ErrorCode.GITHUB_REPO_CREATE_ERROR,
            message=f"Failed to create GitHub repository: {e.stdout}\n{e.stderr}",
            fix_instructions=["Check GitHub token permissions and repository name availability"],
            cause=e
        )
    except Exception as e:
        raise ReleaseError(
            code=ErrorCode.GITHUB_API_ERROR,
            message=f"Unexpected error creating GitHub repository: {e}",
            fix_instructions=["Please report this issue with the full error message"],
            cause=e
        )

def create_release(config: Config) -> None:
    """Create a new release.
    
    Args:
        config: Configuration object
        
    Raises:
        ReleaseError: If release creation fails
    """
    try:
        # Step 1: Validate environment
        logger.start_operation("Validating environment...")
        validation_manager = ValidationManager(config)
        validation_manager.validate_environment()
        
        # Step 2: Analyze changes and suggest version bump
        logger.start_operation("Analyzing changes...")
        version_manager = VersionManager(Path.cwd())
        current_version = version_manager.get_current_versions()["pyproject.toml"]
        new_version = version_manager.suggest_version_bump("patch")  # Default to patch bump
        
        # Step 3: Generate changelog
        logger.start_operation("Generating changelog...")
        changelog_content = generate_changelog(config)
        
        # Step 4: Update version files
        logger.start_operation("Updating version files...")
        version_manager.bump_version(new_version)
        
        # Step 5: Build package
        logger.start_operation("Building package...")
        cmd = ["uv", "build", "--no-sources"]
        logger.command(cmd)
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.success("Package built successfully")
        
        # Step 6: Create Git tag and release
        logger.start_operation("Creating Git tag and release...")
        git_manager = GitManager(Path.cwd())
        
        # Generate release title
        title = generate_release_title(changelog_content)
        
        # Create tag and release
        git_manager.create_tag(f"v{new_version}", title)
        if config.git.push:
            git_manager.push_changes(tags=True)
        
        if config.git.release.enabled:
            git_manager.create_release(
                tag=f"v{new_version}",
                title=title,
                description=changelog_content,
                draft=config.git.release.draft,
                prerelease=config.git.release.prerelease,
                generate_notes=config.git.release.generate_notes
            )
        
        logger.success(f"Successfully created release v{new_version}")
        
    except ReleaseError as e:
        logger.error(f"Release creation failed: {e.message}")
        if e.fix_instructions:
            for instruction in e.fix_instructions:
                logger.error(f"- {instruction}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during release: {str(e)}")
        raise ReleaseError(
            code=ErrorCode.UNKNOWN_ERROR,
            message=f"Unexpected error during release: {str(e)}",
            cause=e
        )

def publish_package(config: Config) -> None:
    """Publish package to PyPI using uv.
    
    Args:
        config: Configuration object
    
    Raises:
        ReleaseError: If publish fails
    """
    # Get PyPI token
    pypi_token = os.environ.get(config.pypi.token_env_var)
    if not pypi_token:
        raise ReleaseError(
            code=ErrorCode.PYPI_AUTH_FAILED,
            message=f"PyPI token not found in environment variable {config.pypi.token_env_var}",
            context={"env_var": config.pypi.token_env_var}
        )
    
    # Publish package
    try:
        cmd = ["uv", "publish"]
        env = {
            **os.environ,
            config.pypi.uv_token_env_var: pypi_token  # Use the configured UV token env var
        }
        logger.command(cmd, {config.pypi.uv_token_env_var: "***"})
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        logger.success("Package published successfully")
    except subprocess.CalledProcessError as e:
        error_output = e.stdout or e.stderr or str(e)
        
        # Check for metadata version issues
        if "metadata version" in error_output.lower():
            raise ReleaseError(
                code=ErrorCode.PYPI_VALIDATION_ERROR,
                message=f"Failed to publish package due to metadata version incompatibility:\n{error_output}",
                context={"command": " ".join(cmd), "exit_code": e.returncode}
            )
        
        # Other publish errors
        raise ReleaseError(
            code=ErrorCode.PYPI_UPLOAD_FAILED,
            message=f"Failed to publish package:\n{error_output}",
            context={"command": " ".join(cmd), "exit_code": e.returncode}
        )

def bump_version(bump_type: str) -> str:
    """Bump the version number.
    
    Args:
        bump_type: Type of version bump (major, minor, patch)
    
    Returns:
        str: New version number
    
    Raises:
        ReleaseError: If version bump fails
    """
    try:
        # Get current version from pyproject.toml
        with open("pyproject.toml", "r") as f:
            content = f.read()
            match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
            if not match:
                raise ReleaseError(
                    ErrorCode.VERSION_NOT_FOUND,
                    "Version not found in pyproject.toml"
                )
            current_version = match.group(1)
        
        # Parse version and bump
        major, minor, patch = map(int, current_version.split("."))
        if bump_type == "major":
            new_version = f"{major + 1}.0.0"
        elif bump_type == "minor":
            new_version = f"{major}.{minor + 1}.0"
        else:  # patch
            new_version = f"{major}.{minor}.{patch + 1}"
        
        # Update version in pyproject.toml
        with open("pyproject.toml", "r") as f:
            content = f.read()
        
        new_content = content.replace(f'version = "{current_version}"', f'version = "{new_version}"')
        
        with open("pyproject.toml", "w") as f:
            f.write(new_content)
        
        logger.success("Updated version in pyproject.toml")
        
        # Clean dist directory and rebuild with new version
        clean_dist()
        validate_package(load_config())
        
        return new_version
    except Exception as e:
        if not isinstance(e, ReleaseError):
            raise ReleaseError(
                ErrorCode.VERSION_BUMP_FAILED,
                str(e)
            ) from e
        raise e

def get_current_version(version_file: str) -> str:
    """Get current version from file.
    
    Args:
        version_file: Path to file containing version string
    
    Returns:
        Current version string
    
    Raises:
        ReleaseError: If version cannot be determined
    """
    try:
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
        
        raise ReleaseError(
            code=ErrorCode.VERSION_NOT_FOUND,
            message=f"Could not find version string in {version_file}",
            context={"file": version_file}
        )
    except Exception as e:
        raise ReleaseError(
            code=ErrorCode.VERSION_NOT_FOUND,
            message=f"Error reading version from {version_file}: {e}",
            context={"file": version_file},
            cause=e
        )

def update_version_in_file(file: str, old_version: str, new_version: str) -> None:
    """Update version string in file.
    
    Args:
        file: Path to file
        old_version: Current version string
        new_version: New version string
    
    Raises:
        ReleaseError: If version update fails
    """
    try:
        with open(file) as f:
            content = f.read()
        
        # Replace version string
        new_content = content.replace(old_version, new_version)
        
        with open(file, "w") as f:
            f.write(new_content)
    except Exception as e:
        raise ReleaseError(
            code=ErrorCode.VERSION_UPDATE_FAILED,
            message=f"Error updating version in {file}: {e}",
            context={"file": file, "old_version": old_version, "new_version": new_version},
            cause=e
        )

def clean_dist() -> None:
    """Clean the dist directory.
    
    This removes all build artifacts from previous builds to ensure a clean state.
    
    Raises:
        ReleaseError: If cleaning fails
    """
    dist_dir = Path("dist")
    
    try:
        # Remove the entire dist directory if it exists
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        # Create a fresh dist directory
        dist_dir.mkdir(exist_ok=True)
        logger.success("Cleaned dist directory")
    except Exception as e:
        raise ReleaseError(
            ErrorCode.BUILD_FAILED,
            f"Failed to clean dist directory: {e}",
            context={"directory": str(dist_dir)}
        )

def create_git_release(version: str, title: str, description: str, config: Config) -> None:
    """Create Git release.
    
    Args:
        version: Release version
        title: Release title
        description: Release description
        config: Configuration object
    
    Raises:
        ReleaseError: If release creation fails
    """
    try:
        # Push changes first
        if config.git.push:
            cmd = ["git", "push", "origin", "HEAD"]
            logger.command(cmd)
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success("Pushed changes to remote")
        
        # Tag release
        tag_name = f"{config.git.tag_prefix}{version}"
        cmd = ["git", "tag", "-a", tag_name, "-m", title]
        logger.command(cmd)
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.success(f"Created Git tag {tag_name}")
        
        # Push tag
        if config.git.push:
            cmd = ["git", "push", "origin", tag_name]
            logger.command(cmd)
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success(f"Pushed Git tag {tag_name}")
        
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
            
            logger.command(cmd)
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success("GitHub release created successfully")
    
    except subprocess.CalledProcessError as e:
        raise ReleaseError(
            code=ErrorCode.GIT_RELEASE_FAILED,
            message=f"Failed to create Git release:\n{e.stdout}\n{e.stderr}",
            context={"command": " ".join(e.cmd), "exit_code": e.returncode}
        )

def analyze_changes() -> str:
    """Analyze changes to determine version bump type.
    
    Returns:
        Version bump type (major, minor, patch)
    """
    logger.start_operation("Analyzing changes for version bump...")
    
    # For now, default to patch
    # TODO: Implement AI-powered analysis of changes
    bump_type = "patch"
    
    logger.success(f"Determined version bump type: {bump_type}")
    return bump_type