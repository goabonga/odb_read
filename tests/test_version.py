"""Tests for package version."""

from odb_tui import __version__


def test_version():
    """Package version should be a valid semver string."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
