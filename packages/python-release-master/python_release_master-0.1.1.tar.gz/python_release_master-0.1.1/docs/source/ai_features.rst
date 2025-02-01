AI Features
===========

Python Release Master includes powerful AI features powered by OpenAI's GPT models to enhance your release management workflow.

Smart Changelog Generation
------------------------

The tool uses OpenAI's GPT models to analyze your commits and pull requests, generating a structured changelog that:

- Determines the appropriate version bump (major, minor, patch)
- Categorizes changes into meaningful sections
- Provides detailed descriptions for each change
- Identifies breaking changes
- Maintains consistent formatting

Example output:

.. code-block:: markdown

   ## Features
   - Add AI-powered changelog generation
   - Implement smart commit message handling

   ## Bug Fixes
   - Fix version detection in pyproject.toml
   - Resolve GitHub API pagination issues

   ## Documentation
   - Update installation instructions
   - Add AI configuration guide

Configuration
~~~~~~~~~~~~

.. code-block:: yaml

   # .release-master.yaml
   changelog:
     ai_powered: true
     openai_model: gpt-4-0125-preview  # Default model
     sections:
       - Features
       - Bug Fixes
       - Documentation
       - Internal Changes
       - Breaking Changes

Intelligent Commit Messages
-------------------------

When uncommitted changes are detected, the tool can:

- Analyze file changes to understand the context
- Generate conventional commit messages
- Add appropriate scope and description
- Include detailed body explaining the changes
- Handle breaking changes correctly

Example commit message:

.. code-block:: text

   feat(changelog): add AI-powered generation

   Implement OpenAI integration for generating changelogs from commits and PRs.
   This change adds intelligent analysis of code changes to provide better
   release notes.

Configuration
~~~~~~~~~~~~

The AI features require an OpenAI API key, which can be provided through:

1. Environment variable:

.. code-block:: bash

   export OPENAI_API_KEY=your-api-key-here

2. GitHub Actions secret:

.. code-block:: yaml

   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

Model Selection
~~~~~~~~~~~~~

You can choose between different OpenAI models:

- ``gpt-4-0125-preview`` (default): Best quality, slower
- ``gpt-3.5-turbo``: Faster, good for most cases

Set the model in your configuration:

.. code-block:: yaml

   changelog:
     ai_powered: true
     openai_model: gpt-3.5-turbo  # Override default model

API Reference
------------

For detailed API documentation, see :ref:`api_reference`. 