from typer.testing import CliRunner

from dspygen.experiments.done.openai_ror_cli import app

runner = CliRunner()

def test_create():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "This is the create command." in result.output  # Replace with specific expected output

def test_train():
    result = runner.invoke(app, ["train"])
    assert result.exit_code == 0
    assert "This is the train command." in result.output  # Replace with specific expected output

def test_generate():
    result = runner.invoke(app, ["generate"])
    assert result.exit_code == 0
    assert "This is the generate command." in result.output  # Replace with specific expected output

def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "This is the list command." in result.output  # Replace with specific expected output

def test_delete():
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "This is the delete command." in result.output  # Replace with specific expected output

def test_help():
    result = runner.invoke(app, ["help"])
    assert result.exit_code == 0
    assert "This is the help command." in result.output  # Replace with specific expected output

