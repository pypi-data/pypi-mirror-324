"""Command-line interface for Python Release Master."""

from typing import Optional

import typer
from rich.console import Console

from python_release_master import __version__
from python_release_master.core import config, release, testing, validation

app = typer.Typer(
    name="python-release-master",
    help="Automated Python package release management with AI-powered changelog generation.",
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        console.print(f"Python Release Master version: {__version__}")
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
        help="Path to the Python package to release.",
    ),
) -> None:
    """Create a new release using configuration from .release-master.yaml."""
    try:
        # Load configuration
        cfg = config.load_config(path)

        # Validate environment and package
        validation.validate_environment(cfg)
        validation.validate_package(cfg)

        # Create release
        release.create_release(config=cfg)

        console.print("[green]Release completed successfully! :tada:[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


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
        console.print("[green]Package initialized successfully! :white_check_mark:[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    app() 