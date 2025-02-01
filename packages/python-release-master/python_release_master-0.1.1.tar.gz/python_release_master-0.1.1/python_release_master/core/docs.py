"""Documentation building module."""

import subprocess
from pathlib import Path


def build_docs() -> None:
    """Build the documentation using Sphinx."""
    docs_source = Path("docs/source")
    docs_build = Path("docs/build/html")

    if not docs_source.exists():
        raise FileNotFoundError("Documentation source directory not found")

    # Create build directory if it doesn't exist
    docs_build.parent.mkdir(parents=True, exist_ok=True)

    # Build documentation
    subprocess.run(
        ["sphinx-build", "-b", "html", str(docs_source), str(docs_build)],
        check=True,
    ) 