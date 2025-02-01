"""Templates for generating project files."""

PYPROJECT_TOML = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_name}"
version = "{version}"
description = "{description}"
readme = "README.md"
requires-python = ">=3.8"
license = "MIT"
keywords = ["{package_name}", "python", "cli"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = []

[[project.authors]]
name = "{owner}"
email = "{owner}@users.noreply.github.com"

[project.urls]
Homepage = "https://github.com/{owner}/{package_name}"
Documentation = "https://github.com/{owner}/{package_name}#readme"
Issues = "https://github.com/{owner}/{package_name}/issues"
Changelog = "https://github.com/{owner}/{package_name}/blob/main/CHANGELOG.md"

[project.scripts]
{cli_name} = "{module_name}.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[tool.black]
line-length = 100
target-version = ["py38"]

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov={module_name}"
testpaths = ["tests"]

[tool.hatch.build]
include = [
    "src/{module_name}/**/*.py",
    "src/{module_name}/**/*.pyi",
    "tests/**/*.py",
]
packages = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.hatch.build.targets.wheel.sources]
"src" = "{module_name}"
'''

README_MD = '''# {title}

{description}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install {package_name}
```

## Usage

```python
import {module_name}
```

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/{owner}/{package_name}.git
   cd {package_name}
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT © {owner}
'''

LICENSE = '''MIT License

Copyright (c) {year} {owner}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

INIT_PY = '''"""Python package for {title}."""

__version__ = "{version}"
__author__ = "{owner}"
__license__ = "MIT"
'''

CLI_PY = '''"""Command line interface for {title}."""

import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("{module_name}")
console = Console()

app = typer.Typer(
    name="{cli_name}",
    help="{description}",
    add_completion=True
)

def version_callback(value: bool) -> None:
    """Print version information and exit."""
    if value:
        from {module_name} import __version__
        console.print(f"{title} version: [green]{__version__}[/]")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version information and exit",
        callback=version_callback,
        is_eager=True,
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug logging"
    ),
) -> None:
    """Main entry point."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.debug("Debug logging enabled")

if __name__ == "__main__":
    app()
'''

TEST_BASIC = '''"""Basic tests for {module_name}."""

from pathlib import Path
import pytest

def test_import():
    """Test that the package can be imported."""
    import {module_name}
    assert {module_name}.__version__
    assert {module_name}.__author__
    assert {module_name}.__license__ == "MIT"

def test_cli():
    """Test CLI can be imported and run."""
    from {module_name}.cli import app
    from typer.testing import CliRunner
    
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{title} version:" in result.stdout
'''

CHANGELOG_MD = '''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release

[Unreleased]: https://github.com/{owner}/{package_name}/compare/v0.1.0...HEAD
'''

GITIGNORE = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
coverage.xml
htmlcov/
.pytest_cache/
.mypy_cache/

# Build
docs/_build/

# OS
.DS_Store
Thumbs.db
'''

DEFAULT_CONFIG = '''# Python Release Master Configuration

# Version management
version:
  files:
    - pyproject.toml  # List of files containing version strings
    - src/{module_name}/__init__.py
  pattern: "\\d+\\.\\d+\\.\\d+"  # Version pattern to match

# Changelog configuration
changelog:
  ai:
    enabled: true
    # NEVER CHANGE THIS MODEL, keep it gpt-4o-mini
    model: "gpt-4o-mini"
    temperature: 0.7
    max_tokens: 1000
    response_format:
      type: "json_object"  # Use JSON mode for structured responses
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes
  commit_conventions:
    feat: Features
    fix: Bug Fixes
    docs: Documentation
    chore: Internal Changes
    refactor: Internal Changes
    test: Internal Changes
    ci: Internal Changes
    build: Internal Changes

# Git configuration
git:
  push: true  # Whether to push changes to remote
  tag_prefix: v  # Prefix for version tags
  release:
    enabled: true
    draft: false  # Create releases as drafts
    prerelease: false  # Mark releases as pre-releases
    generate_notes: true  # Auto-generate release notes

# PyPI configuration
pypi:
  publish: true  # Whether to publish to PyPI
  repository: pypi  # PyPI repository to use (pypi or testpypi)
  token_env_var: "PYPI_TOKEN"  # Environment variable for PyPI token
  uv_token_env_var: "UV_PUBLISH_TOKEN"  # Environment variable for UV token

# Testing configuration
testing:
  run_before_release: false  # Run tests before release
  docker:
    enabled: false  # Run tests in Docker container

# GitHub configuration
github:
  auto_create: false  # Whether to auto-create GitHub repository
  owner: "{owner}"  # Your GitHub username
  repo_name: "{package_name}"  # Your repository name
  private: false  # Whether to create private repository
  description: "{description}"  # Repository description
  token_env_var: "GITHUB_TOKEN"  # Environment variable for GitHub token
''' 