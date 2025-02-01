"""Project structure validator for Python Release Master."""

import re
from pathlib import Path
from typing import Dict, Any, List, Set

from python_release_master.core.errors import ErrorCode, ReleaseError
from python_release_master.core.validators.base import BaseValidator


class ProjectStructureValidator(BaseValidator):
    """Validates project directory structure and file organization."""
    
    # Required top-level files
    REQUIRED_FILES = {
        "pyproject.toml": "Project configuration and metadata",
        ".release-master.yaml": "Release master configuration",
        "README.md": "Project documentation",
        "LICENSE": "Project license",
        "CHANGELOG.md": "Project changelog",
        ".gitignore": "Git ignore patterns",
        "MANIFEST.in": "Package manifest configuration",
    }
    
    # Required directories with their purpose
    REQUIRED_DIRS = {
        "src": "Source code directory",
        "tests": "Test files directory",
        "docs": "Documentation directory",
        "scripts": "Utility scripts directory",
    }
    
    # Required files in docs directory
    REQUIRED_DOCS_FILES = {
        "Makefile": "Documentation build configuration",
        "make.bat": "Windows documentation build script",
        "source/conf.py": "Sphinx configuration",
        "source/index.rst": "Documentation index",
    }
    
    # Required documentation sections
    REQUIRED_DOCS_SECTIONS = {
        "installation.rst": "Installation guide",
        "quickstart.rst": "Quick start guide",
        "configuration.rst": "Configuration guide",
        "api_reference.rst": "API reference",
        "contributing.rst": "Contribution guide",
    }
    
    # Required test files
    REQUIRED_TEST_FILES = {
        "__init__.py": "Test package initialization",
        "test_basic.py": "Basic functionality tests",
        "test_config.py": "Configuration tests",
    }
    
    def _validate_file_exists(self, file_path: Path, description: str) -> None:
        """Validate that a file exists.
        
        Args:
            file_path: Path to file
            description: Description of file purpose
            
        Raises:
            ReleaseError: If file is missing
        """
        if not file_path.exists():
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                f"Missing required file: {file_path}",
                fix_instructions=[
                    f"Create {file_path} file",
                    f"Purpose: {description}",
                    "See documentation for file template and requirements"
                ]
            )
    
    def _validate_dir_exists(self, dir_path: Path, description: str) -> None:
        """Validate that a directory exists.
        
        Args:
            dir_path: Path to directory
            description: Description of directory purpose
            
        Raises:
            ReleaseError: If directory is missing
        """
        if not dir_path.exists():
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                f"Missing required directory: {dir_path}",
                fix_instructions=[
                    f"Create {dir_path} directory",
                    f"Purpose: {description}",
                    "Required structure:",
                    "  - See documentation for detailed layout"
                ]
            )
    
    def _validate_src_structure(self, package_name: str) -> None:
        """Validate src directory structure.
        
        Args:
            package_name: Package name from pyproject.toml
            
        Raises:
            ReleaseError: If structure is invalid
        """
        src_dir = self.workspace_dir / "src"
        pkg_dir = src_dir / package_name.replace("-", "_")
        
        # Required package files
        required_files = {
            "__init__.py": "Package initialization",
            "__main__.py": "CLI entry point",
            "cli.py": "CLI implementation",
        }
        
        # Required package directories
        required_dirs = {
            "core": "Core functionality"
        }
        
        # Validate package directory exists
        self._validate_dir_exists(pkg_dir, "Package source code")
        
        # Validate required files
        for file, desc in required_files.items():
            self._validate_file_exists(pkg_dir / file, desc)
        
        # Validate required directories
        for dir_name, desc in required_dirs.items():
            self._validate_dir_exists(pkg_dir / dir_name, desc)
        
        # Validate core module structure
        core_dir = pkg_dir / "core"
        core_files = {
            "__init__.py": "Core module initialization",
            "config.py": "Configuration handling",
            "errors.py": "Error definitions",
            "logger.py": "Logging functionality",
            "release.py": "Release management",
            "validation_manager.py": "Validation coordination",
            "version_manager.py": "Version management",
        }
        
        for file, desc in core_files.items():
            self._validate_file_exists(core_dir / file, desc)
        
        # Validate validators directory
        validators_dir = core_dir / "validators"
        self._validate_dir_exists(validators_dir, "Validation modules")
        
        validator_files = {
            "__init__.py": "Validators initialization",
            "base.py": "Base validator class",
            "project.py": "Project metadata validator",
            "hatch.py": "Hatch build validator",
            "structure.py": "Project structure validator",
        }
        
        for file, desc in validator_files.items():
            self._validate_file_exists(validators_dir / file, desc)
    
    def _validate_tests_structure(self) -> None:
        """Validate tests directory structure.
        
        Raises:
            ReleaseError: If structure is invalid
        """
        tests_dir = self.workspace_dir / "tests"
        self._validate_dir_exists(tests_dir, "Test files")
        
        for file, desc in self.REQUIRED_TEST_FILES.items():
            self._validate_file_exists(tests_dir / file, desc)
    
    def _validate_docs_structure(self) -> None:
        """Validate docs directory structure.
        
        Raises:
            ReleaseError: If structure is invalid
        """
        docs_dir = self.workspace_dir / "docs"
        self._validate_dir_exists(docs_dir, "Documentation")
        
        # Validate required files
        for file, desc in self.REQUIRED_DOCS_FILES.items():
            self._validate_file_exists(docs_dir / file, desc)
        
        # Validate required sections
        source_dir = docs_dir / "source"
        for file, desc in self.REQUIRED_DOCS_SECTIONS.items():
            self._validate_file_exists(source_dir / file, desc)
    
    def _validate_scripts_structure(self) -> None:
        """Validate scripts directory structure.
        
        Raises:
            ReleaseError: If structure is invalid
        """
        scripts_dir = self.workspace_dir / "scripts"
        self._validate_dir_exists(scripts_dir, "Utility scripts")
        
        # At least one utility script should exist
        if not any(scripts_dir.glob("*.py")):
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                "No utility scripts found in scripts directory",
                fix_instructions=[
                    "Add at least one utility script to scripts directory",
                    "Common scripts:",
                    "- validate.py: Custom validation script",
                    "- setup.py: Environment setup script",
                    "- clean.py: Cleanup script"
                ]
            )
    
    def validate(self) -> None:
        """Validate project structure.
        
        Raises:
            ReleaseError: If validation fails
        """
        # Step 1: Validate required top-level files
        for file, desc in self.REQUIRED_FILES.items():
            self._validate_file_exists(self.workspace_dir / file, desc)
        
        # Step 2: Validate required directories exist
        for dir_name, desc in self.REQUIRED_DIRS.items():
            self._validate_dir_exists(self.workspace_dir / dir_name, desc)
        
        # Step 3: Get package name from pyproject.toml
        config = self._load_pyproject_toml()
        package_name = config["project"]["name"]
        
        # Step 4: Validate src directory structure
        self._validate_src_structure(package_name)
        
        # Step 5: Validate tests directory structure
        self._validate_tests_structure()
        
        # Step 6: Validate docs directory structure
        self._validate_docs_structure()
        
        # Step 7: Validate scripts directory structure
        self._validate_scripts_structure()
        
        # Step 8: Validate no stray files in root
        allowed_patterns = {
            *self.REQUIRED_FILES.keys(),
            "*.txt",  # Allow text files for notes
            "*.yaml", "*.yml",  # Allow YAML files
            "Dockerfile",  # Allow Dockerfile
            "requirements.txt",  # Allow requirements file
            ".dockerignore",  # Allow Docker ignore file
        }
        
        root_files = {f.name for f in self.workspace_dir.glob("*") if f.is_file()}
        unexpected_files = root_files - {
            f for pattern in allowed_patterns
            for f in {str(f) for f in self.workspace_dir.glob(pattern)}
        }
        
        if unexpected_files:
            raise ReleaseError(
                ErrorCode.PKG_STRUCTURE_INVALID,
                "Unexpected files found in project root",
                context={"files": list(unexpected_files)},
                fix_instructions=[
                    "Remove or move unexpected files:",
                    *[f"- {f}" for f in unexpected_files],
                    "",
                    "Files should be organized into appropriate directories:",
                    "- Source code -> src/",
                    "- Tests -> tests/",
                    "- Documentation -> docs/",
                    "- Scripts -> scripts/"
                ]
            ) 