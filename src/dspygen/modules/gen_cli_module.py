"""Documentation: The source code provided is a Python script that uses the dspy and typer libraries to generate a
command-line interface (CLI) based on a given concept. The script defines a class called GenCLIModule, which contains
a forward method that takes in a CLI concept and uses the dspy library to generate a CLI with commands. The
gen_cli_call function then uses this class to generate the CLI based on a given concept. The script also includes a
main function that initializes the dspy library and calls the gen_cli_call function with an empty CLI concept.
Additionally, the script includes a streamlit component from the fastapi library and a router that defines a post
route for generating the CLI. The gen_cli_route function uses the gen_cli_call function to generate the CLI based on
the data provided in the post request."""
import dspy
from pydantic import BaseModel, Field
from typer import Typer

from dspygen.typetemp.functional import render
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.yaml_tools import YAMLMixin

app = Typer()


class GenCLIModule(dspy.Module):
    """GenCLIModule"""

    def forward(self, cli_concept):
        # Generate mock CLI help
        pred = dspy.Predict("cli_concept -> cli_with_commands")
        result = pred(cli_concept=cli_concept).cli_with_commands
        return result


def gen_cli_call(cli_concept):
    gen_cli = GenCLIModule()
    return gen_cli.forward(cli_concept=cli_concept)


@app.command()
def call(cli_concept):
    """GenCLIModule"""
    init_dspy()
    
    print(gen_cli_call(cli_concept=cli_concept))


class TyperCommand(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the command")
    help: str = Field(..., min_length=1, description="The help text for the command")


class TyperCLI(BaseModel, YAMLMixin):
    name: str = Field(..., min_length=1, description="The name of the CLI application")
    commands: list[TyperCommand] = Field(
        ..., description="The commands of the CLI application"
    )


# --- Jinja Templates ---
cli_template = """
import typer
app = typer.Typer()

{% for command in model.commands %}
@app.command(name="{{ command.name }}")
def {{ command.name }}():
    \"\"\"{{ command.help }}\"\"\"
    # Command logic goes here
    print("This is the {{ command.name }} command.")

{% endfor %}

if __name__ == "__main__":
    app()


"""


pytest_template = """
import pytest
from typer.testing import CliRunner
from dspygen.cli import app  # Updated import statement

runner = CliRunner()

{% for command in model.commands %}
def test_{{ command.name }}():
    result = runner.invoke(app, ["{{ command.name }}"])
    assert result.exit_code == 0
    assert "This is the {{ command.name }} command." in result.output  # Replace with specific expected output

{% endfor %}
"""


def main():
    init_dspy()

    concept = gen_concept("7 Command Expert Python ChatBot with OpenAI calls")

    print(concept)

    # model = gen_pydantic_instance_call(prompt=concept,
    #     root_model=TyperCLI, child_models=[TyperCommand]
    # )
    #
    # print(model.to_yaml())
    #
    # render(cli_template, model=model, to="{{ model.name | underscore }}_cli.py")
    # render(pytest_template, model=model, to="test_{{ model.name | underscore }}_cli.py")

    # # --- Render Templates ---
    # env = Environment(loader=FileSystemLoader("."))
    # env.from_string(cli_template).stream(model=model.model_dump()).dump(
    #     "ror_dspy.py"
    # )
    # env.from_string(pytest_template).stream(model=model.model_dump()).dump(
    #     "test_ror_dspy.py"
    # )

    print("CLI application and tests generated.")

from fastapi import APIRouter
router = APIRouter()

@router.post("/gen_cli/")
async def gen_cli_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return gen_cli_call(**data)


def gen_concept(cli_concept):
    init_dspy()
    style = ("Verbose output that simulates the --help command of the synthetic"
             "CLI.")

    pred = dspy.Predict("cli_concept, style -> synthetic_cli_help")
    result = pred(cli_concept=cli_concept, style=style).synthetic_cli_help
    return result


if __name__ == "__main__":
    main()
