Configuration
=============

Configuration File
----------------

Python Release Master uses a YAML configuration file (``.release-master.yaml``) for its settings:

.. code-block:: yaml

   version_files:
     - pyproject.toml
     - src/mypackage/__init__.py

   changelog:
     ai_powered: true
     openai_model: gpt-4-0125-preview
     sections:
       - Features
       - Bug Fixes
       - Documentation
       - Internal Changes

   skip_steps:
     - docker_tests

Configuration Options
------------------

Version Files
~~~~~~~~~~~

List of files containing version strings that should be updated during version bumps:

.. code-block:: yaml

   version_files:
     - pyproject.toml  # Version in project metadata
     - src/mypackage/__init__.py  # Version in package __init__
     - docs/conf.py  # Version in documentation

Changelog Settings
~~~~~~~~~~~~~~~

Configuration for changelog generation:

.. code-block:: yaml

   changelog:
     ai_powered: true  # Use AI for generation
     openai_model: gpt-4-0125-preview  # Model to use
     sections:  # Changelog sections
       - Features
       - Bug Fixes
       - Documentation
       - Internal Changes
     commit_types:  # Conventional commit types
       - feat
       - fix
       - docs
       - style
       - refactor
       - test
       - chore

Skip Steps
~~~~~~~~~

List of steps to skip during release:

.. code-block:: yaml

   skip_steps:
     - docker_tests  # Skip Docker testing
     - docs  # Skip documentation build
     - test  # Skip testing

Environment Variables
------------------

Required Variables
~~~~~~~~~~~~~~~

- ``OPENAI_API_KEY``: OpenAI API key for AI features
- ``PYPI_TOKEN``: PyPI token for publishing
- ``GITHUB_TOKEN``: GitHub token for release creation

Optional Variables
~~~~~~~~~~~~~~~

- ``OPENAI_MODEL``: Override default OpenAI model
- ``RELEASE_MASTER_CONFIG``: Path to config file (default: ``.release-master.yaml``) 