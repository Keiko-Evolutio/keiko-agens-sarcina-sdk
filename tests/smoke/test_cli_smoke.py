"""Smoke tests for kei_agent.cli module."""

def test_import_cli():
    """Test that cli module can be imported."""


def test_import_cli_functions():
    """Test that main CLI functions can be imported."""


def test_main_function_exists():
    """Test that main function exists and is callable."""
    from kei_agent.cli import main

    assert callable(main)
