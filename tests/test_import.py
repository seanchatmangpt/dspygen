"""Test dspygen."""

import dspygen


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(dspygen.__name__, str)
