"""Basic tests for the pygraphile package."""

import pygraphile


def test_version():
    """Test that version is defined."""
    assert hasattr(pygraphile, "__version__")
    assert isinstance(pygraphile.__version__, str)
    assert pygraphile.__version__ == "0.1.0"


def test_module_imports():
    """Test that the module can be imported."""
    assert pygraphile is not None
    assert pygraphile.__author__ == "dshaw0004"
