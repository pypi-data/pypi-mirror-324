Quick Start
===========

GitHub Workflow
-------------

1. Add to your GitHub workflow:

.. code-block:: yaml

   - name: Release
     env:
       PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
       OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
     run: |
       python-release-master publish \
         --bump ${{ github.event.inputs.version_bump }} \
         --title "Release ${{ github.event.inputs.version_bump }} version" \
         --description "${{ github.event.inputs.release_notes }}"

Configuration
------------

Create a ``.release-master.yaml`` file:

.. code-block:: yaml

   version_files:
     - pyproject.toml
     - src/mypackage/__init__.py

   changelog:
     ai_powered: true
     openai_model: gpt-4-0125-preview  # Default model
     sections:
       - Features
       - Bug Fixes
       - Documentation
       - Internal Changes

   skip_steps:
     - docker_tests  # Skip docker testing if needed

Basic Usage
----------

1. Bump version:

   .. code-block:: bash

      python -m python_release_master version bump --type patch

2. Generate changelog:

   .. code-block:: bash

      python -m python_release_master changelog generate

3. Build documentation:

   .. code-block:: bash

      python -m python_release_master docs build 