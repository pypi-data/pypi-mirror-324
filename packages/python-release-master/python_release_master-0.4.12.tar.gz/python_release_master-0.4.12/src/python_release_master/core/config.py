"""Configuration management for Python Release Master."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any

import yaml

from python_release_master.core.errors import ReleaseError, ErrorCode
from python_release_master.core.templates import DEFAULT_CONFIG


@dataclass
class VersionConfig:
    """Version configuration."""
    files: List[str]
    pattern: str = r'\d+\.\d+\.\d+'


@dataclass
class AIConfig:
    """AI configuration."""
    enabled: bool = True
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    response_format: Dict[str, str] = None

    def __post_init__(self):
        """Set default response format and validate model."""
        if self.response_format is None:
            self.response_format = {"type": "json_object"}
        
        # Enforce gpt-4o-mini model
        if self.model != "gpt-4o-mini":
            raise ReleaseError(
                code=ErrorCode.CONFIG_INVALID,
                message=f"Invalid AI model: {self.model}. Only gpt-4o-mini is supported.",
                fix_instructions=[
                    "Set changelog.ai.model to 'gpt-4o-mini' in your .release-master.yaml",
                    "This model is required for consistent and reliable outputs"
                ]
            )


@dataclass
class ChangelogConfig:
    """Changelog configuration."""
    ai: AIConfig
    sections: List[str]
    commit_conventions: Dict[str, str]


@dataclass
class GitReleaseConfig:
    """Git release configuration."""
    enabled: bool = True
    draft: bool = False
    prerelease: bool = False
    generate_notes: bool = True


@dataclass
class GitConfig:
    """Git configuration."""
    push: bool = True
    tag_prefix: str = "v"
    release: GitReleaseConfig = None

    def __post_init__(self):
        """Set default release config."""
        if self.release is None:
            self.release = GitReleaseConfig()


@dataclass
class PyPIConfig:
    """PyPI configuration."""
    publish: bool = True
    repository: str = "pypi"
    token_env_var: str = "PYPI_TOKEN"  # Default to PYPI_TOKEN for backward compatibility
    uv_token_env_var: str = "UV_PUBLISH_TOKEN"  # UV-specific token env var


@dataclass
class DockerConfig:
    """Docker configuration."""
    enabled: bool = True
    python_version: str = "3.9"
    base_image: str = "python:3.9-slim"


@dataclass
class TestingConfig:
    """Testing configuration."""
    run_before_release: bool = True
    docker: DockerConfig = None

    def __post_init__(self):
        """Set default docker config."""
        if self.docker is None:
            self.docker = DockerConfig()


@dataclass
class GitHubConfig:
    """GitHub configuration."""
    auto_create: bool = False
    owner: Optional[str] = None
    repo_name: Optional[str] = None
    private: bool = False
    description: Optional[str] = None
    token_env_var: str = "GITHUB_TOKEN"


@dataclass
class Config:
    """Main configuration."""
    version: VersionConfig
    changelog: ChangelogConfig
    git: GitConfig
    pypi: PyPIConfig
    testing: TestingConfig
    github: GitHubConfig

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create config from dictionary.
        
        Args:
            data: Configuration dictionary
        
        Returns:
            Config object
        
        Raises:
            ReleaseError: If configuration is invalid
        """
        try:
            version = VersionConfig(**data.get("version", {}))
            
            ai_config = AIConfig(**data.get("changelog", {}).get("ai", {}))
            changelog = ChangelogConfig(
                ai=ai_config,
                sections=data.get("changelog", {}).get("sections", []),
                commit_conventions=data.get("changelog", {}).get("commit_conventions", {})
            )
            
            git_release = GitReleaseConfig(**data.get("git", {}).get("release", {}))
            git = GitConfig(
                push=data.get("git", {}).get("push", True),
                tag_prefix=data.get("git", {}).get("tag_prefix", "v"),
                release=git_release
            )
            
            pypi = PyPIConfig(**data.get("pypi", {}))
            
            docker = DockerConfig(**data.get("testing", {}).get("docker", {}))
            testing = TestingConfig(
                run_before_release=data.get("testing", {}).get("run_before_release", True),
                docker=docker
            )
            
            github = GitHubConfig(**data.get("github", {}))
            
            return cls(
                version=version,
                changelog=changelog,
                git=git,
                pypi=pypi,
                testing=testing,
                github=github
            )
        except (TypeError, ValueError) as e:
            raise ReleaseError(
                code=ErrorCode.CONFIG_INVALID,
                message=f"Invalid configuration: {e}",
                fix_instructions=[
                    "Check your configuration against the template below:",
                    "",
                    DEFAULT_CONFIG
                ]
            )


