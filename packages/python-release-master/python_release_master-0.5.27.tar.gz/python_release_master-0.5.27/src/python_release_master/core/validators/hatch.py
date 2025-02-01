"""Validator for hatch build configuration in pyproject.toml."""

from pathlib import Path
from typing import Dict, Any, List

from python_release_master.core.errors import ErrorCode, ReleaseError
from python_release_master.core.validators.base import BaseValidator


class HatchBuildValidator(BaseValidator):
    """Validates hatch build configuration in pyproject.toml."""
    
    REQUIRED_SECTIONS = [
        "tool.hatch.build",
        "tool.hatch.build.targets.wheel",
        "tool.hatch.build.targets.wheel.sources"
    ]
    
    REQUIRED_BUILD_FIELDS = [
        "include",
        "packages"
    ]
    
    REQUIRED_WHEEL_FIELDS = [
        "packages"
    ]
    
    REQUIRED_SOURCES_FIELDS = [
        "src"
    ]
    
    def _validate_build_section(self, config: Dict[str, Any]) -> None:
        """Validate the [tool.hatch.build] section.
        
        Args:
            config: pyproject.toml configuration
            
        Raises:
            ReleaseError: If validation fails
        """
        build_config = config.get("tool", {}).get("hatch", {}).get("build", {})
        
        # Check required fields
        for field in self.REQUIRED_BUILD_FIELDS:
            if field not in build_config:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_FIELD,
                    f"Missing required field '{field}' in [tool.hatch.build] section",
                    fix_instructions=[
                        "Add the following to your pyproject.toml:",
                        "",
                        "[tool.hatch.build]",
                        "include = [",
                        '    "src/{package_name}/**/*.py",',
                        '    "src/{package_name}/**/*.pyi",',
                        '    "tests/**/*.py",',
                        "]",
                        'packages = ["src"]'
                    ]
                )
        
        # Validate includes
        includes = build_config.get("include", [])
        if not isinstance(includes, list):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "The 'include' field must be a list",
                fix_instructions=[
                    "Update the include field to be a list:",
                    "[tool.hatch.build]",
                    "include = [",
                    '    "src/{package_name}/**/*.py",',
                    '    "src/{package_name}/**/*.pyi",',
                    "]"
                ]
            )
        
        # Get package name from config
        package_name = config["project"]["name"].replace("-", "_")
        
        # Required include patterns
        required_patterns = [
            f"src/{package_name}/**/*.py",
            f"src/{package_name}/**/*.pyi",
        ]
        
        # Check for missing patterns
        missing_patterns = [pat for pat in required_patterns if pat not in includes]
        if missing_patterns:
            raise ReleaseError(
                ErrorCode.CONFIG_MISSING_FIELD,
                "Missing required include patterns",
                fix_instructions=[
                    "Add the following patterns to your includes:",
                    "[tool.hatch.build]",
                    "include = [",
                    *[f'    "{pat}",' for pat in required_patterns],
                    '    "tests/**/*.py",  # Optional but recommended',
                    "]"
                ]
            )
        
        # Validate packages
        packages = build_config.get("packages", [])
        if not isinstance(packages, list) or "src" not in packages:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "The 'packages' field must be a list containing 'src'",
                fix_instructions=[
                    "Update the packages field:",
                    "[tool.hatch.build]",
                    'packages = ["src"]'
                ]
            )
    
    def _validate_wheel_section(self, config: Dict[str, Any]) -> None:
        """Validate the [tool.hatch.build.targets.wheel] section.
        
        Args:
            config: pyproject.toml configuration
            
        Raises:
            ReleaseError: If validation fails
        """
        wheel_config = config.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
        
        # Check required fields
        for field in self.REQUIRED_WHEEL_FIELDS:
            if field not in wheel_config:
                raise ReleaseError(
                    ErrorCode.CONFIG_MISSING_FIELD,
                    f"Missing required field '{field}' in [tool.hatch.build.targets.wheel] section",
                    fix_instructions=[
                        "Add the following to your pyproject.toml:",
                        "",
                        "[tool.hatch.build.targets.wheel]",
                        'packages = ["src"]'
                    ]
                )
        
        # Validate packages
        packages = wheel_config.get("packages", [])
        if not isinstance(packages, list) or "src" not in packages:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "The 'packages' field must be a list containing 'src'",
                fix_instructions=[
                    "Update the packages field:",
                    "[tool.hatch.build.targets.wheel]",
                    'packages = ["src"]'
                ]
            )
    
    def _validate_sources_section(self, config: Dict[str, Any]) -> None:
        """Validate the [tool.hatch.build.targets.wheel.sources] section.
        
        Args:
            config: pyproject.toml configuration
            
        Raises:
            ReleaseError: If validation fails
        """
        sources_config = (
            config.get("tool", {})
            .get("hatch", {})
            .get("build", {})
            .get("targets", {})
            .get("wheel", {})
            .get("sources", {})
        )
        
        # Get package name
        package_name = config["project"]["name"].replace("-", "_")
        
        # Check src mapping
        if "src" not in sources_config or sources_config["src"] != package_name:
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                f"Invalid source mapping for 'src' in [tool.hatch.build.targets.wheel.sources]",
                fix_instructions=[
                    "Update the sources mapping:",
                    "[tool.hatch.build.targets.wheel.sources]",
                    f'"src" = "{package_name}"'
                ]
            )
    
    def validate(self) -> None:
        """Validate hatch build configuration.
        
        Raises:
            ReleaseError: If validation fails
        """
        config = self._load_pyproject_toml()
        
        # Check if using hatch as build backend
        build_backend = config.get("build-system", {}).get("build-backend", "")
        if not build_backend.startswith("hatchling"):
            raise ReleaseError(
                ErrorCode.CONFIG_INVALID_VALUE,
                "Hatch build configuration requires hatchling build backend",
                fix_instructions=[
                    "Update your build-system section:",
                    "[build-system]",
                    'requires = ["hatchling"]',
                    'build-backend = "hatchling.build"'
                ]
            )
        
        # Validate each section
        self._validate_build_section(config)
        self._validate_wheel_section(config)
        self._validate_sources_section(config) 