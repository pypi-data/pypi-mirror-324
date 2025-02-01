"""Centralized error handling for Python Release Master."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Dict, Any

from python_release_master.core.logger import logger

class ErrorCode(Enum):
    """Error codes for Python Release Master."""
    
    # Configuration Errors (1000-1999)
    CONFIG_NOT_FOUND = 1001
    CONFIG_INVALID = 1002
    CONFIG_MISSING_REQUIRED = 1003
    
    # Environment Errors (2000-2999)
    ENV_VAR_MISSING = 2001
    ENV_VAR_INVALID = 2002
    PYPI_TOKEN_MISSING = 2003
    GITHUB_TOKEN_MISSING = 2004
    OPENAI_TOKEN_MISSING = 2005
    
    # Package Structure Errors (3000-3999)
    PKG_STRUCTURE_INVALID = 3001
    PKG_FILE_MISSING = 3002
    PKG_FILE_INVALID = 3003
    
    # Version Management Errors (4000-4999)
    VERSION_NOT_FOUND = 4001
    VERSION_INVALID = 4002
    VERSION_UPDATE_FAILED = 4003
    
    # Git Errors (5000-5999)
    GIT_NOT_INITIALIZED = 5001
    GIT_REMOTE_ERROR = 5002
    GIT_TAG_ERROR = 5003
    GIT_PUSH_ERROR = 5004
    
    # GitHub Errors (6000-6999)
    GITHUB_API_ERROR = 6001
    GITHUB_REPO_EXISTS = 6002
    GITHUB_REPO_CREATE_ERROR = 6003
    GITHUB_RELEASE_ERROR = 6004
    
    # PyPI Errors (7000-7999)
    PYPI_BUILD_ERROR = 7001
    PYPI_PUBLISH_ERROR = 7002
    PYPI_AUTH_ERROR = 7003
    
    # AI/OpenAI Errors (8000-8999)
    AI_API_ERROR = 8001
    AI_INVALID_RESPONSE = 8002
    AI_RATE_LIMIT = 8003
    
    # System Errors (9000-9999)
    SYSTEM_IO_ERROR = 9001
    SYSTEM_PERMISSION_ERROR = 9002
    SYSTEM_COMMAND_ERROR = 9003
    
    # Unknown/Unexpected Errors (9999)
    UNKNOWN_ERROR = 9999

@dataclass
class ErrorInfo:
    """Error information with description and fix instructions."""
    code: ErrorCode
    message: str
    description: str
    fix_instructions: List[str]
    context: Optional[Dict[str, Any]] = None

class ReleaseError(Exception):
    """Base exception class for Python Release Master."""
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        description: Optional[str] = None,
        fix_instructions: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        """Initialize error.
        
        Args:
            code: Error code
            message: Error message
            description: Optional detailed description
            fix_instructions: Optional list of fix instructions
            context: Optional error context
            cause: Optional causing exception
        """
        self.error_info = ErrorInfo(
            code=code,
            message=message,
            description=description or ERROR_DESCRIPTIONS.get(code, "No description available."),
            fix_instructions=fix_instructions or ERROR_FIXES.get(code, ["No fix instructions available."]),
            context=context or {}
        )
        self.cause = cause
        super().__init__(message)

# Error descriptions
ERROR_DESCRIPTIONS = {
    ErrorCode.CONFIG_NOT_FOUND: "Configuration file (.release-master.yaml) was not found in the specified location.",
    ErrorCode.CONFIG_INVALID: "Configuration file contains invalid or malformed data.",
    ErrorCode.CONFIG_MISSING_REQUIRED: "Configuration is missing required fields.",
    
    ErrorCode.ENV_VAR_MISSING: "Required environment variable is not set.",
    ErrorCode.ENV_VAR_INVALID: "Environment variable contains invalid value.",
    ErrorCode.PYPI_TOKEN_MISSING: "PyPI API token is not set in environment variables.",
    ErrorCode.GITHUB_TOKEN_MISSING: "GitHub API token is not set in environment variables.",
    ErrorCode.OPENAI_TOKEN_MISSING: "OpenAI API token is not set in environment variables.",
    
    ErrorCode.PKG_STRUCTURE_INVALID: "Package structure does not match expected layout.",
    ErrorCode.PKG_FILE_MISSING: "Required package file is missing.",
    ErrorCode.PKG_FILE_INVALID: "Package file contains invalid or malformed data.",
    
    ErrorCode.VERSION_NOT_FOUND: "Version string could not be found in specified files.",
    ErrorCode.VERSION_INVALID: "Version string is not in valid semantic versioning format.",
    ErrorCode.VERSION_UPDATE_FAILED: "Failed to update version in one or more files.",
    
    ErrorCode.GIT_NOT_INITIALIZED: "Git repository is not initialized.",
    ErrorCode.GIT_REMOTE_ERROR: "Error communicating with Git remote.",
    ErrorCode.GIT_TAG_ERROR: "Error creating or pushing Git tag.",
    ErrorCode.GIT_PUSH_ERROR: "Error pushing changes to Git remote.",
    
    ErrorCode.GITHUB_API_ERROR: "Error communicating with GitHub API.",
    ErrorCode.GITHUB_REPO_EXISTS: "GitHub repository already exists.",
    ErrorCode.GITHUB_REPO_CREATE_ERROR: "Error creating GitHub repository.",
    ErrorCode.GITHUB_RELEASE_ERROR: "Error creating GitHub release.",
    
    ErrorCode.PYPI_BUILD_ERROR: "Error building Python package.",
    ErrorCode.PYPI_PUBLISH_ERROR: "Error publishing package to PyPI.",
    ErrorCode.PYPI_AUTH_ERROR: "PyPI authentication failed.",
    
    ErrorCode.AI_API_ERROR: "Error communicating with AI API.",
    ErrorCode.AI_INVALID_RESPONSE: "AI API returned invalid or unexpected response.",
    ErrorCode.AI_RATE_LIMIT: "AI API rate limit exceeded.",
    
    ErrorCode.SYSTEM_IO_ERROR: "System I/O operation failed.",
    ErrorCode.SYSTEM_PERMISSION_ERROR: "Insufficient system permissions.",
    ErrorCode.SYSTEM_COMMAND_ERROR: "System command execution failed.",
    
    ErrorCode.UNKNOWN_ERROR: "An unexpected error occurred.",
}

# Error fix instructions
ERROR_FIXES = {
    ErrorCode.CONFIG_NOT_FOUND: [
        "Create a .release-master.yaml file in your project root",
        "Run 'python-release-master init' to create a default configuration",
        "Check if you're in the correct directory"
    ],
    ErrorCode.CONFIG_INVALID: [
        "Check the configuration file syntax",
        "Validate against the configuration schema",
        "Remove any invalid or unsupported options"
    ],
    ErrorCode.CONFIG_MISSING_REQUIRED: [
        "Add the missing required fields to your configuration",
        "Check the documentation for required configuration options"
    ],
    
    ErrorCode.ENV_VAR_MISSING: [
        "Set the required environment variable",
        "Add it to your shell profile or .env file",
        "Use a secrets management solution"
    ],
    ErrorCode.ENV_VAR_INVALID: [
        "Check the environment variable value format",
        "Ensure the value meets the required specifications"
    ],
    ErrorCode.PYPI_TOKEN_MISSING: [
        "Create a PyPI API token at https://pypi.org/manage/account/token/",
        "Set the token in the specified environment variable",
        "Check the token environment variable name in your configuration"
    ],
    ErrorCode.GITHUB_TOKEN_MISSING: [
        "Create a GitHub token at https://github.com/settings/tokens",
        "Ensure the token has the required permissions",
        "Set the token in the specified environment variable"
    ],
    ErrorCode.OPENAI_TOKEN_MISSING: [
        "Create an OpenAI API key at https://platform.openai.com/api-keys",
        "Set OPENAI_API_KEY environment variable",
        "Or disable AI features in your configuration"
    ],
    
    # ... Add more fix instructions for other error codes ...
}

def handle_error(error: Exception) -> None:
    """Handle errors in a centralized way.
    
    Args:
        error: Exception to handle
    """
    if isinstance(error, ReleaseError):
        info = error.error_info
        context_str = ""
        if info.context:
            context_str = "\nContext:\n" + "\n".join(f"  {k}: {v}" for k, v in info.context.items())
        
        message = (
            f"Error {info.code.value}: {info.message}\n\n"
            f"Description:\n  {info.description}\n\n"
            f"To fix:{context_str}\n"
            + "\n".join(f"  - {fix}" for fix in info.fix_instructions)
        )
        
        if error.cause:
            message += f"\n\nCaused by: {str(error.cause)}"
        
        logger.panel(message, f"Error {info.code.value}", "red")
    else:
        # Handle unexpected errors
        message = (
            f"An unexpected error occurred: {str(error)}\n\n"
            "This is likely a bug. Please report it with the following information:\n"
            f"  - Error type: {type(error).__name__}\n"
            f"  - Error message: {str(error)}\n"
            "  - Full traceback (see logs)\n"
            "\nTo report this issue:\n"
            "  1. Go to https://github.com/kareemaly/python-release-master/issues\n"
            "  2. Click 'New Issue'\n"
            "  3. Include the error information above\n"
            "  4. Include steps to reproduce the error"
        )
        logger.panel(message, "Unexpected Error", "red")
    
    raise SystemExit(1) 