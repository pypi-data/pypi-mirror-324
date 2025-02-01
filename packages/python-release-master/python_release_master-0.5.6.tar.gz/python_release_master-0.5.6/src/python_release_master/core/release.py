"""Release management utilities for Python Release Master."""

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from python_release_master.core.config import Config
from python_release_master.core.changelog import generate_changelog
from python_release_master.core.validation import validate_environment, ensure_package_structure, validate_package
from python_release_master.core.ai_utils import (
    analyze_changes_for_version_bump,
    generate_release_title,
    generate_changelog_with_ai,
)
from python_release_master.core.logger import logger
from python_release_master.core.errors import ReleaseError, ErrorCode
from python_release_master.core.validation_manager import ValidationManager

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

def create_release(config: Config, workspace_dir: Optional[Path] = None) -> None:
    """Create a new release.
    
    Args:
        config: Configuration object
        workspace_dir: Optional workspace directory path
    
    Raises:
        ReleaseError: If release creation fails
    """
    workspace_dir = Path(workspace_dir or os.getcwd())
    
    try:
        # Initialize validation manager
        validator = ValidationManager(config, workspace_dir)
        
        # Step 1: Run all validation checks
        validator.validate_all()
        
        # Step 2: Clean dist directory and validate build
        logger.start_operation("Cleaning dist directory...")
        clean_dist()
        logger.success("Cleaned dist directory")
        
        logger.start_operation("Validating package build...")
        try:
            cmd = ["uv", "build", "--no-sources"]
            logger.command(cmd)
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success("Package build validation passed")
        except subprocess.CalledProcessError as e:
            raise ReleaseError(
                code=ErrorCode.BUILD_FAILED,
                message=f"Package build validation failed:\n{e.stdout}\n{e.stderr}",
                context={"command": " ".join(cmd), "exit_code": e.returncode}
            )
        
        # Step 3: Create GitHub repository if needed
        create_github_repository(config)
        
        # Step 4: Analyze changes and determine version bump
        logger.start_operation("Analyzing changes for version bump...")
        logger.api_call("OpenAI", "chat/completions", {
            "model": config.changelog.ai.model,
            "temperature": config.changelog.ai.temperature,
            "messages": [{"role": "system", "content": "Analyze git changes for version bump"}]
        })
        bump_type = analyze_changes_for_version_bump(
            model=config.changelog.ai.model,
            temperature=config.changelog.ai.temperature
        )
        logger.success(f"Determined version bump type: {bump_type}")
        
        # Step 5: Bump version
        logger.start_operation("Bumping version...")
        bump_version(bump_type, config.version.files)
        version = get_current_version(config.version.files[0])
        logger.success(f"Bumped version to {version}")
        
        # Step 6: Generate changelog
        logger.start_operation("Generating changelog...")
        try:
            if config.changelog.ai.enabled:
                logger.api_call("OpenAI", "chat/completions", {
                    "model": config.changelog.ai.model,
                    "temperature": config.changelog.ai.temperature,
                    "messages": [{"role": "system", "content": "Generate changelog"}]
                })
                changelog_text = generate_changelog_with_ai(
                    model=config.changelog.ai.model,
                    temperature=config.changelog.ai.temperature,
                    sections=config.changelog.sections
                )
            else:
                changelog_text = generate_changelog(config.changelog.sections, False)
            logger.success("Generated changelog")
        except Exception as e:
            logger.warning(f"Error generating changelog: {e}")
            logger.warning("Falling back to manual changelog generation")
            changelog_text = generate_changelog(config.changelog.sections, False)
        
        # Step 7: Generate release title
        logger.start_operation("Generating release title...")
        logger.api_call("OpenAI", "chat/completions", {
            "model": config.changelog.ai.model,
            "temperature": config.changelog.ai.temperature,
            "messages": [{"role": "system", "content": "Generate release title"}]
        })
        title = generate_release_title(
            version,
            changelog_text,
            model=config.changelog.ai.model,
            temperature=config.changelog.ai.temperature
        )
        logger.success(f"Generated release title: {title}")
        
        # Step 8: Build final package for publishing
        if config.pypi.publish:
            logger.start_operation("Building package for publishing...")
            cmd = ["uv", "build", "--no-sources"]
            logger.command(cmd)
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success("Package built successfully")
            
            # Step 9: Publish to PyPI
            logger.start_operation("Publishing package...")
            publish_package(config)
            logger.success("Package published to PyPI")
        
        # Step 10: Create Git release
        if config.git.release.enabled:
            logger.start_operation("Creating Git release...")
            create_git_release(version, title, changelog_text, config)
            logger.success("Git release created")
        
        # Final success message
        logger.panel(
            f"Successfully created release {version}\n\n"
            f"Title: {title}\n\n"
            f"Changelog:\n{changelog_text}",
            "Release Complete",
            "green"
        )
        
    except ReleaseError as e:
        logger.error("Release creation failed")
        raise e

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
            code=ErrorCode.PYPI_TOKEN_MISSING,
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
                code=ErrorCode.PYPI_METADATA_ERROR,
                message=f"Failed to publish package due to metadata version incompatibility:\n{error_output}",
                cause=e
            )
        
        # Other publish errors
        raise ReleaseError(
            code=ErrorCode.PYPI_PUBLISH_ERROR,
            message=f"Failed to publish package:\n{error_output}",
            cause=e
        )

def bump_version(bump_type: str, version_files: List[str]) -> None:
    """Bump version in specified files.
    
    Args:
        bump_type: Type of version bump (major, minor, patch)
        version_files: List of files containing version strings
    
    Raises:
        ReleaseError: If version bump fails
    """
    current_version = get_current_version(version_files[0])
    if not current_version:
        raise ReleaseError(
            code=ErrorCode.VERSION_NOT_FOUND,
            message="Could not determine current version"
        )
    
    # Parse version components
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", current_version)
    if not match:
        raise ReleaseError(
            code=ErrorCode.VERSION_INVALID,
            message=f"Invalid version format: {current_version}"
        )
    
    major, minor, patch = map(int, match.groups())
    
    # Calculate new version
    if bump_type == "major":
        new_version = f"{major + 1}.0.0"
    elif bump_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        raise ReleaseError(
            code=ErrorCode.VERSION_INVALID,
            message=f"Invalid bump type: {bump_type}"
        )
    
    # Update version in files
    for file in version_files:
        logger.command(["sed", "-i", f"s/{current_version}/{new_version}/g", file])
        update_version_in_file(file, current_version, new_version)
        logger.success(f"Updated version in {file}")

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
    
    Raises:
        ReleaseError: If cleaning fails
    """
    dist_dir = Path("dist")
    try:
        if dist_dir.exists():
            logger.command(["rm", "-rf", "dist"])
            shutil.rmtree(dist_dir)
        dist_dir.mkdir(exist_ok=True)
    except Exception as e:
        raise ReleaseError(
            code=ErrorCode.BUILD_FAILED,
            message=f"Failed to clean dist directory: {e}",
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
            code=ErrorCode.GITHUB_RELEASE_ERROR,
            message=f"Failed to create Git release:\n{e.stdout}\n{e.stderr}",
            cause=e
        )