def load_config(path: str = ".") -> Config:
    """Load configuration from file.
    
    Args:
        path: Path to configuration file or directory
    
    Returns:
        Config object
    
    Raises:
        ReleaseError: If configuration file is not found or is invalid
    """
    config_path = Path(path)
    if config_path.is_dir():
        config_path = config_path / ".release-master.yaml"
    
    if not config_path.exists():
        raise ReleaseError(
            code=ErrorCode.CONFIG_NOT_FOUND,
            message=f"Configuration file not found: {config_path}",
            fix_instructions=[
                "Create a .release-master.yaml file in your project root with the following template:",
                "",
                DEFAULT_CONFIG
            ]
        )
    
    try:
        with open(config_path) as f:
            data = yaml.safe_load(f)
        
        if not data:
            raise ReleaseError(
                code=ErrorCode.CONFIG_INVALID,
                message="Configuration file is empty",
                fix_instructions=[
                    "Add configuration to your .release-master.yaml file using the template below:",
                    "",
                    DEFAULT_CONFIG
                ]
            )
        
        return Config.from_dict(data)
    except yaml.YAMLError as e:
        raise ReleaseError(
            code=ErrorCode.CONFIG_INVALID,
            message=f"Invalid YAML syntax in configuration file: {e}",
            fix_instructions=[
                "Fix the YAML syntax in your configuration file",
                "Use the template below as a reference:",
                "",
                DEFAULT_CONFIG
            ]
        )


def init_config(path: str = ".", repo_name: Optional[str] = None) -> Config:
    """Initialize a new configuration file.
    
    Args:
        path: Path to create configuration in
        repo_name: Optional repository name. If not provided, will use current directory name
    
    Returns:
        Config object
    
    Raises:
        ReleaseError: If configuration file cannot be created
    """
    config_path = Path(path) / ".release-master.yaml"
    
    # Determine repo name if not provided
    if not repo_name:
        repo_name = Path(path).absolute().name.lower().replace(" ", "-")
    
    # Create default configuration
    config = {
        "version": {
            "files": ["pyproject.toml", "src/" + repo_name.replace("-", "_") + "/__init__.py"],
            "pattern": r"\d+\.\d+\.\d+"
        },
        "changelog": {
            "ai": {
                "enabled": True,
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 1000,
                "response_format": {
                    "type": "json_object"
                }
            },
            "sections": [
                "Features",
                "Bug Fixes",
                "Documentation",
                "Internal Changes"
            ],
            "commit_conventions": {
                "feat": "Features",
                "fix": "Bug Fixes",
                "docs": "Documentation",
                "chore": "Internal Changes",
                "refactor": "Internal Changes",
                "test": "Internal Changes",
                "ci": "Internal Changes",
                "build": "Internal Changes"
            }
        },
        "git": {
            "push": True,
            "tag_prefix": "v",
            "release": {
                "enabled": True,
                "draft": False,
                "prerelease": False,
                "generate_notes": True
            }
        },
        "pypi": {
            "publish": True,
            "repository": "pypi"
        },
        "testing": {
            "run_before_release": True,
            "docker": {
                "enabled": False  # Disabled by default now
            }
        },
        "github": {
            "auto_create": True,  # Enable auto-creation by default
            "repo_name": repo_name,
            "private": False,
            "description": f"Python package for {repo_name.replace('-', ' ').title()}",
            "token_env_var": "GITHUB_TOKEN"
        }
    }
    
    try:
        # Write configuration file
        with open(config_path, "w") as f:
            yaml.safe_dump(config, f, sort_keys=False)
        
        return Config.from_dict(config)
    except OSError as e:
        raise ReleaseError(
            code=ErrorCode.SYSTEM_IO_ERROR,
            message=f"Failed to create configuration file: {e}",
            fix_instructions=[
                "Check file permissions and disk space",
                "Try creating the file manually using the template below:",
                "",
                DEFAULT_CONFIG
            ],
            cause=e
        )


def create_package_structure(path: Path) -> None:
    """Create initial package structure.
    
    Args:
        path: Path to create package in
    """
    # Create directories
    (path / "src").mkdir(exist_ok=True)
    (path / "tests").mkdir(exist_ok=True)
    (path / "docs").mkdir(exist_ok=True)
    
    # Create pyproject.toml
    pkg_name = path.name.replace("-", "_").lower()
    pyproject = {
        "build-system": {
            "requires": ["hatchling"],
            "build-backend": "hatchling.build"
        },
        "project": {
            "name": path.name,
            "version": "0.1.0",
            "description": "",
            "readme": "README.md",
            "requires-python": ">=3.8",
            "license": "MIT",
            "dependencies": []
        }
    }
    with open(path / "pyproject.toml", "w") as f:
        yaml.safe_dump(pyproject, f, sort_keys=False, indent=2)
    
    # Create README.md
    with open(path / "README.md", "w") as f:
        f.write(f"# {path.name}\n\n")
    
    # Create LICENSE
    with open(path / "LICENSE", "w") as f:
        f.write("""MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    
    # Create package directory
    pkg_dir = path / "src" / pkg_name
    pkg_dir.mkdir(exist_ok=True)
    (pkg_dir / "__init__.py").touch()
    
    # Create test file
    with open(path / "tests" / "test_basic.py", "w") as f:
        f.write(f"""def test_import():
    import {pkg_name}
    assert {pkg_name}.__version__
""")
    
    # Initialize git repository
    if not (path / ".git").exists():
        os.chdir(path)
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Initial commit"') 