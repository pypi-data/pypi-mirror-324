"""Error handling for Python Release Master."""

from enum import Enum
from typing import List, Optional, Any
from dataclasses import dataclass


class ErrorCode(Enum):
    """Error codes for Python Release Master."""
    
    # Configuration Errors (1000-1999)
    CONFIG_NOT_FOUND = 1000
    CONFIG_INVALID = 1001
    CONFIG_MISSING_FIELD = 1002
    CONFIG_VALIDATION_ERROR = 1003
    CONFIG_PARSE_ERROR = 1004
    
    # Version Errors (2000-2999)
    VERSION_NOT_FOUND = 2000
    VERSION_INVALID = 2001
    VERSION_MISMATCH = 2002
    VERSION_BUMP_FAILED = 2003
    VERSION_VALIDATION_ERROR = 2004
    
    # Changelog Errors (3000-3999)
    CHANGELOG_NOT_FOUND = 3000
    CHANGELOG_INVALID = 3001
    CHANGELOG_GENERATION_FAILED = 3002
    CHANGELOG_VALIDATION_ERROR = 3003
    
    # Build Errors (4000-4999)
    BUILD_FAILED = 4000
    BUILD_VALIDATION_ERROR = 4001
    BUILD_MISSING_DEPENDENCIES = 4002
    BUILD_INVALID_CLASSIFIERS = 4003
    BUILD_INVALID_METADATA = 4004
    
    # Environment Errors (5000-5999)
    ENV_MISSING_VARIABLE = 5000
    ENV_VALIDATION_ERROR = 5001
    ENV_MISSING_DEPENDENCY = 5002
    ENV_INVALID_PYTHON = 5003
    ENV_INVALID_VIRTUALENV = 5004
    
    # Git Errors (6000-6999)
    GIT_NOT_INSTALLED = 6000
    GIT_REPO_NOT_FOUND = 6001
    GIT_PUSH_FAILED = 6002
    GIT_TAG_FAILED = 6003
    GIT_RELEASE_FAILED = 6004
    GIT_DIRTY_WORKSPACE = 6005
    GIT_VALIDATION_ERROR = 6006
    GIT_INIT_FAILED = 6007
    GIT_COMMIT_FAILED = 6008
    
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
    
    # Generic Errors (99000-99999)
    UNKNOWN_ERROR = 99000
    OPERATION_CANCELLED = 99001


class ReleaseError(Exception):
    """Base exception class for Python Release Master."""
    
    def __init__(self, code: ErrorCode, message: str, context: Optional[dict] = None,
                 fix_instructions: Optional[List[str]] = None, cause: Optional[Exception] = None):
        """Initialize release error.
        
        Args:
            code: Error code
            message: Error message
            context: Optional error context
            fix_instructions: Optional list of fix instructions
            cause: Optional cause exception
        """
        self.code = code
        self.message = message
        self.context = context or {}
        self.fix_instructions = fix_instructions or []
        self.cause = cause
        super().__init__(message)


@dataclass
class ErrorInfo:
    """Error information for better error reporting."""
    code: ErrorCode
    message: str
    description: str
    fix: List[str]
    context: Optional[dict] = None


