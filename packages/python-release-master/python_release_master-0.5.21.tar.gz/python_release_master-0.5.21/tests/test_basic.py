"""Basic tests for python_release_master."""

import pytest

def test_import():
    """Test that the package can be imported."""
    import python_release_master
    assert python_release_master.__version__
