"""Python Release Master - Automated package release management with AI-powered changelog generation."""

import tomli
from pathlib import Path

def _get_version() -> str:
    """Get version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        return tomli.load(f)["project"]["version"]

__version__ = _get_version() 