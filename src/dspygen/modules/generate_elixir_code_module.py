import dspy
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from dspygen.models.code_blueprint import CodeBlueprint


class GenerateElixirCode(dspy.Signature):
    """
    Generates optimized Elixir code based on the provided CodeBlueprint.

    This signature leverages the AI's understanding of Elixir best practices to create or improve Elixir code
    in alignment with the goals defined in the blueprint.
    """
    # Using relevant fields from CodeBlueprint as input fields
    module_name: str = dspy.InputField(desc="Name of the Elixir module to generate or improve.")
    description: str = dspy.InputField(desc="Description of the module's purpose and functionality.")
    files_to_edit: List[str] = dspy.InputField(desc="List of Elixir files that need modification or enhancement.")
    context_files: List[str] = dspy.InputField(desc="Additional context files to provide relevant information.")
    compliance_checks: Optional[Dict[str, bool]] = dspy.InputField(
        desc="Compliance checks to adhere to during code generation.")
    integration_points: List[str] = dspy.InputField(
        desc="Services, APIs, or modules that this code needs to interact with.")
    output: str = dspy.OutputField(desc="Generated or improved Elixir code output.", prefix="```elixir\n")


class ElixirCodeGenerationModule(dspy.Module):
    """ElixirCodeGenerationModule processes a CodeBlueprint to generate or improve Elixir code."""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, blueprint: CodeBlueprint):
        """
        Generates Elixir code using the AI model, applying best practices and optimizations as specified
        in the blueprint.
        """
        # Construct the signature instance with relevant fields from the blueprint
        signature_instance = GenerateElixirCode(
            module_name=blueprint.module_name,
            description=blueprint.description,
            files_to_edit=blueprint.files_to_edit,
            context_files=blueprint.context_files,
            compliance_checks=blueprint.compliance_checks,
            integration_points=blueprint.integration_points
        )

        # Initialize a predictor using the specified AI signature
        pred = dspy.Predict(GenerateElixirCode)

        # Generate the code using the AI and return it
        self.output = pred(**signature_instance.dict()).output
        return self.output


def read_blueprint_from_file(file_path: str) -> CodeBlueprint:
    """Reads a CodeBlueprint from a YAML file."""
    import yaml
    with open(file_path, 'r') as file:
        blueprint_data = yaml.safe_load(file)
    return CodeBlueprint(**blueprint_data)


def write_elixir_code_to_file(file_path: str, elixir_code: str):
    """Writes generated Elixir code to a file."""
    with open(file_path, 'w') as file:
        file.write(elixir_code)


def generate_elixir_code_from_blueprint(blueprint_path: str, output_path: str):
    """Reads a blueprint, generates Elixir code, and writes it to a file."""
    # Read the blueprint from the file
    blueprint = read_blueprint_from_file(blueprint_path)

    # Generate Elixir code based on the blueprint
    generator = ElixirCodeGenerationModule()
    generated_code = generator.forward(blueprint=blueprint)

    # Write the generated code to the output file
    write_elixir_code_to_file(output_path, generated_code)
    print(f"Generated Elixir code written to {output_path}")


import os
import subprocess
import yaml

from dspy import Predict


def read_blueprint(blueprint_path: str) -> dict:
    """Reads the blueprint YAML file and returns its content as a dictionary."""
    with open(blueprint_path, "r") as file:
        blueprint = yaml.safe_load(file)
    return blueprint


def generate_elixir_code_from_blueprint(blueprint_path: str, output_path: str):
    """Generates Elixir code from a blueprint and runs the test."""
    # Read the blueprint
    blueprint = read_blueprint(blueprint_path)

    # Extract details from the blueprint
    files_to_create = blueprint.get("files_to_create", [])
    message = blueprint.get("message", "")
    model = blueprint.get("model", "gpt-4o-mini")
    context_files = blueprint.get("context_files", [])

    # Step 1: Generate code using the AI model
    generate_code(files_to_create, message, model, context_files, output_path)

    # Step 2: Run the test command
    test_cmd = blueprint.get("test_cmd")
    if test_cmd:
        run_tests(test_cmd)


def generate_code(files_to_create, message, model, context_files, output_path):
    """Generates the required Elixir code based on the blueprint."""
    # Create an instance of the dspy.Predict module
    predictor = Predict(GenerateElixirCode)

    for file in files_to_create:
        # Generate code for each file specified in the blueprint
        input_data = {
            "message": message,
            "context": read_context_files(context_files),
            "model": model
        }
        generated_code = predictor(source_code="", **input_data).generated_code

        # Write the generated code to the output path
        file_path = os.path.join(output_path, file)
        with open(file_path, "w") as f:
            f.write(generated_code)

        print(f"Generated and saved: {file_path}")


def read_context_files(context_files):
    """Reads and returns content of all context files as a combined string."""
    combined_context = ""
    for context_file in context_files:
        with open(context_file, "r") as file:
            combined_context += file.read() + "\n"
    return combined_context


def run_tests(test_cmd: str):
    """Executes the provided test command."""
    print(f"Running tests with command: {test_cmd}")
    subprocess.run(test_cmd, shell=True)


if __name__ == "__main__":
    # Example usage:
    blueprint_path = "ping_pong_server_blueprint.yaml"
    output_path = "./"
    generate_elixir_code_from_blueprint(blueprint_path, output_path)
