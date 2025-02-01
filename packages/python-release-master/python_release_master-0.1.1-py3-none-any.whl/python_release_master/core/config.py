"""Configuration module for Python Release Master."""

import os
from dataclasses import dataclass
from typing import List, Optional
import yaml


@dataclass
class ChangelogConfig:
    """Configuration for changelog generation."""

    ai_powered: bool = True
    openai_model: str = "gpt-4"
    sections: List[str] = None

    def __post_init__(self):
        """Set default sections if none provided."""
        if self.sections is None:
            self.sections = [
                "Features",
                "Bug Fixes",
                "Documentation",
                "Internal Changes",
            ]

    @classmethod
    def from_dict(cls, data: dict) -> "ChangelogConfig":
        """Create ChangelogConfig from dictionary."""
        return cls(
            ai_powered=data.get("ai_powered", True),
            openai_model=data.get("openai_model", "gpt-4"),
            sections=data.get("sections", None)
        )


@dataclass
class Config:
    """Main configuration for Python Release Master."""

    version_files: List[str]
    changelog: ChangelogConfig = None
    skip_steps: Optional[List[str]] = None

    def __post_init__(self):
        """Convert changelog dict to ChangelogConfig if needed."""
        if self.changelog is None:
            self.changelog = ChangelogConfig()
        # Don't initialize skip_steps if it's None
        if self.skip_steps is not None and not isinstance(self.skip_steps, list):
            self.skip_steps = list(self.skip_steps)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create Config from dictionary."""
        return cls(
            version_files=data.get("version_files", ["pyproject.toml"]),
            changelog=ChangelogConfig.from_dict(data.get("changelog", {})),
            skip_steps=data.get("skip_steps")  # Don't provide default here
        )


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or return default config.

    Args:
        config_path: Path to configuration file. If None, will look for .release-master.yaml
            in current directory.

    Returns:
        Config object with loaded configuration.
    """
    if config_path is None:
        config_path = ".release-master.yaml"

    # Handle directory paths
    if os.path.isdir(config_path):
        config_path = os.path.join(config_path, ".release-master.yaml")

    try:
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f) or {}
    except (FileNotFoundError, IsADirectoryError):
        # Return default config if file not found
        return Config(version_files=["pyproject.toml"])

    return Config.from_dict(config_dict) 