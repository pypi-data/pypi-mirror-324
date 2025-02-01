"""Command line interface for python-release-master."""

import click
from .core import version, changelog, docs


@click.group()
def cli():
    """Python Release Master - Automated release management tool."""
    pass


@cli.group(name="version")
def version_cmd():
    """Version management commands."""
    pass


@version_cmd.command(name="bump")
@click.argument("bump_type", type=click.Choice(["major", "minor", "patch"]))
def bump(bump_type: str):
    """Bump version number (major, minor, or patch)."""
    try:
        new_version = version.bump_version(bump_type)
        click.echo(f"Version bumped to {new_version}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.group(name="changelog")
def changelog_cmd():
    """Changelog management commands."""
    pass


@changelog_cmd.command(name="generate")
def generate():
    """Generate changelog for current version."""
    try:
        changelog.generate_changelog()
        click.echo("Changelog generated successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.group(name="docs")
def docs_cmd():
    """Documentation management commands."""
    pass


@docs_cmd.command(name="build")
def build():
    """Build documentation."""
    try:
        docs.build_docs()
        click.echo("Documentation built successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main() 