# Error messages for each error code
ERROR_MESSAGES = {
    # Configuration Errors
    ErrorCode.CONFIG_NOT_FOUND: "Configuration file not found",
    ErrorCode.CONFIG_INVALID: "Invalid configuration",
    ErrorCode.CONFIG_MISSING_FIELD: "Missing required configuration field",
    ErrorCode.CONFIG_VALIDATION_ERROR: "Configuration validation error",
    ErrorCode.CONFIG_PARSE_ERROR: "Failed to parse configuration file",
    
    # Version Errors
    ErrorCode.VERSION_NOT_FOUND: "Version not found",
    ErrorCode.VERSION_INVALID: "Invalid version format",
    ErrorCode.VERSION_MISMATCH: "Version mismatch between files",
    ErrorCode.VERSION_BUMP_FAILED: "Failed to bump version",
    ErrorCode.VERSION_VALIDATION_ERROR: "Version validation error",
    
    # Changelog Errors
    ErrorCode.CHANGELOG_NOT_FOUND: "Changelog not found",
    ErrorCode.CHANGELOG_INVALID: "Invalid changelog format",
    ErrorCode.CHANGELOG_GENERATION_FAILED: "Failed to generate changelog",
    ErrorCode.CHANGELOG_VALIDATION_ERROR: "Changelog validation error",
    
    # Build Errors
    ErrorCode.BUILD_FAILED: "Build failed",
    ErrorCode.BUILD_VALIDATION_ERROR: "Build validation error",
    ErrorCode.BUILD_MISSING_DEPENDENCIES: "Missing build dependencies",
    ErrorCode.BUILD_INVALID_CLASSIFIERS: "Invalid classifiers",
    ErrorCode.BUILD_INVALID_METADATA: "Invalid package metadata",
    
    # Environment Errors
    ErrorCode.ENV_MISSING_VARIABLE: "Missing environment variable",
    ErrorCode.ENV_VALIDATION_ERROR: "Environment validation error",
    ErrorCode.ENV_MISSING_DEPENDENCY: "Missing system dependency",
    ErrorCode.ENV_INVALID_PYTHON: "Invalid Python version",
    ErrorCode.ENV_INVALID_VIRTUALENV: "Invalid virtual environment",
    
    # Git Errors
    ErrorCode.GIT_NOT_INSTALLED: "Git is not installed",
    ErrorCode.GIT_REPO_NOT_FOUND: "Git repository not found",
    ErrorCode.GIT_PUSH_FAILED: "Failed to push changes",
    ErrorCode.GIT_TAG_FAILED: "Failed to create tag",
    ErrorCode.GIT_RELEASE_FAILED: "Failed to create release",
    ErrorCode.GIT_DIRTY_WORKSPACE: "Workspace has uncommitted changes",
    ErrorCode.GIT_VALIDATION_ERROR: "Git validation error",
    ErrorCode.GIT_INIT_FAILED: "Failed to initialize Git repository",
    ErrorCode.GIT_COMMIT_FAILED: "Failed to create commit",
    
    # GitHub Errors
    ErrorCode.GITHUB_AUTH_FAILED: "GitHub authentication failed",
    ErrorCode.GITHUB_REPO_EXISTS: "GitHub repository already exists",
    ErrorCode.GITHUB_CREATE_FAILED: "Failed to create GitHub repository",
    ErrorCode.GITHUB_RELEASE_FAILED: "Failed to create GitHub release",
    ErrorCode.GITHUB_API_ERROR: "GitHub API error",
    
    # Validation Errors
    ErrorCode.VALIDATION_FAILED: "Validation failed",
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
    
    # Generic Errors
    ErrorCode.UNKNOWN_ERROR: "Unknown error occurred",
    ErrorCode.OPERATION_CANCELLED: "Operation cancelled by user"
}


