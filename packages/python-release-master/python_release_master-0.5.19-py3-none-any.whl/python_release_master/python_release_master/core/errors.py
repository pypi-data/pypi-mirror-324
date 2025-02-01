"""Error handling for the Python Release Master."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional, List


class ErrorCode(Enum):
    """Error codes for the Python Release Master."""
    
    # Configuration Errors (1000-1999)
    CONFIG_NOT_FOUND = 1000
    CONFIG_INVALID = 1001
    CONFIG_MISSING_FIELD = 1002
    CONFIG_INVALID_VALUE = 1003
    CONFIG_VERSION_PATTERN_INVALID = 1004
    CONFIG_VALIDATION_ERROR = 1005
    CONFIG_FILE_NOT_FOUND = 1006
    CONFIG_PARSE_ERROR = 1007
    
    # Environment Errors (2000-2999)
    ENV_VAR_MISSING = 2000
    ENV_VAR_INVALID = 2001
    PYTHON_VERSION_UNSUPPORTED = 2002
    GIT_NOT_INSTALLED = 2003
    UV_NOT_INSTALLED = 2004
    
    # Package Structure Errors (3000-3999)
    PYPROJECT_NOT_FOUND = 3000
    PYPROJECT_INVALID = 3001
    SRC_DIR_NOT_FOUND = 3002
    PACKAGE_DIR_NOT_FOUND = 3003
    INIT_PY_NOT_FOUND = 3004
    README_NOT_FOUND = 3005
    LICENSE_NOT_FOUND = 3006
    CHANGELOG_NOT_FOUND = 3007
    TESTS_DIR_NOT_FOUND = 3008
    
    # Build Errors (4000-4999)
    BUILD_FAILED = 4000
    BUILD_INVALID_PACKAGE = 4001
    BUILD_MISSING_DEPENDENCY = 4002
    BUILD_INVALID_ENTRY_POINT = 4003
    BUILD_INVALID_CLASSIFIERS = 4004
    
    # Version Errors (5000-5999)
    VERSION_INVALID = 5000
    VERSION_NOT_FOUND = 5001
    VERSION_MISMATCH = 5002
    VERSION_BUMP_FAILED = 5003
    VERSION_VALIDATION_ERROR = 5004
    VERSION_TAG_EXISTS = 5005
    
    # Git Errors (6000-6999)
    GIT_REPO_NOT_FOUND = 6000
    GIT_REMOTE_NOT_FOUND = 6001
    GIT_PUSH_FAILED = 6002
    GIT_TAG_FAILED = 6003
    GIT_RELEASE_FAILED = 6004
    GIT_DIRTY_WORKSPACE = 6005
    GIT_VALIDATION_ERROR = 6006
    GIT_INIT_FAILED = 6007
    GIT_COMMIT_FAILED = 6008
    
    # PyPI Errors (7000-7999)
    PYPI_AUTH_FAILED = 7000
    PYPI_UPLOAD_FAILED = 7001
    PYPI_PACKAGE_EXISTS = 7002
    PYPI_INVALID_CREDENTIALS = 7003
    PYPI_VALIDATION_ERROR = 7004
    PYPI_BUILD_FAILED = 7005
    
    # GitHub Errors (8000-8999)
    GITHUB_AUTH_FAILED = 8000
    GITHUB_REPO_EXISTS = 8001
    GITHUB_CREATE_FAILED = 8002
    GITHUB_RELEASE_FAILED = 8003
    GITHUB_API_ERROR = 8004
    
    # Validation Errors (9000-9999)
    VALIDATION_FAILED = 9000
    VALIDATION_PACKAGE_NAME = 9001
    VALIDATION_VERSION_FORMAT = 9002
    VALIDATION_DEPENDENCIES = 9003
    VALIDATION_ENTRY_POINTS = 9004
    VALIDATION_CLASSIFIERS = 9005
    
    # Testing Errors (10000-10999)
    TESTING_VALIDATION_ERROR = 10000
    TEST_EXECUTION_FAILED = 10001
    DOCKER_BUILD_FAILED = 10002
    
    # Package Errors (11000-11999)
    PACKAGE_VALIDATION_ERROR = 11000
    PACKAGE_BUILD_FAILED = 11001
    PACKAGE_PUBLISH_FAILED = 11002
    
    # Changelog Errors (12000-12999)
    CHANGELOG_VALIDATION_ERROR = 12000
    CHANGELOG_GENERATION_FAILED = 12001
    
    # Generic Errors (99000-99999)
    UNKNOWN_ERROR = 99000
    OPERATION_CANCELLED = 99001


@dataclass
class ErrorInfo:
    """Information about an error."""
    
    code: ErrorCode
    message: str
    description: str
    fix: str
    context: Optional[Dict[str, Any]] = None


class ReleaseError(Exception):
    """Base exception for the Python Release Master."""
    
    def __init__(
        self,
        code: ErrorCode,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        fix_instructions: Optional[List[str]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        """Initialize the error.
        
        Args:
            code: Error code
            message: Error message
            context: Additional context for the error
            fix_instructions: List of instructions to fix the error
            cause: Original exception that caused this error
        """
        self.code = code
        self.message = message or ERROR_DESCRIPTIONS[code]
        self.context = context or {}
        self.fix_instructions = fix_instructions or []
        self.cause = cause
        super().__init__(self.message)


ERROR_DESCRIPTIONS = {
    # Configuration Errors
    ErrorCode.CONFIG_NOT_FOUND: "Configuration file not found",
    ErrorCode.CONFIG_INVALID: "Invalid configuration file",
    ErrorCode.CONFIG_MISSING_FIELD: "Missing required configuration field",
    ErrorCode.CONFIG_INVALID_VALUE: "Invalid configuration value",
    ErrorCode.CONFIG_VERSION_PATTERN_INVALID: "Invalid version pattern in configuration",
    ErrorCode.CONFIG_VALIDATION_ERROR: "Configuration validation error",
    ErrorCode.CONFIG_FILE_NOT_FOUND: "Configuration file not found",
    ErrorCode.CONFIG_PARSE_ERROR: "Configuration parse error",
    
    # Environment Errors
    ErrorCode.ENV_VAR_MISSING: "Required environment variable not found",
    ErrorCode.ENV_VAR_INVALID: "Invalid environment variable value",
    ErrorCode.PYTHON_VERSION_UNSUPPORTED: "Unsupported Python version",
    ErrorCode.GIT_NOT_INSTALLED: "Git is not installed",
    ErrorCode.UV_NOT_INSTALLED: "UV is not installed",
    
    # Package Structure Errors
    ErrorCode.PYPROJECT_NOT_FOUND: "pyproject.toml not found",
    ErrorCode.PYPROJECT_INVALID: "Invalid pyproject.toml file",
    ErrorCode.SRC_DIR_NOT_FOUND: "src directory not found",
    ErrorCode.PACKAGE_DIR_NOT_FOUND: "Package directory not found",
    ErrorCode.INIT_PY_NOT_FOUND: "__init__.py not found",
    ErrorCode.README_NOT_FOUND: "README.md not found",
    ErrorCode.LICENSE_NOT_FOUND: "LICENSE file not found",
    ErrorCode.CHANGELOG_NOT_FOUND: "CHANGELOG.md not found",
    ErrorCode.TESTS_DIR_NOT_FOUND: "tests directory not found",
    
    # Build Errors
    ErrorCode.BUILD_FAILED: "Package build failed",
    ErrorCode.BUILD_INVALID_PACKAGE: "Invalid package structure",
    ErrorCode.BUILD_MISSING_DEPENDENCY: "Missing build dependency",
    ErrorCode.BUILD_INVALID_ENTRY_POINT: "Invalid entry point configuration",
    ErrorCode.BUILD_INVALID_CLASSIFIERS: "Invalid package classifiers",
    
    # Version Errors
    ErrorCode.VERSION_INVALID: "Invalid version format",
    ErrorCode.VERSION_NOT_FOUND: "Version not found in files",
    ErrorCode.VERSION_MISMATCH: "Version mismatch between files",
    ErrorCode.VERSION_BUMP_FAILED: "Failed to bump version",
    ErrorCode.VERSION_VALIDATION_ERROR: "Version validation error",
    ErrorCode.VERSION_TAG_EXISTS: "Version tag already exists",
    
    # Git Errors
    ErrorCode.GIT_REPO_NOT_FOUND: "Git repository not found",
    ErrorCode.GIT_REMOTE_NOT_FOUND: "Git remote not found",
    ErrorCode.GIT_PUSH_FAILED: "Failed to push to remote",
    ErrorCode.GIT_TAG_FAILED: "Failed to create Git tag",
    ErrorCode.GIT_RELEASE_FAILED: "Failed to create Git release",
    ErrorCode.GIT_DIRTY_WORKSPACE: "Git workspace has uncommitted changes",
    ErrorCode.GIT_VALIDATION_ERROR: "Git validation error",
    ErrorCode.GIT_INIT_FAILED: "Git initialization failed",
    ErrorCode.GIT_COMMIT_FAILED: "Git commit failed",
    
    # PyPI Errors
    ErrorCode.PYPI_AUTH_FAILED: "PyPI authentication failed",
    ErrorCode.PYPI_UPLOAD_FAILED: "Failed to upload package to PyPI",
    ErrorCode.PYPI_PACKAGE_EXISTS: "Package already exists on PyPI",
    ErrorCode.PYPI_INVALID_CREDENTIALS: "Invalid PyPI credentials",
    ErrorCode.PYPI_VALIDATION_ERROR: "PyPI validation error",
    ErrorCode.PYPI_BUILD_FAILED: "PyPI build failed",
    
    # GitHub Errors
    ErrorCode.GITHUB_AUTH_FAILED: "GitHub authentication failed",
    ErrorCode.GITHUB_REPO_EXISTS: "GitHub repository already exists",
    ErrorCode.GITHUB_CREATE_FAILED: "Failed to create GitHub repository",
    ErrorCode.GITHUB_RELEASE_FAILED: "Failed to create GitHub release",
    ErrorCode.GITHUB_API_ERROR: "GitHub API error",
    
    # Validation Errors
    ErrorCode.VALIDATION_FAILED: "Package validation failed",
    ErrorCode.VALIDATION_PACKAGE_NAME: "Invalid package name",
    ErrorCode.VALIDATION_VERSION_FORMAT: "Invalid version format",
    ErrorCode.VALIDATION_DEPENDENCIES: "Invalid dependencies",
    ErrorCode.VALIDATION_ENTRY_POINTS: "Invalid entry points",
    ErrorCode.VALIDATION_CLASSIFIERS: "Invalid classifiers",
    
    # Testing Errors
    ErrorCode.TESTING_VALIDATION_ERROR: "Testing validation error",
    ErrorCode.TEST_EXECUTION_FAILED: "Test execution failed",
    ErrorCode.DOCKER_BUILD_FAILED: "Docker build failed",
    
    # Package Errors
    ErrorCode.PACKAGE_VALIDATION_ERROR: "Package validation error",
    ErrorCode.PACKAGE_BUILD_FAILED: "Package build failed",
    ErrorCode.PACKAGE_PUBLISH_FAILED: "Package publish failed",
    
    # Changelog Errors
    ErrorCode.CHANGELOG_VALIDATION_ERROR: "Changelog validation error",
    ErrorCode.CHANGELOG_GENERATION_FAILED: "Failed to generate changelog",
    
    # Generic Errors
    ErrorCode.UNKNOWN_ERROR: "Unknown error",
    ErrorCode.OPERATION_CANCELLED: "Operation cancelled",
}


ERROR_FIXES = {
    # Configuration Errors
    ErrorCode.CONFIG_NOT_FOUND: "Create a configuration file using the default template",
    ErrorCode.CONFIG_INVALID: "Fix the configuration file according to the schema",
    ErrorCode.CONFIG_MISSING_FIELD: "Add the required field to the configuration file",
    ErrorCode.CONFIG_INVALID_VALUE: "Update the configuration value to match the expected format",
    ErrorCode.CONFIG_VERSION_PATTERN_INVALID: "Use a valid semantic version pattern (e.g., '\\d+\\.\\d+\\.\\d+')",
    ErrorCode.CONFIG_VALIDATION_ERROR: "Fix configuration validation errors",
    ErrorCode.CONFIG_FILE_NOT_FOUND: "Create a configuration file",
    ErrorCode.CONFIG_PARSE_ERROR: "Fix configuration parse errors",
    
    # Environment Errors
    ErrorCode.ENV_VAR_MISSING: "Set the required environment variable",
    ErrorCode.ENV_VAR_INVALID: "Update the environment variable with a valid value",
    ErrorCode.PYTHON_VERSION_UNSUPPORTED: "Use Python 3.8 or later",
    ErrorCode.GIT_NOT_INSTALLED: "Install Git using your system's package manager",
    ErrorCode.UV_NOT_INSTALLED: "Install UV using 'pip install uv'",
    
    # Package Structure Errors
    ErrorCode.PYPROJECT_NOT_FOUND: "Create a pyproject.toml file in the project root",
    ErrorCode.PYPROJECT_INVALID: "Fix the pyproject.toml file according to the PEP 621 specification",
    ErrorCode.SRC_DIR_NOT_FOUND: "Create a src directory in the project root",
    ErrorCode.PACKAGE_DIR_NOT_FOUND: "Create the package directory under src/",
    ErrorCode.INIT_PY_NOT_FOUND: "Create an __init__.py file in the package directory",
    ErrorCode.README_NOT_FOUND: "Create a README.md file in the project root",
    ErrorCode.LICENSE_NOT_FOUND: "Create a LICENSE file in the project root",
    ErrorCode.CHANGELOG_NOT_FOUND: "Create a CHANGELOG.md file in the project root",
    ErrorCode.TESTS_DIR_NOT_FOUND: "Create a tests directory in the project root",
    
    # Build Errors
    ErrorCode.BUILD_FAILED: "Check the build output for specific errors and fix them",
    ErrorCode.BUILD_INVALID_PACKAGE: "Ensure the package structure follows Python packaging standards",
    ErrorCode.BUILD_MISSING_DEPENDENCY: "Add the missing dependency to pyproject.toml",
    ErrorCode.BUILD_INVALID_ENTRY_POINT: "Fix the entry point configuration in pyproject.toml",
    ErrorCode.BUILD_INVALID_CLASSIFIERS: "Update classifiers to use valid PyPI classifiers",
    
    # Version Errors
    ErrorCode.VERSION_INVALID: "Use a valid semantic version (e.g., '1.0.0')",
    ErrorCode.VERSION_NOT_FOUND: "Add version string to the specified files",
    ErrorCode.VERSION_MISMATCH: "Ensure version strings match across all files",
    ErrorCode.VERSION_BUMP_FAILED: "Manually update version strings in the specified files",
    ErrorCode.VERSION_VALIDATION_ERROR: "Fix version validation errors",
    ErrorCode.VERSION_TAG_EXISTS: "Use a different version tag",
    
    # Git Errors
    ErrorCode.GIT_REPO_NOT_FOUND: "Initialize a Git repository with 'git init'",
    ErrorCode.GIT_REMOTE_NOT_FOUND: "Add a Git remote with 'git remote add origin <url>'",
    ErrorCode.GIT_PUSH_FAILED: "Ensure you have write access to the repository",
    ErrorCode.GIT_TAG_FAILED: "Ensure the tag doesn't already exist",
    ErrorCode.GIT_RELEASE_FAILED: "Check GitHub permissions and release settings",
    ErrorCode.GIT_DIRTY_WORKSPACE: "Commit or stash changes before proceeding",
    ErrorCode.GIT_VALIDATION_ERROR: "Fix Git validation errors",
    ErrorCode.GIT_INIT_FAILED: "Initialize Git repository",
    ErrorCode.GIT_COMMIT_FAILED: "Commit changes to Git",
    
    # PyPI Errors
    ErrorCode.PYPI_AUTH_FAILED: "Check your PyPI token and permissions",
    ErrorCode.PYPI_UPLOAD_FAILED: "Fix package build issues and try again",
    ErrorCode.PYPI_PACKAGE_EXISTS: "Bump the version number before publishing",
    ErrorCode.PYPI_INVALID_CREDENTIALS: "Update your PyPI credentials",
    ErrorCode.PYPI_VALIDATION_ERROR: "Fix PyPI validation errors",
    ErrorCode.PYPI_BUILD_FAILED: "Fix PyPI build issues and try again",
    
    # GitHub Errors
    ErrorCode.GITHUB_AUTH_FAILED: "Check your GitHub token and permissions",
    ErrorCode.GITHUB_REPO_EXISTS: "Use a different repository name or delete the existing one",
    ErrorCode.GITHUB_CREATE_FAILED: "Check your GitHub permissions and repository settings",
    ErrorCode.GITHUB_RELEASE_FAILED: "Ensure the tag exists and you have release permissions",
    ErrorCode.GITHUB_API_ERROR: "Check the GitHub API status and your request format",
    
    # Validation Errors
    ErrorCode.VALIDATION_FAILED: "Fix all validation errors before proceeding",
    ErrorCode.VALIDATION_PACKAGE_NAME: "Use a valid Python package name (lowercase, no spaces)",
    ErrorCode.VALIDATION_VERSION_FORMAT: "Use semantic versioning (MAJOR.MINOR.PATCH)",
    ErrorCode.VALIDATION_DEPENDENCIES: "Fix dependency specifications in pyproject.toml",
    ErrorCode.VALIDATION_ENTRY_POINTS: "Fix entry point configuration in pyproject.toml",
    ErrorCode.VALIDATION_CLASSIFIERS: "Use valid PyPI classifiers",
    
    # Testing Errors
    ErrorCode.TESTING_VALIDATION_ERROR: "Fix testing validation errors",
    ErrorCode.TEST_EXECUTION_FAILED: "Fix test execution errors",
    ErrorCode.DOCKER_BUILD_FAILED: "Fix Docker build issues",
    
    # Package Errors
    ErrorCode.PACKAGE_VALIDATION_ERROR: "Fix package validation errors",
    ErrorCode.PACKAGE_BUILD_FAILED: "Fix package build issues",
    ErrorCode.PACKAGE_PUBLISH_FAILED: "Fix package publish issues",
    
    # Changelog Errors
    ErrorCode.CHANGELOG_VALIDATION_ERROR: "Fix changelog validation errors",
    ErrorCode.CHANGELOG_GENERATION_FAILED: "Manually generate changelog",
    
    # Generic Errors
    ErrorCode.UNKNOWN_ERROR: "Check the error message and logs for more details",
    ErrorCode.OPERATION_CANCELLED: "Check the error message and logs for more details",
}


def handle_error(error: Exception) -> None:
    """Handle an error and provide helpful information."""
    import logging
    import traceback
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from python_release_master.core.templates import DEFAULT_CONFIG
    
    console = Console(stderr=True)
    log = logging.getLogger("python_release_master")
    
    if isinstance(error, ReleaseError):
        error_info = ErrorInfo(
            code=error.code,
            message=error.message,
            description=ERROR_DESCRIPTIONS[error.code],
            fix=ERROR_FIXES.get(error.code, "Fix the error according to the instructions below"),
            context=error.context,
        )
        
        title = Text()
        title.append("Error ", style="bold red")
        title.append(f"[{error_info.code.value}] ", style="dim")
        title.append(error_info.code.name, style="red")
        
        content = Text()
        content.append("Message: ", style="bold")
        content.append(f"{error_info.message}\n\n")
        content.append("Description: ", style="bold")
        content.append(f"{error_info.description}\n\n")
        
        if error.fix_instructions:
            content.append("How to fix:\n", style="bold green")
            for instruction in error.fix_instructions:
                content.append(f"  {instruction}\n")
        else:
            content.append("How to fix: ", style="bold green")
            content.append(error_info.fix)
        
        if error_info.context:
            content.append("\nContext:\n", style="bold")
            for key, value in error_info.context.items():
                content.append(f"  {key}: ", style="dim")
                content.append(f"{value}\n")
        
        if error.code == ErrorCode.CONFIG_NOT_FOUND:
            content.append("\nTemplate:\n", style="bold green")
            content.append(DEFAULT_CONFIG.format(
                module_name="your_package",
                package_name="your-package",
                owner="your-username",
                description="Your package description"
            ))
        
        console.print(Panel(content, title=title, border_style="red"))
        log.debug("Full traceback:", exc_info=True)
    else:
        console.print("[bold red]Unexpected Error![/]")
        console.print(Panel(
            "\n".join(traceback.format_exception(type(error), error, error.__traceback__)),
            title="[red]Traceback[/]",
            border_style="red",
        )) 