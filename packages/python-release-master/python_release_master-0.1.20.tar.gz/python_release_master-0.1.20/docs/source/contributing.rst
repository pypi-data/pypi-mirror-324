Contributing
===========

We love your input! We want to make contributing to Python Release Master as easy and transparent as possible.

Development Setup
---------------

1. Fork the repository
2. Clone your fork:

   .. code-block:: bash

      git clone https://github.com/yourusername/python-release-master.git
      cd python-release-master

3. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # Linux/macOS
      # or
      venv\Scripts\activate  # Windows

4. Install development dependencies:

   .. code-block:: bash

      pip install -e ".[dev]"

Running Tests
-----------

Run the test suite:

.. code-block:: bash

   python -m pytest

With coverage:

.. code-block:: bash

   python -m pytest --cov=python_release_master

Building Documentation
-------------------

Build the documentation locally:

.. code-block:: bash

   cd docs
   make html

Pull Request Process
-----------------

1. Update the documentation if needed
2. Update the tests if needed
3. Run the test suite
4. Create a Pull Request with a clear title and description
5. Wait for review and address any comments

Code Style
---------

We use:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:

.. code-block:: bash

   black .
   isort .
   flake8 .
   mypy . 