# Python Release Master

An automated Python package release management tool with AI-powered changelog generation.

## Features

- 🤖 AI-powered changelog generation
- 🔄 Automated version bumping (semantic versioning)
- 📦 PyPI publishing
- 🏷️ Git tag and release creation
- 🎯 Smart version bump suggestions

## Installation

```bash
pip install python-release-master
```

## Quick Start

1. Create a `.release-master.yaml` configuration file in your project root:

```yaml
version:
  files:
    - pyproject.toml  # Files containing version strings
  pattern: '\d+\.\d+\.\d+'

changelog:
  ai:
    enabled: true
    model: gpt-4-1106-preview
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes

git:
  push: true
  tag_prefix: v
  release:
    enabled: true

pypi:
  publish: true
```

2. Set required environment variables:
```bash
export OPENAI_API_KEY=your-openai-api-key
export PYPI_TOKEN=your-pypi-token
```

3. Run the release command from your project directory:
```bash
release-master release-package
```

## How It Works

1. Analyzes git history to determine version bump type (major, minor, patch)
2. Updates version in specified files
3. Generates changelog using OpenAI
4. Builds Python package
5. Publishes to PyPI
6. Creates Git tag and release

## Configuration

Key configuration options in `.release-master.yaml`:

- `version.files`: List of files containing version strings
- `changelog.ai.enabled`: Enable/disable AI-powered changelog
- `git.push`: Whether to push changes to remote
- `pypi.publish`: Whether to publish to PyPI

## CLI Commands

```bash
# Create a new release
release-master release-package

# Show help
release-master --help

# Show version
release-master --version
```

## Requirements

- Python 3.8+
- OpenAI API key
- PyPI token
- Git repository

## License

MIT License 