"""Test rdddy."""

import rdddy


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(rdddy.__name__, str)
