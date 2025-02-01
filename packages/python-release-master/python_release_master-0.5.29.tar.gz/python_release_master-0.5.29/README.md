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

## Usage

Simply run the command in your package directory:

```bash
python-release-master
```

Options:
- `--debug` or `-d`: Enable debug logging
- `--version` or `-V`: Show version information and exit

This will:
- Analyze changes and bump version
- Generate changelog
- Build and publish to PyPI
- Create GitHub release

## Configuration

Configuration is optional and automatically created with smart defaults. If you need to customize, create a `.release-master.yaml` file:

```yaml
version:
  files: ["pyproject.toml", "src/my_package/__init__.py"]

changelog:
  ai:
    enabled: true
    model: "gpt-4o-mini"

github:
  auto_create: true
  private: false

pypi:
  publish: true
```

## License

MIT 