"""Command-line interface for Python Release Master."""

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from python_release_master import __version__
from python_release_master.core import config, release
from python_release_master.core.logger import logger
from python_release_master.core.errors import handle_error

def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        logger.panel(f"Python Release Master version: {__version__}", "Version Info")
        raise typer.Exit()

def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug logging"
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version information and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Create a new release with automated version bumping, changelog generation, and publishing."""
    try:
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")
        
        # Load configuration from current directory
        cfg = config.load_config(".")
        
        # Create release
        release.create_release(cfg)
        
        logger.success("Release completed successfully! 🎉")
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    typer.run(main) 