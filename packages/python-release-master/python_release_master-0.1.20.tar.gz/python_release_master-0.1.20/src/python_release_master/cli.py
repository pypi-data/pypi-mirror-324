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
def publish(
    bump: str = typer.Option(
        ...,
        "--bump",
        "-b",
        help="Version bump type (major, minor, patch).",
    ),
    title: str = typer.Option(
        ...,
        "--title",
        "-t",
        help="Release title.",
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="Release description (optional).",
    ),
    skip: Optional[str] = typer.Option(
        None,
        "--skip",
        "-s",
        help="Comma-separated list of steps to skip.",
    ),
) -> None:
    """Publish a new release of the package."""
    try:
        # Load configuration
        cfg = config.load_config()

        # Validate environment
        validation.validate_environment(cfg)

        # Run tests (unless skipped)
        if not (skip and "tests" in skip.split(",")):
            testing.run_tests(cfg)

        # Create release
        release.create_release(
            bump_type=bump,
            title=title,
            description=description,
            config=cfg,
            skip_steps=skip.split(",") if skip else None,
        )

        console.print("[green]Release completed successfully! :tada:[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def validate(
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Path to the Python package to validate.",
    ),
) -> None:
    """Validate a Python package without publishing."""
    try:
        # Load and validate configuration
        cfg = config.load_config(path)
        validation.validate_package(cfg)
        console.print("[green]Package validation successful! :white_check_mark:[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    app() 