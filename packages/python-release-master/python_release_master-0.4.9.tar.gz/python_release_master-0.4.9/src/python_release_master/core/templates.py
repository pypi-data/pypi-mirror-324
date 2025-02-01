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
authors = []

[project.urls]
Homepage = "https://github.com/{owner}/{package_name}"
Issues = "https://github.com/{owner}/{package_name}/issues"

[project.scripts]
{cli_name} = "{module_name}.cli:main"
'''

README_MD = '''# {title}

{description}

## Installation

```bash
pip install {package_name}
```

## Usage

```python
import {module_name}
```

## Development

1. Clone the repository
2. Install in development mode:
   ```bash
   pip install -e .
   ```

## License

MIT
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
'''

CLI_PY = '''"""Command line interface."""

import logging
from typing import Optional

import click
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

@click.group()
@click.version_option()
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(debug: bool):
    """CLI tool for {title}."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.debug("Debug logging enabled")

if __name__ == "__main__":
    main()
'''

TEST_BASIC = '''"""Basic tests for {module_name}."""

import pytest

def test_import():
    """Test that the package can be imported."""
    import {module_name}
    assert {module_name}.__version__
'''

DEFAULT_CONFIG = '''version:
  files: ["pyproject.toml", "src/{module_name}/__init__.py"]
  pattern: "\\d+\\.\\d+\\.\\d+"

changelog:
  ai:
    enabled: true
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 1000
    response_format:
      type: "json_object"
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

git:
  push: true
  tag_prefix: v
  release:
    enabled: true
    draft: false
    prerelease: false
    generate_notes: true

pypi:
  publish: true
  repository: pypi
  token_env_var: "PYPI_TOKEN"
  uv_token_env_var: "UV_PUBLISH_TOKEN"

testing:
  run_before_release: true
  docker:
    enabled: false

github:
  auto_create: true
  repo_name: "{package_name}"
  private: false
  description: "{description}"
  token_env_var: "GITHUB_TOKEN"
''' 