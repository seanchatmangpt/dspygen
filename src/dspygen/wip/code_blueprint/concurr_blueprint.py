from typing import List, Optional

from pydantic import Field, BaseModel

from sungen.utils.dspy_tools import predict_type, PredictType, predict_types, init_dspy
from sungen.utils.yaml_tools import YAMLMixin

import dspy


class CodeBlueprint(BaseModel, YAMLMixin):
    """
    Defines a blueprint for configuring and running commands with code generation tools in an enterprise environments.

    This class encapsulates configuration parameters for creating, editing, and managing files using AI-powered
    development assistants or code generation tools.
    """
    description: str = Field(
        ...,
        description="Description of the blueprint, explaining its purpose, functionality, "
                    "and how it is intended to be used."
    )
    files_to_create: List[str] = Field(
        ...,
        description="List of files that should be created as part of this blueprint. "
                    "The tool will ensure these files exist before proceeding with any operations."
    )
    files_to_edit: List[str] = Field(
        ...,
        description="List of files that the code generation tool will edit. "
                    "These files are the focus of the tool's modifications or enhancements."
    )
    read_only_files: List[str] = Field(
        default_factory=list,
        description="List of files to be marked as read-only. The tool will consider these files for context "
                    "but will not modify them. Useful for providing additional information without risking unwanted changes."
    )
    message: str = Field(
        None,
        description="Custom message to use for the tool's operations. Useful for providing a specific instruction "
                    "or context for the tool to consider when making changes."
    )
    context_files: List[str] = Field(
        default_factory=list,
        description="List of relevant context files. These files are included as additional context for the tool, "
                    "helping it understand the broader codebase or environments without being modified."
    )


def main():
    """Main function to demonstrate concurrent predictions."""
    # Initialize dspy settings if necessary
    # from sungen.utils.dspy_tools import init_dspy
    # init_dspy()

    # Define a list of prediction tasks
    prediction_tasks = [
        PredictType(
            input_data={"message": "Create blueprint.yaml for project Alpha."},
            output_model=CodeBlueprint
        ),
        PredictType(
            input_data={"message": "Check system status for project Beta."},
            output_model=CodeBlueprint
        ),
        PredictType(
            input_data={"message": "Set up deployment scripts for project Gamma."},
            output_model=CodeBlueprint
        ),
        PredictType(
            input_data={"message": "Verify integration for project Delta."},
            output_model=CodeBlueprint
        ),
        # Add more PredictType instances as needed
    ]

    # Execute predictions concurrently
    results = predict_types(prediction_tasks)

    # Process and display the results
    for idx, result in enumerate(results, start=1):
        if isinstance(result, CodeBlueprint):
            print(f"Result {idx} - CodeBlueprint:")
            print(result.to_yaml())


if __name__ == "__main__":
    init_dspy()

    main()
