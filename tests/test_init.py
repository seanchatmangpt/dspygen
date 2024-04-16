import pytest
from typer.testing import CliRunner

from dspygen.cli import app

runner = CliRunner()


@pytest.mark.parametrize("project_name", [
    " projectWithSpaceAtStart",
    "projectWithSpaceAtEnd ",
    "project with space",
    "project__with__doubleunderscore",
    "project--with--doublehyphen",
    "-projectWithHyphenAtStart",
    "projectWithHyphenAtEnd-",
    "_projectWithUnderscoreAtStart",
    "projectWithUnderscoreAtEnd_",
    "-projectWithHyphenAtStart",
    "_projectWithUnderscoreAtStart",
])
def test_init_invalid_names(project_name):
    result = runner.invoke(app, ["init", project_name])
    assert result.exit_code != 0
