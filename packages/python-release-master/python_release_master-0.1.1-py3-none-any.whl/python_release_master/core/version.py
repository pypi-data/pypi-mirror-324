"""Version management functionality for python-release-master."""
import os
import re
from typing import Optional

import toml

def get_current_version(version_file: str = "pyproject.toml") -> str:
    """Get the current version from pyproject.toml."""
    if not os.path.exists(version_file):
        raise FileNotFoundError(f"Version file {version_file} not found")
    
    with open(version_file) as f:
        data = toml.load(f)
    
    return data["project"]["version"]

def bump_version(bump_type: str, version_file: str = "pyproject.toml") -> str:
    """Bump the version number based on semver rules."""
    current = get_current_version(version_file)
    
    # Parse current version
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", current)
    if not match:
        raise ValueError(f"Invalid version format: {current}")
    
    major, minor, patch = map(int, match.groups())
    
    # Bump version according to type
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    new_version = f"{major}.{minor}.{patch}"
    
    # Update version in file
    with open(version_file) as f:
        data = toml.load(f)
    
    data["project"]["version"] = new_version
    
    with open(version_file, "w") as f:
        toml.dump(data, f)
    
    return new_version

def validate_version(version: str) -> bool:
    """Validate that a version string follows semver format."""
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version)) 