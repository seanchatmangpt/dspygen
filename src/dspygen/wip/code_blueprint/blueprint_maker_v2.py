from sungen.utils.dspy_tools import predict_str

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

    fn_message = "Implement an example feature to demonstrate YAML configuration. Save the blueprint to blueprint.yaml"\

    # Use the updated predict_str function to get the save directory
    try:
        save_dir = predict_str(
            "file_path",
            message=fn_message,
            current_dir=current_folder
        )
        print(f"Save Directory: {save_dir}")
    except Exception as e:
        print(f"Save directory prediction failed: {e}")

    # Continue with the rest of your main function
    # ...

if __name__ == "__main__":
    main()
