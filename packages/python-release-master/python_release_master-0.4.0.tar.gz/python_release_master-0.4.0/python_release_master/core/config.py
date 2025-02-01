"""Configuration management for Python Release Master."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any

import yaml


@dataclass
class VersionConfig:
    """Version configuration."""
    files: List[str]
    pattern: str = r'\d+\.\d+\.\d+'


@dataclass
class AIConfig:
    """AI configuration."""
    enabled: bool = True
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    response_format: Dict[str, str] = None

    def __post_init__(self):
        """Set default response format."""
        if self.response_format is None:
            self.response_format = {"type": "json_object"}


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
        """
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


def load_config(path: str = ".") -> Config:
    """Load configuration from file.
    
    Args:
        path: Path to configuration file or directory
    
    Returns:
        Config object
    """
    config_path = Path(path)
    if config_path.is_dir():
        config_path = config_path / ".release-master.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}. "
            "Please create a .release-master.yaml file in your project root."
        )
    
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    return Config.from_dict(data)


def init_config(path: str = ".") -> None:
    """Initialize a new configuration file.
    
    Args:
        path: Path to create configuration in
    """
    config_path = Path(path) / ".release-master.yaml"
    if config_path.exists():
        raise FileExistsError(f"Configuration file already exists: {config_path}")
    
    # Create default configuration
    config = {
        "version": {
            "files": ["pyproject.toml"],
            "pattern": r"\d+\.\d+\.\d+"
        },
        "changelog": {
            "ai": {
                "enabled": True,
                "model": "gpt-4",
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
                "enabled": True,
                "python_version": "3.9",
                "base_image": "python:3.9-slim"
            }
        },
        "github": {
            "auto_create": False,
            "token_env_var": "GITHUB_TOKEN"
        }
    }
    
    # Write configuration file
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False, indent=2)
    
    # Create initial package structure if needed
    pkg_path = Path(path)
    if not (pkg_path / "pyproject.toml").exists():
        create_package_structure(pkg_path)


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