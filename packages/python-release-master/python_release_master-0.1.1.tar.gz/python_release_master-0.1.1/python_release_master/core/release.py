"""Release management functionality for python-release-master."""
import os
import re
import subprocess
from typing import Dict, List, Optional, Tuple

from . import version, changelog, docs, ai
from .config import Config


def get_current_version(version_file: str) -> str:
    """Get current version from version file."""
    try:
        with open(version_file) as f:
            content = f.read()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
            raise ValueError(f"No version found in {version_file}")
    except FileNotFoundError:
        raise ValueError(f"Version file {version_file} not found")


def generate_changelog_with_ai(config: Config) -> str:
    """Generate changelog using AI.
    
    Args:
        config: Configuration object with AI settings
        
    Returns:
        Generated changelog text
    """
    try:
        # Get commits since last tag
        commits = ai.get_commit_messages_since_last_tag()
        if not commits:
            return ""
            
        # Get pull requests
        prs = ai.get_pull_requests_since_last_tag()
        
        # Generate changelog using AI
        changelog_text = ai.generate_changelog(
            commits=commits,
            pull_requests=prs,
            sections=config.changelog.sections,
            model=config.changelog.openai_model
        )
        
        return changelog_text
    except Exception as e:
        print(f"AI changelog generation failed: {str(e)}")
        return ""


def generate_changelog(config: Config = None) -> str:
    """Generate changelog for current version."""
    if config and config.changelog.ai_powered:
        changelog_text = generate_changelog_with_ai(config)
        if changelog_text:
            return changelog_text
    return changelog.generate_changelog()


def build_package() -> Tuple[bool, str]:
    """Build the package using build.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Clean dist directory if it's empty
        if not os.path.exists("dist"):
            os.makedirs("dist")
        elif not os.listdir("dist"):
            # Only clean if empty
            for file in os.listdir("dist"):
                os.remove(os.path.join("dist", file))

        # Build package if no dist files exist
        dist_files = os.listdir("dist")
        if not dist_files:
            result = subprocess.run(
                ["python", "-m", "build", "--wheel", "--sdist"],
                capture_output=True,
                text=True,
                check=True
            )

        # Verify build
        dist_files = os.listdir("dist")
        if not dist_files:
            return False, "No package files were created"

        # Check for both wheel and sdist
        has_wheel = any(f.endswith(".whl") for f in dist_files)
        has_sdist = any(f.endswith(".tar.gz") for f in dist_files)

        if not (has_wheel and has_sdist):
            return False, "Missing wheel or sdist package files"

        return True, f"Package built successfully: {', '.join(dist_files)}"
    except subprocess.CalledProcessError as e:
        return False, f"Build command failed: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return False, f"Unexpected error during build: {str(e)}"


def publish_to_pypi() -> Tuple[bool, str]:
    """Publish the package to PyPI.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Check for PyPI token
        if not os.getenv("PYPI_TOKEN"):
            return False, "PYPI_TOKEN environment variable not set"

        # Check for dist directory
        if not os.path.exists("dist") or not os.listdir("dist"):
            return False, "No distribution files found in dist directory"

        # Upload to PyPI using twine
        result = subprocess.run(
            ["twine", "upload", "dist/*", "--non-interactive"],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "TWINE_USERNAME": "__token__", "TWINE_PASSWORD": os.getenv("PYPI_TOKEN")}
        )
        return True, "Package published successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to publish package: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return False, f"Unexpected error during publish: {str(e)}"


