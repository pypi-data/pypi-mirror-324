# Python Release Master

A modern Python package release automation tool that handles everything from version bumping to publishing on PyPI.

## Features

- 🚀 One-command release process
- 📦 Automatic package building and publishing with `uv`
- 🤖 AI-powered changelog generation
- 🔄 Automatic version bumping
- 🎯 GitHub repository creation and release management
- 📝 Smart defaults and minimal configuration

## Requirements

- Python 3.8+
- GitHub CLI (`gh`) installed and authenticated
- PyPI token in environment as `PYPI_TOKEN`
- OpenAI API key in environment as `OPENAI_API_KEY` (optional, for AI features)

## Installation

```bash
pip install python-release-master
```

## Quick Start

1. Create a new package:
   ```bash
   release-master init my-package
   ```
   This will:
   - Create a new directory with your package name
   - Set up the package structure with smart defaults
   - Create a GitHub repository
   - Initialize git and push the first commit

2. Release your package:
   ```bash
   cd my-package
   release-master release-package
   ```
   This will:
   - Analyze changes and bump version
   - Generate changelog
   - Build and publish to PyPI
   - Create GitHub release

## Configuration

Configuration is optional and automatically created with smart defaults. If you need to customize, edit `.release-master.yaml`:

```yaml
version:
  files: ["pyproject.toml", "src/my_package/__init__.py"]

changelog:
  ai:
    enabled: true
    model: "gpt-4"

github:
  auto_create: true
  private: false

pypi:
  publish: true
```

## License

MIT 