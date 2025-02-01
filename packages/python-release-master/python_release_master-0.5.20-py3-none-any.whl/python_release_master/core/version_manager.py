"""Version management for Python Release Master."""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from packaging.version import Version, parse
import tomli
import tomli_w

from python_release_master.core.errors import ErrorCode, ReleaseError
from python_release_master.core.logger import logger


class VersionManager:
    """Manages version bumping and validation."""
    
    def __init__(self, workspace_dir: Path):
        """Initialize version manager.
        
        Args:
            workspace_dir: Path to workspace directory
        """
        self.workspace_dir = workspace_dir
        self._current_versions = {}  # Cache for current versions
    
    def _load_pyproject_toml(self) -> Dict[str, Any]:
        """Load and parse pyproject.toml.
        
        Returns:
            Dict containing pyproject.toml contents
            
        Raises:
            ReleaseError: If file not found or invalid
        """
        pyproject_path = self.workspace_dir / "pyproject.toml"
        if not pyproject_path.exists():
            raise ReleaseError(
                ErrorCode.CONFIG_NOT_FOUND,
                "pyproject.toml not found",
                fix_instructions=[
                    "Create a pyproject.toml file in your project root",
                    "Include required build-system and project sections"
                ]
            )
        
        try:
            with open(pyproject_path, "rb") as f:
                return tomli.load(f)
        except Exception as e:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID,
                f"Failed to parse pyproject.toml: {str(e)}",
                cause=e
            )
    
    def _save_pyproject_toml(self, config: Dict[str, Any]) -> None:
        """Save pyproject.toml.
        
        Args:
            config: Configuration to save
            
        Raises:
            ReleaseError: If save fails
        """
        pyproject_path = self.workspace_dir / "pyproject.toml"
        try:
            with open(pyproject_path, "wb") as f:
                tomli_w.dump(config, f)
        except Exception as e:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID,
                f"Failed to save pyproject.toml: {str(e)}",
                cause=e
            )
    
    def _get_version_from_file(self, file_path: Path) -> Optional[str]:
        """Extract version from a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Version string if found, None otherwise
        """
        try:
            with open(file_path, "r") as f:
                content = f.read()
                # Common version patterns
                patterns = [
                    r'version\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # version = "x.y.z"
                    r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # __version__ = "x.y.z"
                    r'VERSION\s*=\s*["\'](\d+\.\d+\.\d+)["\']',  # VERSION = "x.y.z"
                ]
                for pattern in patterns:
                    match = re.search(pattern, content)
                    if match:
                        return match.group(1)
            return None
        except Exception:
            return None
    
    def get_current_versions(self) -> Dict[str, str]:
        """Get current versions from all version files.
        
        Returns:
            Dict mapping file paths to version strings
            
        Raises:
            ReleaseError: If versions are inconsistent
        """
        if self._current_versions:
            return self._current_versions
        
        versions = {}
        
        # Get version from pyproject.toml
        config = self._load_pyproject_toml()
        if "project" in config and "version" in config["project"]:
            versions["pyproject.toml"] = config["project"]["version"]
        
        # Get version from __init__.py
        package_name = config["project"]["name"].replace("-", "_")
        init_path = self.workspace_dir / "src" / package_name / "__init__.py"
        if init_path.exists():
            version = self._get_version_from_file(init_path)
            if version:
                versions[str(init_path)] = version
        
        # Validate versions are consistent
        if len(set(versions.values())) > 1:
            raise ReleaseError(
                ErrorCode.VERSION_MISMATCH,
                "Inconsistent versions found across files",
                context={"versions": versions},
                fix_instructions=[
                    "Update all version strings to match:",
                    *[f"- {file}: {version}" for file, version in versions.items()]
                ]
            )
        
        self._current_versions = versions
        return versions
    
    def validate_new_version(self, new_version: str) -> None:
        """Validate that a new version is valid and newer than current.
        
        Args:
            new_version: Version string to validate
            
        Raises:
            ReleaseError: If version is invalid or not newer
        """
        # Validate version format
        if not re.match(r"^\d+\.\d+\.\d+$", new_version):
            raise ReleaseError(
                ErrorCode.VERSION_INVALID,
                f"Invalid version format: {new_version}",
                fix_instructions=[
                    "Version must follow semantic versioning (MAJOR.MINOR.PATCH)",
                    "Examples: 1.0.0, 0.5.17, 2.3.1"
                ]
            )
        
        # Get current versions
        current_versions = self.get_current_versions()
        if not current_versions:
            return
        
        # Compare with all current versions
        new_ver = parse(new_version)
        for file, current_version in current_versions.items():
            current_ver = parse(current_version)
            if new_ver <= current_ver:
                raise ReleaseError(
                    ErrorCode.VERSION_INVALID,
                    f"New version {new_version} is not newer than current version {current_version} in {file}",
                    fix_instructions=[
                        f"Choose a version higher than {current_version}",
                        "Current versions:",
                        *[f"- {f}: {v}" for f, v in current_versions.items()],
                        "",
                        "Suggested versions:",
                        f"- Patch: {current_ver.major}.{current_ver.minor}.{current_ver.micro + 1}",
                        f"- Minor: {current_ver.major}.{current_ver.minor + 1}.0",
                        f"- Major: {current_ver.major + 1}.0.0"
                    ]
                )
    
    def bump_version(self, new_version: str) -> None:
        """Bump version in all version files.
        
        Args:
            new_version: New version string
            
        Raises:
            ReleaseError: If version bump fails
        """
        # Validate new version
        self.validate_new_version(new_version)
        
        # Update pyproject.toml
        config = self._load_pyproject_toml()
        old_version = config["project"]["version"]
        config["project"]["version"] = new_version
        self._save_pyproject_toml(config)
        logger.success("Updated version in pyproject.toml")
        
        # Update __init__.py
        package_name = config["project"]["name"].replace("-", "_")
        init_path = self.workspace_dir / "src" / package_name / "__init__.py"
        if init_path.exists():
            try:
                with open(init_path, "r") as f:
                    content = f.read()
                
                # Update version patterns
                patterns = [
                    (r'version\s*=\s*["\'](\d+\.\d+\.\d+)["\']', f'version = "{new_version}"'),
                    (r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', f'__version__ = "{new_version}"'),
                    (r'VERSION\s*=\s*["\'](\d+\.\d+\.\d+)["\']', f'VERSION = "{new_version}"')
                ]
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                
                with open(init_path, "w") as f:
                    f.write(content)
                
                logger.success(f"Updated version in {init_path}")
            except Exception as e:
                raise ReleaseError(
                    ErrorCode.VERSION_UPDATE_FAILED,
                    f"Failed to update version in {init_path}",
                    cause=e
                )
        
        # Clear version cache
        self._current_versions = {}
        
        logger.success(f"Bumped version to {new_version}")
    
    def suggest_version_bump(self, bump_type: str = "patch") -> str:
        """Suggest next version based on bump type.
        
        Args:
            bump_type: Type of version bump (major, minor, patch)
            
        Returns:
            Suggested version string
            
        Raises:
            ReleaseError: If current version cannot be determined
        """
        current_versions = self.get_current_versions()
        if not current_versions:
            return "0.1.0"  # Default for new projects
        
        # Use first version (they should all be the same)
        current_version = parse(next(iter(current_versions.values())))
        
        if bump_type == "major":
            return f"{current_version.major + 1}.0.0"
        elif bump_type == "minor":
            return f"{current_version.major}.{current_version.minor + 1}.0"
        else:  # patch
            return f"{current_version.major}.{current_version.minor}.{current_version.micro + 1}" 