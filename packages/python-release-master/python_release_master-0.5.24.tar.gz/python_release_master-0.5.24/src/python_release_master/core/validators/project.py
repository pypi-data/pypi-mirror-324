"""Validator for project metadata in pyproject.toml."""

import re
from pathlib import Path
from typing import Dict, Any, List

from python_release_master.core.errors import ErrorCode, ReleaseError
from python_release_master.core.validators.base import BaseValidator


class ProjectMetadataValidator(BaseValidator):
    """Validates project metadata in pyproject.toml."""
    
    REQUIRED_FIELDS = [
        "name",
        "version",
        "description",
        "readme",
        "requires-python",
        "license",
        "dependencies",
        "authors"
    ]
    
    OPTIONAL_FIELDS = [
        "keywords",
        "classifiers",
        "urls",
        "scripts",
        "gui-scripts",
        "entry-points",
        "optional-dependencies"
    ]
    
    PYTHON_VERSION_PATTERN = r"^>=\d+\.\d+(\.\d+)?$"
    VERSION_PATTERN = r"^\d+\.\d+\.\d+$"
    LICENSE_IDENTIFIERS = [
        "MIT", "Apache-2.0", "GPL-3.0-or-later", "BSD-3-Clause",
        "LGPL-3.0-or-later", "MPL-2.0"
    ]
    
    def _validate_name(self, name: str) -> None:
        """Validate package name.
        
        Args:
            name: Package name
            
        Raises:
            ReleaseError: If validation fails
        """
        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", name):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                f"Invalid package name: {name}",
                fix_instructions=[
                    "Package name must:",
                    "1. Start with a lowercase letter",
                    "2. Contain only lowercase letters, numbers, and hyphens",
                    "3. End with a letter or number",
                    "4. Not contain consecutive hyphens",
                    "",
                    "Examples of valid names:",
                    "- my-package",
                    "- awesome-tool",
                    "- python-release-master"
                ]
            )
    
    def _validate_version(self, version: str) -> None:
        """Validate package version.
        
        Args:
            version: Package version
            
        Raises:
            ReleaseError: If validation fails
        """
        if not re.match(self.VERSION_PATTERN, version):
            raise ReleaseError(
                ErrorCode.VERSION_INVALID,
                f"Invalid version format: {version}",
                fix_instructions=[
                    "Version must follow semantic versioning (MAJOR.MINOR.PATCH)",
                    "",
                    "Examples:",
                    "- 1.0.0",
                    "- 0.5.17",
                    "- 2.3.1"
                ]
            )
    
    def _validate_python_version(self, requires_python: str) -> None:
        """Validate Python version requirement.
        
        Args:
            requires_python: Python version requirement
            
        Raises:
            ReleaseError: If validation fails
        """
        if not re.match(self.PYTHON_VERSION_PATTERN, requires_python):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                f"Invalid Python version requirement: {requires_python}",
                fix_instructions=[
                    "Python version requirement must be in format: >=X.Y[.Z]",
                    "",
                    "Examples:",
                    "- >=3.8",
                    "- >=3.9.0",
                    "- >=3.10"
                ]
            )
    
    def _validate_license(self, license_info: Dict[str, str]) -> None:
        """Validate license information.
        
        Args:
            license_info: License information
            
        Raises:
            ReleaseError: If validation fails
        """
        if not isinstance(license_info, dict) or "text" not in license_info:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "Invalid license format",
                fix_instructions=[
                    "License must be specified as a table with 'text' field:",
                    "",
                    "license = { text = \"MIT\" }",
                    "",
                    "Common license identifiers:",
                    *[f"- {lid}" for lid in self.LICENSE_IDENTIFIERS]
                ]
            )
        
        if license_info["text"] not in self.LICENSE_IDENTIFIERS:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                f"Unknown license identifier: {license_info['text']}",
                fix_instructions=[
                    "Use one of these common license identifiers:",
                    *[f"- {lid}" for lid in self.LICENSE_IDENTIFIERS],
                    "",
                    "Example:",
                    'license = { text = "MIT" }'
                ]
            )
    
    def _validate_dependencies(self, dependencies: List[str]) -> None:
        """Validate package dependencies.
        
        Args:
            dependencies: List of dependencies
            
        Raises:
            ReleaseError: If validation fails
        """
        if not isinstance(dependencies, list):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "Dependencies must be a list",
                fix_instructions=[
                    "Format dependencies as a list:",
                    "",
                    "dependencies = [",
                    '    "requests>=2.25.0",',
                    '    "click>=8.0.0"',
                    "]"
                ]
            )
        
        for dep in dependencies:
            if not re.match(r"^[a-zA-Z0-9-_.]+([><=!~]=?[0-9a-zA-Z.-]+)?$", dep):
                raise ReleaseError(
                    ErrorCode.CONFIG_INVALID_VALUE,
                    f"Invalid dependency format: {dep}",
                    fix_instructions=[
                        "Dependencies must follow the format: package[>=|==]version",
                        "",
                        "Examples:",
                        '- "requests>=2.25.0"',
                        '- "click>=8.0.0"',
                        '- "rich==10.0.0"'
                    ]
                )
    
    def _validate_authors(self, authors: List[Dict[str, str]]) -> None:
        """Validate authors information.
        
        Args:
            authors: List of author information
            
        Raises:
            ReleaseError: If validation fails
        """
        if not isinstance(authors, list):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "Authors must be a list of tables",
                fix_instructions=[
                    "Format authors as a list of tables:",
                    "",
                    "[[project.authors]]",
                    'name = "Your Name"',
                    'email = "your.email@example.com"'
                ]
            )
        
        for author in authors:
            if not isinstance(author, dict) or "name" not in author:
                raise ReleaseError(
                    ErrorCode.CONFIG_INVALID_VALUE,
                    "Each author must have at least a name",
                    fix_instructions=[
                        "Each author must be a table with at least a name:",
                        "",
                        "[[project.authors]]",
                        'name = "Your Name"',
                        'email = "your.email@example.com"  # Optional'
                    ]
                )
    
    def validate(self) -> None:
        """Validate project metadata.
        
        Raises:
            ReleaseError: If validation fails
        """
        config = self._load_pyproject_toml()
        
        if "project" not in config:
            raise ReleaseError(
                ErrorCode.CONFIG_MISSING_FIELD,
                "Missing [project] section in pyproject.toml",
                fix_instructions=[
                    "Add a [project] section to your pyproject.toml:",
                    "",
                    "[project]",
                    'name = "your-package"',
                    'version = "0.1.0"',
                    'description = "Your package description"',
                    'readme = "README.md"',
                    'requires-python = ">=3.8"',
                    'license = { text = "MIT" }',
                    "",
                    "[[project.authors]]",
                    'name = "Your Name"',
                    'email = "your.email@example.com"'
                ]
            )
        
        project = config["project"]
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in project:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_FIELD,
                    f"Missing required field '{field}' in [project] section",
                    fix_instructions=[
                        f"Add the '{field}' field to your [project] section.",
                        "See the documentation for the correct format."
                    ]
                )
        
        # Validate each field
        self._validate_name(project["name"])
        self._validate_version(project["version"])
        self._validate_python_version(project["requires-python"])
        self._validate_license(project["license"])
        self._validate_dependencies(project["dependencies"])
        self._validate_authors(project["authors"]) 