def create_git_release(version: str, title: str, body: str) -> Tuple[bool, str]:
    """Create a GitHub release.
    
    Args:
        version: Version number (e.g. "1.0.0")
        title: Release title
        body: Release description
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Ensure version starts with 'v'
        tag_name = f"v{version}" if not version.startswith("v") else version

        # Create and push tag
        subprocess.run(["git", "tag", "-a", tag_name, "-m", title], check=True)
        subprocess.run(["git", "push", "origin", tag_name], check=True)

        # Check for GitHub CLI
        subprocess.run(["gh", "--version"], capture_output=True, check=True)

        # Create release command
        cmd = ["gh", "release", "create", tag_name, "--title", title, "--notes", body]

        # Add dist files if they exist
        if os.path.exists("dist"):
            for file in os.listdir("dist"):
                cmd.extend(["--attach", os.path.join("dist", file)])

        # Create release
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, f"Release {tag_name} created successfully"
    except subprocess.CalledProcessError as e:
        if "gh: command not found" in str(e.stderr):
            return False, "GitHub CLI not installed"
        return False, f"Failed to create release: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        return False, f"Unexpected error during release: {str(e)}"


def update_version_in_file(file_path: str, new_version: str) -> bool:
    """Update version string in a file."""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Common version patterns
    patterns = [
        r'version\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # version = "x.y.z"
        r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # __version__ = "x.y.z"
        r'VERSION\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # VERSION = "x.y.z"
    ]
    
    updated = False
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), new_version), content)
            updated = True
    
    if updated:
        with open(file_path, 'w') as f:
            f.write(content)
    
    return updated


def bump_version(bump_type: str, version_files: List[str]) -> None:
    """Bump version in all version files."""
    if bump_type not in ["major", "minor", "patch"]:
        raise ValueError("Invalid bump type. Must be major, minor, or patch")

    for version_file in version_files:
        current_version = get_current_version(version_file)
        major, minor, patch = map(int, current_version.split("."))

        if bump_type == "major":
            major += 1
            minor = patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        new_version = f"{major}.{minor}.{patch}"
        
        with open(version_file, "r") as f:
            content = f.read()
        
        new_content = re.sub(
            r'version\s*=\s*["\']([^"\']+)["\']',
            f'version = "{new_version}"',
            content
        )
        
        with open(version_file, "w") as f:
            f.write(new_content)


def create_release(
    bump_type: str,
    title: str,
    description: str,
    config: Config,
    skip_steps: Optional[List[str]] = None
) -> None:
    """Create a new release.
    
    Args:
        bump_type: Type of version bump (major, minor, patch)
        title: Release title
        description: Release description
        config: Configuration object
        skip_steps: Optional list of steps to skip
    
    Raises:
        ValueError: If any step fails
    """
    if skip_steps is None:
        skip_steps = []

    # Bump version
    if "version" not in skip_steps:
        bump_version(bump_type, config.version_files)
        version = get_current_version(config.version_files[0])
    else:
        version = get_current_version(config.version_files[0])

    # Generate changelog
    if "changelog" not in skip_steps:
        changelog_text = generate_changelog(config)
        if changelog_text:
            description = f"{description}\n\n{changelog_text}"

    # Build package
    if "build" not in skip_steps:
        success, message = build_package()
        if not success:
            raise ValueError(f"Package build failed: {message}")

    # Publish to PyPI
    if "publish" not in skip_steps:
        success, message = publish_to_pypi()
        if not success:
            raise ValueError(f"Package upload failed: {message}")

    # Create GitHub release
    if "github" not in skip_steps:
        success, message = create_git_release(version, title, description)
        if not success:
            raise ValueError(f"GitHub release failed: {message}")


def create_git_tag(tag_name: str, message: Optional[str] = None) -> None:
    """Create and push a git tag."""
    if not message:
        message = f"Release {tag_name}"
    
    # Create tag
    subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
    
    # Push tag
    subprocess.run(["git", "push", "origin", tag_name], check=True)


def get_latest_tag() -> Optional[str]:
    """Get the latest git tag."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_changes_since_tag(tag: Optional[str] = None) -> List[str]:
    """Get list of changes since the specified tag or all changes if no tag."""
    if not tag:
        tag = get_latest_tag()
    
    if tag:
        cmd = ["git", "log", f"{tag}..HEAD", "--oneline"]
    else:
        cmd = ["git", "log", "--oneline"]
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip().split("\n") 