"""Main entry point for the Python Release Master CLI."""

from python_release_master.cli import main as cli_main


def main() -> int:
    """Entry point for the CLI."""
    return cli_main()


if __name__ == "__main__":
    main() 