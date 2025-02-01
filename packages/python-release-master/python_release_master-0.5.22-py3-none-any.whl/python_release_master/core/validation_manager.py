"""Validation manager that combines all validation checks."""

import os
from pathlib import Path
from typing import Optional, List

from python_release_master.core.config import Config
from python_release_master.core.errors import ReleaseError, ErrorCode
from python_release_master.core.logger import logger
from python_release_master.core.validators.project import ProjectMetadataValidator
from python_release_master.core.validators.hatch import HatchBuildValidator
from python_release_master.core.validators.structure import ProjectStructureValidator


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
        self.validators = [
            ProjectMetadataValidator(self.workspace_dir),
            HatchBuildValidator(self.workspace_dir),
            ProjectStructureValidator(self.workspace_dir)
        ]
    
    def validate_environment(self) -> None:
        """Validate environment configuration.
        
        Raises:
            ReleaseError: If validation fails
        """
        try:
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
    
    def validate_all(self) -> None:
        """Run all validation checks.
        
        Raises:
            ReleaseError: If any validation fails
        """
        try:
            # Run environment validation first
            self.validate_environment()
            
            # Run all validators
            for validator in self.validators:
                logger.start_operation(f"Running {validator.__class__.__name__}...")
                validator.validate()
                logger.success(f"{validator.__class__.__name__} passed")
            
            logger.success("All validation checks passed")
            
        except ReleaseError as e:
            logger.error("Validation failed")
            raise e 