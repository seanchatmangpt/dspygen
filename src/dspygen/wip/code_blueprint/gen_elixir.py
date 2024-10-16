# generate.py
import dsp
import random
from dspy import Module, Prediction
from dspy.predict.parameter import Parameter
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging
import os

from dspygen.wip.code_blueprint.generate import Generate
from sungen.utils.dspy_tools import init_dspy


# ============================
# Main Function for Generation Pipeline
# ============================

def main():
    """
    Main function to generate test and implementation files using the Generate class.
    """
    init_dspy()

    # Define the blueprints
    test_blueprint = {
        "additional_args": [],
        "auto_test": False,
        "description": "A blueprint to create a test for PingPongServer GenServer that plays ping-pong five times and stops.",
        "files_to_create": [
            "test/ping_pong_server_test.exs"
        ],
        "files_to_edit": [],
        "lint": False,
        "message": "Create a test for PingPongServer GenServer that plays ping-pong five times and stops.",
        "test_cmd": "mix test",
        "model": "gpt-4o-mini",
        "module_name": "ping_pong_server_test_blueprint",
        "context_files": [".context.md"],
        "version": "1.0.0"
    }

    code_blueprint = {
        "additional_args": [],
        "auto_test": False,
        "description": "A blueprint to create PingPongServer GenServer that plays ping-pong five times and stops.",
        "files_to_create": [
            "lib/ping_pong_server.ex"
        ],
        "files_to_edit": [],
        "lint": False,
        "message": "Create PingPongServer GenServer that plays ping-pong five times and stops based on the generated tests.",
        "test_cmd": "mix test",
        "model": "gpt-4o-mini",
        "module_name": "ping_pong_server_blueprint",
        "context_files": [
            "test/ping_pong_server_test.exs"  # Reference to the generated test file
        ],
        "version": "1.0.0"
    }

    # Helper function to write generated content to files
    def write_files(files_content: Dict[str, str]):
        for file_path, content in files_content.items():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Created file: {file_path}")

    # 1. Generate the Test File
    print("Generating Test File...")
    test_prompt = test_blueprint["message"]
    test_generator = Generate(prompt=test_prompt, temperature=0.3, max_tokens=500)

    try:
        test_prediction = test_generator()
        test_content = test_prediction.text.strip()
        # Assuming the prediction returns the full file content
        files_to_create_test = {test_blueprint["files_to_create"][0]: test_content}
        write_files(files_to_create_test)
    except Exception as e:
        print(f"Test generation failed: {e}")
        return

    # 2. Generate the Implementation File Based on the Test
    print("\nGenerating Implementation File...")
    # Read the generated test content to use as context
    try:
        with open(test_blueprint["files_to_create"][0], 'r') as f:
            test_context = f.read()
    except FileNotFoundError:
        print("Test file not found. Cannot proceed with implementation generation.")
        return

    # For simplicity, we'll include the test content directly in the prompt
    code_prompt = f"{code_blueprint['message']}\n\n# Test Context:\n{test_context}\n\n# Implementation:"
    code_generator = Generate(prompt=code_prompt, temperature=0.3, max_tokens=1000)

    try:
        code_prediction = code_generator()
        code_content = code_prediction.text.strip()
        files_to_create_code = {code_blueprint["files_to_create"][0]: code_content}
        write_files(files_to_create_code)
    except Exception as e:
        print(f"Implementation generation failed: {e}")
        return

    print("\nGeneration pipeline completed successfully.")

if __name__ == "__main__":
    main()