# Fix instructions for each error code
FIX_INSTRUCTIONS = {
    # Configuration Errors
    ErrorCode.CONFIG_NOT_FOUND: [
        "Create a .release-master.yaml file in your project root",
        "Use the default configuration template"
    ],
    ErrorCode.CONFIG_INVALID: [
        "Check your configuration syntax",
        "Compare against the default configuration template"
    ],
    ErrorCode.CONFIG_MISSING_FIELD: [
        "Add the missing field to your configuration",
        "Check the documentation for required fields"
    ],
    
    # Version Errors
    ErrorCode.VERSION_NOT_FOUND: [
        "Add version string to your package",
        "Update version.files in configuration"
    ],
    ErrorCode.VERSION_INVALID: [
        "Use semantic versioning (MAJOR.MINOR.PATCH)",
        "Check version string format"
    ],
    ErrorCode.VERSION_MISMATCH: [
        "Update all version strings to match",
        "Check version.files in configuration"
    ],
    
    # Build Errors
    ErrorCode.BUILD_FAILED: [
        "Check build dependencies",
        "Verify package structure"
    ],
    ErrorCode.BUILD_MISSING_DEPENDENCIES: [
        "Install required build dependencies",
        "Check your build-system.requires in pyproject.toml"
    ],
    ErrorCode.BUILD_INVALID_CLASSIFIERS: [
        "Update classifiers to use valid classifiers",
        "Check against the official classifier list"
    ],
    
    # Git Errors
    ErrorCode.GIT_NOT_INSTALLED: [
        "Install Git on your system",
        "Add Git to your system PATH"
    ],
    ErrorCode.GIT_REPO_NOT_FOUND: [
        "Initialize Git repository",
        "Check if .git directory exists"
    ],
    ErrorCode.GIT_PUSH_FAILED: [
        "Check remote repository configuration",
        "Verify Git credentials"
    ],
    
    # GitHub Errors
    ErrorCode.GITHUB_AUTH_FAILED: [
        "Check GitHub token permissions",
        "Verify token is set in environment"
    ],
    ErrorCode.GITHUB_CREATE_FAILED: [
        "Check repository name availability",
        "Verify GitHub token permissions"
    ],
    
    # Testing Errors
    ErrorCode.TEST_EXECUTION_FAILED: [
        "Check test dependencies",
        "Run tests locally to debug"
    ],
    ErrorCode.DOCKER_BUILD_FAILED: [
        "Check Docker configuration",
        "Verify Docker is running"
    ],
    
    # Generic Errors
    ErrorCode.UNKNOWN_ERROR: [
        "Check the error message for details",
        "Report the issue if it persists"
    ],
    ErrorCode.OPERATION_CANCELLED: [
        "Re-run the command to try again",
        "Check if any cleanup is needed"
    ]
}


def handle_error(error: Exception) -> None:
    """Handle an error and provide helpful information."""
    import logging
    import traceback
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    
    console = Console(stderr=True)
    log = logging.getLogger("python_release_master")
    
    if isinstance(error, ReleaseError):
        # Create error info
        error_info = ErrorInfo(
            code=error.code,
            message=error.message,
            description=ERROR_MESSAGES.get(error.code, "No description available"),
            fix=error.fix_instructions or FIX_INSTRUCTIONS.get(error.code, ["No fix instructions available"]),
            context=error.context
        )
        
        # Create title
        title = Text()
        title.append("Release Error ", style="bold red")
        title.append(f"[{error_info.code.value}] ", style="dim")
        title.append(error_info.code.name, style="red")
        
        # Create content
        content = Text()
        
        # Add message section
        content.append("\n🚫 Error Message:\n", style="bold red")
        content.append(f"   {error_info.message}\n\n")
        
        # Add description section
        content.append("📝 Description:\n", style="bold yellow")
        content.append(f"   {error_info.description}\n\n")
        
        # Add fix instructions section
        content.append("🔧 How to Fix:\n", style="bold green")
        for instruction in error_info.fix:
            content.append(f"   • {instruction}\n")
        
        # Add context section if available
        if error_info.context:
            content.append("\n🔍 Additional Context:\n", style="bold blue")
            for key, value in error_info.context.items():
                content.append(f"   • {key}: ", style="bold")
                content.append(f"{value}\n")
        
        # Add note for external repos if it's a version mismatch
        if error.code == ErrorCode.VERSION_MISMATCH:
            content.append("\n⚠️  Note for External Repositories:\n", style="bold magenta")
            content.append("   If you're running this on an external repository, ensure you have permission\n")
            content.append("   to modify its version files. If not, you may need to:\n")
            content.append("   • Fork the repository first\n")
            content.append("   • Get necessary permissions\n")
            content.append("   • Or contact the repository maintainers\n")
        
        # Create and print panel
        panel = Panel(
            content,
            title=title,
            border_style="red",
            padding=(1, 2)
        )
        console.print(panel)
        
        # Log debug information if available
        if error.cause:
            log.debug("Original error:", exc_info=error.cause)
    
    else:
        # Handle unexpected errors
        console.print("[bold red]Unexpected Error![/]")
        error_panel = Panel(
            "\n".join(traceback.format_exception(type(error), error, error.__traceback__)),
            title="[red]Traceback[/]",
            border_style="red"
        )
        console.print(error_panel) 