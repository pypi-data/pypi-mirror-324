"""Validation manager that combines all validation checks."""

import os
from pathlib import Path
from typing import Optional, List

from python_release_master.core.config import Config
from python_release_master.core.errors import ReleaseError, ErrorCode
from python_release_master.core.logger import logger
from python_release_master.core.validators import (
    PyProjectValidator,
    PackageStructureValidator,
    RequiredFilesValidator,
    DependencyValidator,
    EntryPointValidator,
    RepositoryValidator
)


class ValidationManager:
    """Manages all validation checks for the release process."""
    
    def __init__(self, config: Config, workspace_dir: Optional[Path] = None):
        """Initialize validation manager.
        
        Args:
            config: Configuration object
            workspace_dir: Optional workspace directory path
        """
        self.config = config
        self.workspace_dir = Path(workspace_dir or os.getcwd())
        self.repository_validator = RepositoryValidator(self.workspace_dir)
    
    def validate_environment(self) -> None:
        """Validate the environment before running operations.
        
        Raises:
            ReleaseError: If environment validation fails
        """
        logger.start_operation("Validating environment...")
        
        try:
            # Check for required environment variables
            if self.config.pypi.publish:
                pypi_token = os.environ.get(self.config.pypi.token_env_var)
                if not pypi_token:
                    raise ReleaseError(
                        code=ErrorCode.PYPI_TOKEN_MISSING,
                        message=f"{self.config.pypi.token_env_var} environment variable is required for publishing to PyPI",
                        context={"env_var": self.config.pypi.token_env_var}
                    )
                # Ensure the token will be available to UV
                if (self.config.pypi.uv_token_env_var not in os.environ and 
                    self.config.pypi.uv_token_env_var != self.config.pypi.token_env_var):
                    os.environ[self.config.pypi.uv_token_env_var] = pypi_token
            
            # Validate OpenAI configuration if AI-powered changelog is enabled
            if self.config.changelog.ai.enabled and "OPENAI_API_KEY" not in os.environ:
                raise ReleaseError(
                    code=ErrorCode.OPENAI_TOKEN_MISSING,
                    message="OPENAI_API_KEY environment variable is required for AI-powered changelog"
                )
            
            # Validate GitHub configuration if auto-create is enabled
            if self.config.github.auto_create and self.config.github.token_env_var not in os.environ:
                raise ReleaseError(
                    code=ErrorCode.GITHUB_TOKEN_MISSING,
                    message=f"{self.config.github.token_env_var} environment variable is required for GitHub auto-creation",
                    context={"env_var": self.config.github.token_env_var}
                )
            
            # Validate version files exist
            for file in self.config.version.files:
                if not Path(file).exists():
                    raise ReleaseError(
                        code=ErrorCode.VERSION_NOT_FOUND,
                        message=f"Version file not found: {file}",
                        context={"file": file},
                        fix_instructions=["Create the file or update version.files in config"]
                    )
            
            logger.success("Environment validation passed")
            
        except ReleaseError as e:
            logger.error("Environment validation failed")
            raise e
    
    def validate_package_structure(self) -> None:
        """Validate package structure and configuration.
        
        This combines both the new validators and existing package structure checks.
        
        Raises:
            ReleaseError: If package validation fails
        """
        logger.start_operation("Validating package structure...")
        
        try:
            # Run all validators from the repository validator
            self.repository_validator.validate()
            
            # Additional checks from existing validation
            # Check for tests directory
            if not (self.workspace_dir / "tests").exists():
                raise ReleaseError(
                    code=ErrorCode.PKG_STRUCTURE_INVALID,
                    message="No tests directory found",
                    fix_instructions=["Create tests directory"]
                )
            
            # Check for documentation
            if not (self.workspace_dir / "docs").exists():
                raise ReleaseError(
                    code=ErrorCode.PKG_STRUCTURE_INVALID,
                    message="No documentation directory found",
                    fix_instructions=["Create docs directory"]
                )
            
            logger.success("Package structure validation passed")
            
        except ReleaseError as e:
            logger.error("Package structure validation failed")
            raise e
    
    def validate_all(self) -> None:
        """Run all validation checks.
        
        This is the main entry point for validation before the release process.
        
        Raises:
            ReleaseError: If any validation fails
        """
        try:
            # Step 1: Environment validation
            self.validate_environment()
            
            # Step 2: Package structure validation
            self.validate_package_structure()
            
            logger.success("All validation checks passed")
            
        except ReleaseError as e:
            logger.error("Validation failed")
            raise e 