# Python Release Master

An automated Python package release management tool with AI-powered changelog generation. Streamline your Python package releases with automated version bumping, changelog generation, and PyPI publishing.

## Features

- 🚀 Automated version bumping (major, minor, patch)
- 📝 AI-powered changelog generation
- 🔍 Package validation in clean Docker environment
- 📦 PyPI publishing
- 🏷️ GitHub release creation
- ✨ Modern CLI interface

## Installation

```bash
pip install python-release-master
```

## Quick Start

1. Create a configuration file `.release-master.yml` in your project root:

```yaml
version_files:
  - pyproject.toml  # Files containing version strings to update
  - src/your_package/__init__.py

changelog:
  ai_powered: true  # Set to false to use simple commit list
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes

git:
  push: true  # Whether to push changes automatically
  tag: true   # Whether to create git tags

pypi:
  publish: true  # Whether to publish to PyPI
```

2. Set up your PyPI token:
```bash
export PYPI_TOKEN=your_pypi_token
```

3. Run the release command:
```bash
# Create a patch release
python-release-master release create --version-bump patch

# Create a minor release with custom title
python-release-master release create --version-bump minor --title "New Features Release"

# Create a major release with description
python-release-master release create --version-bump major --title "v2.0 Release" --description "Complete rewrite with new features"
```

## Advanced Usage

### Skipping Steps

You can skip specific steps in the release process:

```bash
python-release-master release create --version-bump patch --skip version,changelog,publish
```

Available skip options:
- `version`: Skip version bumping
- `changelog`: Skip changelog generation
- `verify`: Skip package verification
- `publish`: Skip PyPI publishing
- `github`: Skip GitHub release creation

### Package Verification

By default, the tool verifies your package in a clean Docker environment before publishing:

1. Creates a fresh Docker container
2. Installs your package
3. Runs basic validation tests
4. Ensures all dependencies are properly specified

To skip verification:
```bash
python-release-master release create --version-bump patch --skip verify
```

### AI-Powered Changelog

When `changelog.ai_powered` is enabled, the tool:
1. Analyzes your git commits since the last release
2. Uses AI to categorize and summarize changes
3. Generates a human-readable changelog

To disable AI-powered changelog:
```yaml
changelog:
  ai_powered: false
```

## Configuration Reference

Full configuration options in `.release-master.yml`:

```yaml
version_files:
  - pyproject.toml
  - src/your_package/__init__.py

changelog:
  ai_powered: true
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes
  commit_types:  # Optional: map commit prefixes to sections
    feat: Features
    fix: Bug Fixes
    docs: Documentation
    chore: Internal Changes

git:
  push: true
  tag: true
  remote: origin
  main_branch: main

pypi:
  publish: true
  repository: pypi  # Use 'testpypi' for testing

github:
  create_release: true
  draft: false
  prerelease: false
```

## Requirements

- Python 3.8+
- Docker (for package verification)
- Git
- PyPI account and token

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 