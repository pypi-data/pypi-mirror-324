# Python Release Master

An automated Python package release management tool with AI-powered changelog generation.

## Features

- Automated version management
- AI-powered changelog generation from commits and PRs
- Smart commit message generation for uncommitted changes
- Comprehensive testing (unit, integration, docker)
- Documentation generation and validation
- PyPI publishing with verification
- GitHub Actions integration

## Installation

```bash
pip install python-release-master
```

## Quick Start

1. Add to your GitHub workflow:

```yaml
- name: Release
  env:
    PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    python-release-master publish \
      --bump ${{ github.event.inputs.version_bump }} \
      --title "Release ${{ github.event.inputs.version_bump }} version" \
      --description "${{ github.event.inputs.release_notes }}"
```

2. Configure release settings:

```yaml
# .release-master.yaml
version_files:
  - pyproject.toml
  - src/mypackage/__init__.py

changelog:
  ai_powered: true
  openai_model: gpt-4-0125-preview  # Default model, can also use gpt-3.5-turbo
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes

skip_steps:
  - docker_tests  # Skip docker testing if needed
```

## AI Features

### Smart Changelog Generation

The tool uses OpenAI's GPT models to analyze your commits and pull requests, generating a structured changelog that:

- Determines the appropriate version bump (major, minor, patch)
- Categorizes changes into meaningful sections
- Provides detailed descriptions for each change
- Identifies breaking changes
- Maintains consistent formatting

Example output:
```markdown
## Features
- Add AI-powered changelog generation
- Implement smart commit message handling

## Bug Fixes
- Fix version detection in pyproject.toml
- Resolve GitHub API pagination issues

## Documentation
- Update installation instructions
- Add AI configuration guide
```

### Intelligent Commit Messages

When uncommitted changes are detected, the tool can:

- Analyze file changes to understand the context
- Generate conventional commit messages
- Add appropriate scope and description
- Include detailed body explaining the changes
- Handle breaking changes correctly

Example commit message:
```
feat(changelog): add AI-powered generation

Implement OpenAI integration for generating changelogs from commits and PRs.
This change adds intelligent analysis of code changes to provide better
release notes.
```

## Configuration

### OpenAI Settings

```yaml
changelog:
  ai_powered: true
  openai_model: gpt-4-0125-preview  # Default model
  sections:
    - Features
    - Bug Fixes
    - Documentation
    - Internal Changes
    - Breaking Changes
```

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `PYPI_TOKEN`: PyPI token for publishing
- `GITHUB_TOKEN`: GitHub token for release creation

## Documentation

For detailed documentation, visit [docs/](docs/).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details. 