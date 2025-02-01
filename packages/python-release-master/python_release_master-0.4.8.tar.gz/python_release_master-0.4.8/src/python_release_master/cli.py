"""Command-line interface for Python Release Master."""

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from python_release_master import __version__
from python_release_master.core import config, release, testing, validation
from python_release_master.core.logger import logger
from python_release_master.core.errors import handle_error

app = typer.Typer(
    name="python-release-master",
    help="Automated Python package release management with AI-powered changelog generation.",
    add_completion=False,
)

def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        logger.panel(f"Python Release Master version: {__version__}", "Version Info")
        raise typer.Exit()

@app.callback()
def common(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version information and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Common options for all commands."""

@app.command()
def release_package(
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Path to package directory"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug logging"
    )
) -> None:
    """Create a new release."""
    try:
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")
        
        # Load configuration
        cfg = config.load_config(path)
        
        # Create release
        release.create_release(cfg)
        
        logger.success("Release completed successfully! 🎉")
    except Exception as e:
        handle_error(e)

@app.command()
def init(
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Path to initialize the package in.",
    ),
) -> None:
    """Initialize a new Python package with release configuration."""
    try:
        # Create initial configuration
        config.init_config(path)
        logger.success("Package initialized successfully! ✅")
    except Exception as e:
        handle_error(e)

def main() -> None:
    """Main entry point for the CLI."""
    try:
        app()
    except Exception as e:
        handle_error(e) 