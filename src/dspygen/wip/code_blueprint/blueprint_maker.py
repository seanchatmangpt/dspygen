from typing import List, Optional

from pydantic import Field, BaseModel

from sungen.utils.dspy_tools import predict_type
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


import os

def get_repository_root() -> str:
    """Get the absolute path of the repository root."""
    current_path = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_path, '.git')) and current_path != '/':
        current_path = os.path.dirname(current_path)
    return current_path

def get_current_folder() -> str:
    """Get the absolute path of the current folder."""
    return os.path.abspath(os.path.dirname(__file__))


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    repo_root = get_repository_root()
    current_folder = get_current_folder()
    print(f"Repository Root: {repo_root}")
    print(f"Current Folder: {current_folder}")

    bp_message = "Create blueprint.yaml for hello blueprint with the message 'hello blueprint'. Use .context.md for the read"


    fn_message = "Implement an example feature to demonstrate YAML configuration. Save the blueprint to blueprint.yaml"

        # Create the YAML configuration using the predict_type function
    blueprint = predict_type(
        {"message": bp_message},
        CodeBlueprint)
    save_dir = dspy.Predict("message, current_dir -> file_path")(message=fn_message, current_dir=current_folder).file_path

    # Convert the output model instance to YAML
    yaml_output = blueprint.to_yaml(save_dir)
    print(yaml_output)


from concurrent.futures import ThreadPoolExecutor, as_completed

def predict_type_message():
    bp_message = "Create blueprint.yaml for hello blueprint with the message 'hello blueprint'. Use .context.md for the read"
    blueprint = predict_type({"message": bp_message}, CodeBlueprint)
    return blueprint

def predict_save_dir():
    fn_message = "Implement an example feature to demonstrate YAML configuration. Save the blueprint to blueprint.yaml"
    save_dir = dspy.Predict("message, current_dir -> file_path")(
        message=fn_message, current_dir=get_current_folder()).file_path
    return save_dir

def run_concurrently():
    # Using ThreadPoolExecutor to run the functions concurrently
    with ThreadPoolExecutor() as executor:
        # Submit both tasks to the executor
        future_blueprint = executor.submit(predict_type_message)
        future_save_dir = executor.submit(predict_save_dir)

        # Use as_completed to get results as they complete
        for future in as_completed([future_blueprint, future_save_dir]):
            try:
                result = future.result()  # Get the result of the future
                if future == future_blueprint:
                    print("Blueprint prediction completed:", result)
                elif future == future_save_dir:
                    print("Save directory prediction completed:", result)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_concurrently()



if __name__ == '__main__':
    main()
    