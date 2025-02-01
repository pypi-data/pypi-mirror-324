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
    """Main configuration class."""
    version: VersionConfig
    changelog: ChangelogConfig
    git: GitConfig
    testing: TestingConfig
    github: GitHubConfig


def load_config(workspace_dir: Optional[Path] = None) -> Config:
    """Load configuration from .release-master.yaml.
    
    Args:
        workspace_dir: Optional workspace directory path
        
    Returns:
        Config object
        
    Raises:
        ReleaseError: If config is invalid or missing
    """
    workspace_dir = Path(workspace_dir or os.getcwd())
    config_path = workspace_dir / ".release-master.yaml"
    
    # Create default config if not exists
    if not config_path.exists():
        with open(config_path, "w") as f:
            yaml.safe_dump(DEFAULT_CONFIG, f)
    
    try:
        with open(config_path) as f:
            data = yaml.safe_load(f)
        
        # Load and validate sections
        version = VersionConfig(**data.get("version", {}))
        changelog = ChangelogConfig(
            ai=AIConfig(**data.get("changelog", {}).get("ai", {})),
            sections=data.get("changelog", {}).get("sections", []),
            commit_conventions=data.get("changelog", {}).get("commit_conventions", {})
        )
        git = GitConfig(**data.get("git", {}))
        testing = TestingConfig(**data.get("testing", {}))
        github = GitHubConfig(**data.get("github", {}))
        
        return Config(
            version=version,
            changelog=changelog,
            git=git,
            testing=testing,
            github=github
        )
        
    except Exception as e:
        raise ReleaseError(
            code=ErrorCode.CONFIG_INVALID,
            message=f"Failed to load config: {str(e)}",
            fix_instructions=[
                "Check your .release-master.yaml for syntax errors",
                "Compare against the default configuration"
            ],
            cause=e
        ) 