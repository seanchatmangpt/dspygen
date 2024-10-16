from __future__ import annotations
from typing import List, Optional, Union, Literal, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import yaml

from dspygen.utils.dsl_tools import DSLModel


class Trigger(DSLModel):
    """
    Represents the trigger section of a GitHub Actions workflow.
    """
    push: Optional[Dict[str, Any]] = Field(
        None, description="Configuration for push events."
    )
    pull_request: Optional[Dict[str, Any]] = Field(
        None, description="Configuration for pull request events."
    )
    schedule: Optional[List[Dict[str, str]]] = Field(
        None, description="Configuration for scheduled events."
    )


class ActionReference(BaseModel):
    """
    Represents a reference to a GitHub Action.
    """
    uses: str = Field(
        ..., description="The action to use, in the format 'owner/repo@ref'."
    )
    with_: Optional[Dict[str, Any]] = Field(
        None, alias="with", description="Input parameters for the action."
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables for the action."
    )


class Step(DSLModel):
    """
    Represents a single step within a job.
    """
    name: Optional[str] = Field(
        None, description="The name of the step."
    )
    uses: Optional[str] = Field(
        None, description="The action to use for this step."
    )
    run: Optional[str] = Field(
        None, description="The shell command to execute for this step."
    )
    with_: Optional[Dict[str, Any]] = Field(
        None, alias="with", description="Input parameters for the step."
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables for the step."
    )


class Job(DSLModel):
    """
    Represents a single job within a GitHub Actions workflow.
    """
    name: Optional[str] = Field(
        None, description="The name of the job."
    )
    runs_on: str = Field(
        ..., description="The runner environments for the job. "
                         "Valid values are 'ubuntu-latest', 'macos-latest', and 'windows-latest'."
    )
    steps: List[Step] = Field(
        ..., description="List of steps to execute in the job."
    )
    needs: Optional[List[str]] = Field(
        None, description="List of jobs that this job depends on."
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables for the job."
    )


class Workflow(DSLModel):
    """
    Represents a GitHub Actions workflow.
    """
    name: Optional[str] = Field(
        None, description="The name of the workflow."
    )
    on: Trigger = Field(
        ..., description="The events that trigger the workflow."
    )
    jobs: list[Job] = Field(
        ..., description="Dictionary of jobs to execute in the workflow."
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables for the workflow."
    )


class GHActionsDocument(DSLModel):
    """
    Represents the entire GitHub Actions document.
    """
    workflow: Workflow = Field(
        ..., description="The Workflow defined in the GitHub Actions document."
    )


prompt = """Create a GitHub Actions workflow that triggers on push and pull_request events for the main and develop 
branches. The workflow should run on ubuntu-latest and have a single job named CI. This job should contain the 
following steps: check out the repository using the actions/checkout@v3 action, set up Python using 
actions/setup-python@v4 with Python version 3.9, install dependencies with the command pip install -r 
requirements.txt, and run tests using pytest. Ensure the workflow is clean and excludes any unnecessary fields."""


def main():
    """Main function"""
    from sungen.utils.dspy_tools import init_lm, init_instant, init_text
    init_lm()

    doc = GHActionsDocument.from_prompt(prompt)
    print(doc.to_yaml())


if __name__ == '__main__':
    main()

