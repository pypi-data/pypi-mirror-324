"""Configuration management for Python Release Master."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class ChangelogConfig:
    """Configuration for changelog generation."""

    ai_powered: bool = True
    openai_model: str = "gpt-4"
    sections: List[str] = field(default_factory=lambda: ["Features", "Bug Fixes", "Documentation", "Internal Changes"])

    @classmethod
    def from_dict(cls, data: dict) -> "ChangelogConfig":
        """Create a ChangelogConfig from a dictionary."""
        return cls(
            ai_powered=data.get("ai_powered", True),
            openai_model=data.get("openai_model", "gpt-4"),
            sections=data.get("sections", ["Features", "Bug Fixes", "Documentation", "Internal Changes"]),
        )


@dataclass
class Config:
    """Main configuration for Python Release Master."""

    version_files: List[str]
    changelog: ChangelogConfig
    skip_steps: List[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create a Config from a dictionary."""
        return cls(
            version_files=data.get("version_files", []),
            changelog=ChangelogConfig.from_dict(data.get("changelog", {})),
            skip_steps=data.get("skip_steps", []),
        )


def load_config(path: str = ".") -> Config:
    """Load configuration from .release-master.yaml file."""
    config_path = Path(path) / ".release-master.yaml"
    
    # Use default configuration if file doesn't exist
    if not config_path.exists():
        return Config(
            version_files=["pyproject.toml"],
            changelog=ChangelogConfig(),
        )
    
    # Load and parse configuration file
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    return Config.from_dict(data) 