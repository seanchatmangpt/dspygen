import httpx
from dspygen.utils.dspy_tools import init_dspy
from dspygen.lm.cerebras_lm import Cerebras
import dspy

from pydantic import BaseModel, Field
from typing import List, Optional


# Define models for the AiderBlueprint
class AiderBlueprint(BaseModel):
    files_to_create: List[str] = Field(..., description="List of files to be created.")
    files_to_edit: List[str] = Field(..., description="List of files to be edited.")
    read_only_files: Optional[List[str]] = Field(default_factory=list, description="List of files to be marked as read-only and used in context window.")
    model: str = Field(default="gpt-4", description="AI model to use.")
    auto_test: bool = Field(default=True, description="Enable or disable automatic testing after edits.")
    lint: bool = Field(default=True, description="Enable or disable linting of files.")
    pretty_output: bool = Field(default=True, description="Enable or disable colorized output.")
    dark_mode: bool = Field(default=False, description="Set terminal output theme to dark mode.")
    additional_args: Optional[List[str]] = Field(default_factory=list, description="Additional command-line arguments for Aider.")
    message: str = Field(..., description="Custom message to use for the Aider command.")
    conventions_file: Optional[str] = Field(default="CONVENTIONS.md", description="File containing coding conventions.")


def save_blueprint_to_ash(blueprint: AiderBlueprint, base_url: str):
    """
    Save the generated AiderBlueprint to the Ash backend.

    Args:
        blueprint (AiderBlueprint): The blueprint to save.
        base_url (str): The base URL of the Ash backend API.
    """
    with httpx.Client() as client:
        response = client.post(f"{base_url}/aider_blueprints", json=blueprint.dict())
        response.raise_for_status()
        print(f"Blueprint saved successfully with ID: {response.json().get('id')}")


def main(input_text):
    """Main function"""
    init_dspy(max_tokens=2000, temperature=0.0)

    # Define input and output models
    class Input(dspy.BaseModel):
        user_story: str

    class Output(dspy.BaseModel):
        """Create the FAANG Solution Architect Level AiderBlueprint"""
        aider_blueprint: AiderBlueprint

    # Create a Typed Signature
    class AiderBlueprintSignature(dspy.Signature):
        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()

    # Initialize the Typed Predictor
    predictor = dspy.TypedPredictor(AiderBlueprintSignature)

    # Example input
    user_story_input = Input(
        user_story=input_text)

    # Get prediction
    prediction = predictor(input=user_story_input)

    # Print the generated AiderBlueprint
    print(f"AiderBlueprint: {prediction.output.aider_blueprint}")

    # Save the generated blueprint to Ash backend
    # base_url = "http://localhost:4000/api"  # Replace with your actual Ash backend URL
    # save_blueprint_to_ash(prediction.output.aider_blueprint, base_url)


def blueprint_call(user_story, context):
    main(user_story + context)


if __name__ == '__main__':
    main("As a user, I want to be able to search for a product by name so that I can find it easily.")
