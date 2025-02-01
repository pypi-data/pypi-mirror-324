Installation
============

This guide will help you install and set up Python Release Master.

Requirements
-----------

Before installing, ensure you have the following prerequisites:

* Python 3.8 or higher
* pip (Python package installer)
* Git

Installation Methods
------------------

You can install Python Release Master using one of the following methods:

From PyPI
~~~~~~~~

The recommended way to install is via pip:

.. code-block:: bash

    pip install python-release-master

From Source
~~~~~~~~~~

To install from source:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/python-release-master.git
       cd python-release-master

2. Install in development mode:

   .. code-block:: bash

       pip install -e ".[dev]"

Configuration
------------

After installation, you'll need to configure a few things:

1. Create a configuration file named ``release-config.yaml`` in your project root:

   .. code-block:: yaml

       version:
         files:
           - pyproject.toml
           - src/mypackage/__init__.py

       changelog:
         ai_powered: true
         openai_model: "gpt-4-0125-preview"
         sections:
           - Features
           - Bug Fixes
           - Documentation
           - Other

2. If using AI features, set your OpenAI API key:

   .. code-block:: bash

       export OPENAI_API_KEY=your-api-key

Verification
-----------

To verify the installation:

.. code-block:: bash

    python -m python_release_master --version

This should display the version number of Python Release Master. 