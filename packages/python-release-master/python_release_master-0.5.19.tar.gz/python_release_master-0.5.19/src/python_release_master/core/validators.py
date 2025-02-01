"""Validation classes for repository structure and publishing requirements."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import tomli
import re
import yaml
from abc import ABC, abstractmethod

from python_release_master.core.errors import (
    ErrorCode,
    ReleaseError,
)
from python_release_master.core.logger import logger


class BaseValidator(ABC):
    """Base class for all validators."""
    
    def __init__(self, workspace_dir: Path):
        """Initialize validator.
        
        Args:
            workspace_dir: Path to workspace directory
        """
        self.workspace_dir = workspace_dir
    
    @abstractmethod
    def validate(self) -> None:
        """Validate the workspace.
        
        Raises:
            ReleaseError: If validation fails
        """
        pass


class ConfigValidator(BaseValidator):
    """Validates .release-master.yaml configuration."""
    
    REQUIRED_SECTIONS = ["version", "changelog", "git", "pypi", "github"]
    REQUIRED_VERSION_FIELDS = ["files", "pattern"]
    REQUIRED_CHANGELOG_FIELDS = ["ai", "sections", "commit_conventions"]
    REQUIRED_GIT_FIELDS = ["push", "tag_prefix", "release"]
    REQUIRED_PYPI_FIELDS = ["publish", "repository", "token_env_var", "uv_token_env_var"]
    REQUIRED_GITHUB_FIELDS = ["auto_create", "owner", "repo_name", "private", "description", "token_env_var"]
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.required_sections = ["version", "changelog", "git", "pypi", "testing", "github"]
    
    def validate(self) -> None:
        """Validate .release-master.yaml configuration.
        
        Raises:
            ReleaseError: If validation fails
        """
        config_path = self.workspace_dir / ".release-master.yaml"
        
        if not config_path.exists():
            raise ReleaseError(
                ErrorCode.CONFIG_NOT_FOUND,
                ".release-master.yaml not found",
                context={"file": str(config_path)}
            )
        
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
        except Exception as e:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID,
                f"Failed to parse .release-master.yaml: {str(e)}",
                context={"file": str(config_path)}
            )
        
        # Validate required sections
        for section in self.required_sections:
            if section not in config:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required section '{section}' in configuration"
                )
        
        # Validate version section
        for field in self.REQUIRED_VERSION_FIELDS:
            if field not in config["version"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required field '{field}' in version section"
                )
        
        # Validate version pattern
        try:
            re.compile(config["version"]["pattern"])
        except re.error as e:
            raise ReleaseError(
                ErrorCode.CONFIG_VALIDATION_ERROR,
                f"Invalid version pattern: {e}"
            )
        
        # Validate changelog section
        for field in self.REQUIRED_CHANGELOG_FIELDS:
            if field not in config["changelog"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required field '{field}' in changelog section"
                )
        
        # Validate git section
        for field in self.REQUIRED_GIT_FIELDS:
            if field not in config["git"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required field '{field}' in git section"
                )
        
        # Validate PyPI section
        for field in self.REQUIRED_PYPI_FIELDS:
            if field not in config["pypi"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required field '{field}' in pypi section"
                )
        
        # Validate GitHub section
        for field in self.REQUIRED_GITHUB_FIELDS:
            if field not in config["github"]:
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    f"Missing required field '{field}' in github section"
                )
        
        # Validate testing section
        if "testing" not in config:
            raise ReleaseError(
                ErrorCode.CONFIG_VALIDATION_ERROR,
                "Testing section is missing"
            )
        
        # Validate release settings if enabled
        if config["git"].get("release", {}).get("enabled"):
            if not config["git"].get("tag_prefix"):
                raise ReleaseError(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    "Tag prefix must be specified when releases are enabled"
                )
        
        # Validate PyPI token if publishing is enabled
        if config["pypi"]["publish"]:
            token_var = config["pypi"]["token_env_var"]
            if token_var not in os.environ:
                raise ReleaseError(
                    ErrorCode.PYPI_VALIDATION_ERROR,
                    f"PyPI token not found in environment variable {token_var}"
                )
            
            # Check UV token
            uv_token_var = config["pypi"]["uv_token_env_var"]
            if uv_token_var not in os.environ:
                raise ReleaseError(
                    ErrorCode.PYPI_VALIDATION_ERROR,
                    f"UV token not found in environment variable {uv_token_var}"
                )


class GitValidator(BaseValidator):
    """Validates Git configuration and state."""
    
    def validate(self) -> None:
        """Validate Git configuration and state.
        
        Raises:
            ReleaseError: If validation fails
        """
        # Check if Git is installed
        try:
            import subprocess
            subprocess.run(["git", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ReleaseError(
                ErrorCode.GIT_NOT_INSTALLED,
                "Git is not installed",
                context={"command": "git --version"}
            )
        
        # Check if Git repository exists
        git_dir = self.workspace_dir / ".git"
        if not git_dir.exists():
            raise ReleaseError(
                ErrorCode.GIT_REPO_NOT_FOUND,
                "Git repository not found",
                context={"directory": str(self.workspace_dir)}
            )
        
        # Note: We don't check for uncommitted changes here since they will be handled
        # by the AI-powered commit and release process later in the pipeline


class PyPIValidator(BaseValidator):
    """Validates PyPI configuration."""
    
    def validate(self) -> None:
        """Validate PyPI configuration.
        
        Raises:
            ReleaseError: If validation fails
        """
        # Check if UV is installed
        try:
            import subprocess
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ReleaseError(
                ErrorCode.UV_NOT_INSTALLED,
                "UV is not installed",
                context={"command": "uv --version"}
            )
        
        # Load config
        config_path = self.workspace_dir / ".release-master.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Check PyPI token if publishing is enabled
        if config["pypi"]["publish"]:
            token_var = config["pypi"]["token_env_var"]
            if token_var not in os.environ:
                raise ReleaseError(
                    ErrorCode.PYPI_VALIDATION_ERROR,
                    f"PyPI token not found in environment variable {token_var}"
                )
            
            # Check UV token
            uv_token_var = config["pypi"]["uv_token_env_var"]
            if uv_token_var not in os.environ:
                raise ReleaseError(
                    ErrorCode.PYPI_VALIDATION_ERROR,
                    f"UV token not found in environment variable {uv_token_var}"
                )


class TestingValidator(BaseValidator):
    """Validates testing configuration."""
    
    def validate(self) -> None:
        """Validate testing configuration.
        
        Raises:
            ReleaseError: If validation fails
        """
        # Load config
        config_path = self.workspace_dir / ".release-master.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Check if tests directory exists
        tests_dir = self.workspace_dir / "tests"
        if not tests_dir.exists():
            raise ReleaseError(
                ErrorCode.TESTS_DIR_NOT_FOUND,
                "Tests directory not found",
                context={"directory": str(tests_dir)}
            )
        
        # Check if Docker is available if enabled
        if config["testing"].get("docker", {}).get("enabled", False):
            try:
                import subprocess
                subprocess.run(["docker", "--version"], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                raise ReleaseError(
                    ErrorCode.SYSTEM_COMMAND_ERROR,
                    "Docker is not installed but testing.docker.enabled is true",
                    context={"command": "docker --version"}
                )


class PyProjectValidator(BaseValidator):
    """Validates pyproject.toml configuration."""
    
    REQUIRED_SECTIONS = ["build-system", "project"]
    REQUIRED_BUILD_FIELDS = ["requires", "build-backend"]
    REQUIRED_PROJECT_FIELDS = [
        "name", "version", "description", "readme",
        "requires-python", "license", "dependencies"
    ]
    
    # Build backend metadata version support
    BUILD_BACKEND_METADATA_VERSIONS = {
        "setuptools.build_meta": "2.1",  # setuptools supports metadata 2.1
        "hatchling.build": "2.4",        # hatchling supports metadata 2.4
        "poetry.core.masonry.api": "2.4", # poetry supports metadata 2.4
        "pdm.backend": "2.4",            # pdm supports metadata 2.4
        "flit.buildapi": "2.4",          # flit supports metadata 2.4
    }
    
    # Metadata version requirements for different features
    METADATA_VERSION_FEATURES = {
        "license-file": "2.4",  # license-file requires metadata version 2.4+
        "dynamic": "2.2",       # dynamic fields require metadata version 2.2+
        "scripts": "2.1",       # Entry points in pyproject.toml require 2.1+
        "dependencies": "2.1",  # Dependencies in pyproject.toml require 2.1+
        "optional-dependencies": "2.1",  # Optional dependencies require 2.1+
    }
    
    def _get_backend_metadata_version(self, backend: str) -> str:
        """Get the metadata version supported by a build backend.
        
        Args:
            backend: Build backend name
        
        Returns:
            Metadata version supported by the backend
        """
        # Get the base backend name without parameters
        base_backend = backend.split(":")[0]
        return self.BUILD_BACKEND_METADATA_VERSIONS.get(base_backend, "2.1")  # Default to 2.1 for unknown backends
    
    def _check_metadata_compatibility(self, config: Dict[str, Any]) -> None:
        """Check if the package metadata is compatible with the build backend.
        
        Args:
            config: pyproject.toml configuration
        
        Raises:
            ReleaseError: If metadata is incompatible with build backend
        """
        backend = config["build-system"]["build-backend"]
        backend_metadata_version = self._get_backend_metadata_version(backend)
        project = config.get("project", {})
        
        # Convert version strings to tuples for comparison
        backend_version = tuple(map(int, backend_metadata_version.split(".")))
        
        for feature, required_version in self.METADATA_VERSION_FEATURES.items():
            required_version_tuple = tuple(map(int, required_version.split(".")))
            
            if feature in project and backend_version < required_version_tuple:
                raise ReleaseError(
                    ErrorCode.PYPI_VALIDATION_ERROR,
                    f"The '{feature}' field requires metadata version {required_version} but build backend '{backend}' only supports {backend_metadata_version}",
                    fix_instructions=[
                        "Either:",
                        f"1. Update your build backend to one that supports metadata {required_version}+",
                        "   - hatchling (recommended)",
                        "   - poetry.core.masonry.api",
                        "   - flit.buildapi",
                        f"2. Remove or modify the '{feature}' field to be compatible with metadata {backend_metadata_version}",
                        "3. Use an alternative configuration format supported by your current build backend"
                    ]
                )
    
    def _validate_build_includes(self, config: Dict[str, Any]) -> None:
        """Validate build includes configuration.
        
        Args:
            config: pyproject.toml configuration
            
        Raises:
            ReleaseError: If validation fails
        """
        package_name = config["project"]["name"].replace("-", "_")
        build_config = config.get("tool", {}).get("hatch", {}).get("build", {})
        includes = build_config.get("include", [])
        
        required_includes = [
            f"src/{package_name}/**/*.py",
            f"src/{package_name}/**/*.pyi",
        ]
        
        missing_includes = [inc for inc in required_includes if inc not in includes]
        if missing_includes:
            raise ReleaseError(
                ErrorCode.CONFIG_MISSING_FIELD,
                "Missing required build includes in pyproject.toml",
                fix_instructions=[
                    "Add the following includes to [tool.hatch.build] section:",
                    "include = [",
                    *[f'    "{inc}",' for inc in required_includes],
                    "]",
                    "",
                    "Example configuration:",
                    "[tool.hatch.build]",
                    "include = [",
                    f'    "src/{package_name}/**/*.py",',
                    f'    "src/{package_name}/**/*.pyi",',
                    "    # Add any other includes you need",
                    "]",
                    'packages = ["src"]'
                ]
            )

    def _validate_entry_points(self, config: Dict[str, Any]) -> None:
        """Validate entry points configuration.
        
        Args:
            config: pyproject.toml configuration
            
        Raises:
            ReleaseError: If validation fails
        """
        package_name = config["project"]["name"]
        package_import = package_name.replace("-", "_")
        scripts = config.get("project", {}).get("scripts", {})
        
        # Check if the main tool entry point exists and is correct
        expected_entry = f"{package_import}.__main__:main"
        actual_entry = scripts.get(package_name)
        
        if not actual_entry:
            raise ReleaseError(
                ErrorCode.CONFIG_MISSING_FIELD,
                f"Missing required entry point for {package_name} in [project.scripts]",
                fix_instructions=[
                    "Add the following entry point to [project.scripts] section:",
                    "[project.scripts]",
                    f'{package_name} = "{expected_entry}"',
                    "",
                    "Then create the corresponding __main__.py file:",
                    f"src/{package_import}/__main__.py",
                    "",
                    "Example __main__.py content:",
                    "def main():",
                    '    """Entry point for the CLI."""',
                    "    # Your CLI code here",
                    "    return 0",
                    "",
                    "if __name__ == '__main__':",
                    "    main()"
                ]
            )
        elif actual_entry != expected_entry:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                f"Invalid entry point format for {package_name}",
                fix_instructions=[
                    "Update the entry point in [project.scripts] section:",
                    "[project.scripts]",
                    f'{package_name} = "{expected_entry}"  # Current: {actual_entry}',
                    "",
                    "The entry point should:",
                    f"1. Use the package import name: {package_import}",
                    "2. Point to __main__:main",
                    "3. Have a corresponding __main__.py file with a main() function"
                ]
            )
    
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
        
        # Check metadata compatibility with build backend
        self._check_metadata_compatibility(config)
        
        # Validate build includes
        self._validate_build_includes(config)
        
        # Validate entry points
        self._validate_entry_points(config)


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
                ErrorCode.SRC_DIR_NOT_FOUND,
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
                ErrorCode.PACKAGE_DIR_NOT_FOUND,
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
                ErrorCode.INIT_PY_NOT_FOUND,
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
                    ErrorCode.PACKAGE_VALIDATION_ERROR,
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
                package_name = config["project"]["name"].replace("-", "_")
                raise ReleaseError(
                    ErrorCode.PACKAGE_VALIDATION_ERROR,
                    f"Entry point module not found: {file_path}",
                    fix_instructions=[
                        f"Create the module file at: {file_path}",
                        f"Or update the entry point in pyproject.toml to point to an existing module",
                        "",
                        "Example module structure:",
                        f"src/{package_name}/",
                        "├── __init__.py",
                        f"└── {module_parts[-1]}.py  # Create this file",
                        "",
                        f"Example {module_parts[-1]}.py content:",
                        "def " + func_name + "():",
                        '    print("Hello from CLI!")',
                        "    return 0"
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
            EntryPointValidator(self.workspace_dir),
            ConfigValidator(self.workspace_dir),
            GitValidator(self.workspace_dir),
            PyPIValidator(self.workspace_dir),
            TestingValidator(self.workspace_dir)
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