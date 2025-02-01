"""Base validator class for all validators."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional

from python_release_master.core.errors import ReleaseError


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
    
    def _load_pyproject_toml(self) -> Dict[str, Any]:
        """Load and parse pyproject.toml.
        
        Returns:
            Dict containing pyproject.toml contents
            
        Raises:
            ReleaseError: If file not found or invalid
        """
        import tomli
        
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