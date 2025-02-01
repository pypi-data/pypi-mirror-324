"""Validation classes for repository structure and publishing requirements."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import tomli
import re

from python_release_master.core.errors import (
    ErrorCode,
    ReleaseError,
)
from python_release_master.core.logger import logger


class BaseValidator:
    """Base class for all validators."""
    
    def __init__(self, workspace_dir: Path):
        """Initialize validator.
        
        Args:
            workspace_dir: Path to workspace directory
        """
        self.workspace_dir = workspace_dir
    
    def validate(self) -> None:
        """Validate the workspace.
        
        Raises:
            ReleaseError: If validation fails
        """
        raise NotImplementedError


class PyProjectValidator(BaseValidator):
    """Validates pyproject.toml configuration."""
    
    REQUIRED_SECTIONS = ["build-system", "project"]
    REQUIRED_BUILD_FIELDS = ["requires", "build-backend"]
    REQUIRED_PROJECT_FIELDS = [
        "name", "version", "description", "readme",
        "requires-python", "license", "dependencies"
    ]
    
    def validate(self) -> None:
        """Validate pyproject.toml configuration.
        
        Raises:
            ReleaseError: If validation fails
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
                config = tomli.load(f)
        except Exception as e:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID,
                f"Failed to parse pyproject.toml: {str(e)}",
                cause=e
            )
        
        # Validate required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in config:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_REQUIRED,
                    f"Missing required section [{section}] in pyproject.toml"
                )
        
        # Validate build-system fields
        for field in self.REQUIRED_BUILD_FIELDS:
            if field not in config["build-system"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_REQUIRED,
                    f"Missing required field '{field}' in [build-system] section"
                )
        
        # Validate project fields
        for field in self.REQUIRED_PROJECT_FIELDS:
            if field not in config["project"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_REQUIRED,
                    f"Missing required field '{field}' in [project] section"
                )
        
        # Validate version format
        version = config["project"]["version"]
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            raise ReleaseError(
                ErrorCode.VERSION_INVALID,
                f"Invalid version format: {version}. Must be in format X.Y.Z"
            )


class PackageStructureValidator(BaseValidator):
    """Validates package directory structure."""
    
    def validate(self) -> None:
        """Validate package directory structure.
        
        Raises:
            ReleaseError: If validation fails
        """
        # Check src directory exists
        src_dir = self.workspace_dir / "src"
        if not src_dir.exists():
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                "src directory not found",
                fix_instructions=[
                    "Create a src directory in your project root",
                    "Move your package code into src/<package_name>"
                ]
            )
        
        # Get package name from pyproject.toml
        pyproject_path = self.workspace_dir / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            config = tomli.load(f)
        package_name = config["project"]["name"]
        
        # Check package directory exists
        package_dir = src_dir / package_name.replace("-", "_")
        if not package_dir.exists():
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                f"Package directory {package_dir} not found",
                fix_instructions=[
                    f"Create directory src/{package_name}",
                    "Move your package code into this directory"
                ]
            )
        
        # Check __init__.py exists
        init_file = package_dir / "__init__.py"
        if not init_file.exists():
            raise ReleaseError(
                ErrorCode.PKG_FILE_MISSING,
                f"__init__.py not found in {package_dir}",
                fix_instructions=[
                    f"Create {init_file} file",
                    "Add version and package metadata"
                ]
            )


class RequiredFilesValidator(BaseValidator):
    """Validates presence of required files."""
    
    REQUIRED_FILES = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        ".gitignore"
    ]
    
    def validate(self) -> None:
        """Validate required files exist.
        
        Raises:
            ReleaseError: If validation fails
        """
        for filename in self.REQUIRED_FILES:
            file_path = self.workspace_dir / filename
            if not file_path.exists():
                raise ReleaseError(
                    ErrorCode.PKG_FILE_MISSING,
                    f"Required file {filename} not found",
                    fix_instructions=[
                        f"Create {filename} in your project root",
                        "Add appropriate content based on file type"
                    ]
                )


class DependencyValidator(BaseValidator):
    """Validates package dependencies."""
    
    def validate(self) -> None:
        """Validate package dependencies.
        
        Raises:
            ReleaseError: If validation fails
        """
        pyproject_path = self.workspace_dir / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            config = tomli.load(f)
        
        dependencies = config["project"].get("dependencies", [])
        
        # Validate dependency format
        for dep in dependencies:
            if not re.match(r"^[a-zA-Z0-9-_.]+([><=!~]=?[0-9a-zA-Z.-]+)?$", dep):
                raise ReleaseError(
                    ErrorCode.CONFIG_INVALID,
                    f"Invalid dependency format: {dep}",
                    fix_instructions=[
                        "Use format: package>=version or package==version",
                        "Example: requests>=2.25.0"
                    ]
                )


class EntryPointValidator(BaseValidator):
    """Validates CLI entry points."""
    
    def validate(self) -> None:
        """Validate CLI entry points.
        
        Raises:
            ReleaseError: If validation fails
        """
        pyproject_path = self.workspace_dir / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            config = tomli.load(f)
        
        # Check if project.scripts is defined
        if "scripts" not in config.get("project", {}):
            raise ReleaseError(
                ErrorCode.CONFIG_MISSING_REQUIRED,
                "No CLI entry points defined in [project.scripts]",
                fix_instructions=[
                    "Add [project.scripts] section to pyproject.toml",
                    "Define your CLI entry points",
                    'Example: my-cli = "my_package.cli:main"'
                ]
            )
        
        # Validate each entry point
        for script_name, entry_point in config["project"]["scripts"].items():
            # Check entry point format
            if not re.match(r"^[a-zA-Z0-9_.]+:[a-zA-Z0-9_]+$", entry_point):
                raise ReleaseError(
                    ErrorCode.CONFIG_INVALID,
                    f"Invalid entry point format: {entry_point}",
                    fix_instructions=[
                        'Use format: "package.module:function"',
                        'Example: "my_package.cli:main"'
                    ]
                )
            
            # Check if the module and function exist
            module_path, func_name = entry_point.split(":")
            module_parts = module_path.split(".")
            
            # Convert module path to file path
            file_path = self.workspace_dir / "src"
            for part in module_parts:
                file_path = file_path / part
            file_path = file_path.with_suffix(".py")
            
            if not file_path.exists():
                raise ReleaseError(
                    ErrorCode.PKG_FILE_MISSING,
                    f"Entry point module not found: {file_path}",
                    fix_instructions=[
                        f"Create module {module_path}",
                        f"Implement function {func_name}"
                    ]
                )


class RepositoryValidator:
    """Main validator that runs all validation checks."""
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        """Initialize repository validator.
        
        Args:
            workspace_dir: Path to workspace directory, defaults to current directory
        """
        self.workspace_dir = Path(workspace_dir or os.getcwd())
        
        # Initialize all validators
        self.validators = [
            PyProjectValidator(self.workspace_dir),
            PackageStructureValidator(self.workspace_dir),
            RequiredFilesValidator(self.workspace_dir),
            DependencyValidator(self.workspace_dir),
            EntryPointValidator(self.workspace_dir)
        ]
    
    def validate(self) -> None:
        """Run all validation checks.
        
        Raises:
            ReleaseError: If any validation fails
        """
        for validator in self.validators:
            validator_name = validator.__class__.__name__
            logger.start_operation(f"Running {validator_name}...")
            try:
                validator.validate()
                logger.success(f"{validator_name} passed")
            except ReleaseError as e:
                logger.error(f"{validator_name} failed")
                raise e 