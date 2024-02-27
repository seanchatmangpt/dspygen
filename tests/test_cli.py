"""Test dspygen CLI."""

from typer.testing import CliRunner

from dspygen.cli import app

runner = CliRunner()


def test_init() -> None:
    """Test that the say command works as expected."""
    result = runner.invoke(app, ["init", "hello-world-project"])
    assert result.exit_code == 0


def test_bad_init() -> None:
    """Test that the say command works as expected."""
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 2
