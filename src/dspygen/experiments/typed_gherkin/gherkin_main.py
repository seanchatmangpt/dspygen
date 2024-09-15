from dspygen.utils.dspy_tools import init_dspy
from dspygen.lm.cerebras_lm import Cerebras
import dspy

from pydantic import BaseModel, Field
from typing import List


# Define models for the Gherkin story
class Step(BaseModel):
    step_type: str = Field(description="Type of the step (Given, When, Then, And, But)")
    description: str = Field(description="Description of the step")


class Scenario(BaseModel):
    title: str = Field(description="Title of the scenario")
    steps: List[Step] = Field(description="List of steps in the scenario")


class Feature(BaseModel):
    title: str = Field(description="Title of the Gherkin feature")
    description: str = Field(description="Description of the Gherkin feature")
    scenarios: List[Scenario] = Field(description="List of scenarios under the feature")


def main():
    """Main function"""
    init_dspy(lm_instance=Cerebras(model="llama3.1-8b"), max_tokens=2000, temperature=0.0)

    # Define input and output models
    class Input(dspy.BaseModel):
        user_story: str

    class Output(dspy.BaseModel):
        """Create the FAANG Solution Architect Level BDD"""
        gherkin_scenario: Feature

    # Create a Typed Signature
    class GherkinSignature(dspy.Signature):
        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()

    # Initialize the Typed Predictor
    predictor = dspy.TypedPredictor(GherkinSignature)

    # Example input
    user_story_input = Input(
        user_story="As a user, I want to be able to search for a product by name so that I can find it easily.")

    # Get prediction
    prediction = predictor(input=user_story_input)
    print(f"Gherkin Scenario: {prediction.output.gherkin_scenario}")


if __name__ == '__main__':
    main()
