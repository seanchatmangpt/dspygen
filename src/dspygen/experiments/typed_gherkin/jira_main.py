"""
This is a jira-main.py file that is used to generate a Jira epic for a product manager.
The epic is then used to create a series of Jira tickets.
"""

from dspygen.utils.dspy_tools import init_dspy
from dspygen.lm.cerebras_lm import Cerebras
import dspy
from pydantic import BaseModel, Field
from typing import List

class JiraTicket(BaseModel):
    
    title: str = Field(description="Title of the Jira ticket")
    description: str = Field(description="Description of the Jira ticket")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for the ticket")
    story_points: int = Field(description="Estimated story points for the ticket")

class JiraEpic(BaseModel):
    title: str = Field(description="Title of the Jira epic")
    description: str = Field(description="Description of the Jira epic")
    tickets: List[JiraTicket] = Field(description="List of Jira tickets in the epic")

def main():
    """Main function"""
    init_dspy(lm_instance=Cerebras(model="llama3.1-8b"), max_tokens=4000, temperature=0.0)

    # Define input and output models
    class Input(dspy.BaseModel):
        user_story: str = Field(description="User story for the Jira epic")

    class Output(dspy.BaseModel):
        """Create the FAANG Solution Architect Level Jira Epic and Tickets"""
        jira_epic: JiraEpic

    # Create a Typed Signature
    class JiraSignature(dspy.Signature):
        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()

    # Initialize the Typed Predictor
    predictor = dspy.TypedPredictor(JiraSignature)

    # Example input
    jira_input = Input(
        user_story="As a developer, I want a fully automated system to write all of my code for me."
    )

    # Get prediction
    prediction = predictor(input=jira_input)
    print(f"Jira Epic: {prediction.output.jira_epic}")


if __name__ == '__main__':
    main()
