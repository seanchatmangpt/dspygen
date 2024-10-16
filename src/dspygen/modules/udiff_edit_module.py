import dspy
from dspy import InputField, OutputField, Signature

from dspygen.utils.dspy_tools import init_dspy

class UDiffChangeGenerator(dspy.Signature):
    """
    Generates the diff content (hunk_content) between the hunk lines for a unified diff (UDiff)
    based on the given source code, hunk header, and edit instructions.

    CHANGED LINES MUST FOLLOW THE HUNK HEADER EXACTLY
    """
    source_code = InputField(
        desc="The original source code to be edited."
    )
    hunk_header = InputField(
        desc="The hunk header indicating the lines to be changed."
    )
    edit_instructions = InputField(
        desc="The instructions describing the changes to be made to the source code."
    )
    changed_hunk_header= OutputField(desc="Must match")
    changed_lines = OutputField(
        desc="The changed lines with the same amount of changes as the line numbers."
    )



class UDiffGenerator(dspy.Signature):
    """
    Generates hunk_header for a unified diff (UDiff) based on the given source code and edit instructions.
    Hunk Header Example @@ -*,* +*,* @@
    """
    source_code = InputField(
        desc="The original source code to be edited."
    )
    edit_instructions = InputField(
        desc="The instructions describing the changes to be made to the source code."
    )
    # Output fields
    hunk_header = OutputField(desc="@@ -*,* +*,* @@")
    # added_lines = OutputField()
    # removed_lines = OutputField()


def add_line_numbers(input_string):
    # Split the input string into a list of lines
    lines = input_string.splitlines()

    # Enumerate over the lines, adding line numbers starting from 1
    numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]

    # Join the numbered lines back into a single string with newline characters
    return "\n".join(numbered_lines)


def udiff_edit_call(source_path, edit_instructions):
    """Utility function to generate a udiff format for the provided source code and instructions."""
    # Read the source code from the file
    with open(source_path, 'r') as file:
        source_code = file.read()

    # print(add_line_numbers(source_code))

    result = dspy.ChainOfThought(UDiffGenerator).forward(
        source_code=add_line_numbers(source_code),
        # udiff_format=udiff_format,
        edit_instructions=edit_instructions)

    print(f"@@ -{result.hunk_header}")
    # print(result.added_lines)
    # print(result.removed_lines)

    result = dspy.ChainOfThought(UDiffChangeGenerator).forward(
        source_code=add_line_numbers(source_code),
        hunk_header=f"@@ -{result.hunk_header}",
        edit_instructions=edit_instructions)

    print(result.changed_lines)

    return result


# Example usage
example_source_path = "example_file.js"  # Make sure this file exists on disk
# example_edit_instructions = "change loginUser to use a ternary"
example_edit_instructions = "rename the greet method to greetPerson and change the Hello message"


def main():
    init_dspy()
    """Main function to demonstrate generating a udiff for the example."""
    # Generate the udiff using the provided example inputs
    udiff_result = udiff_edit_call(example_source_path, example_edit_instructions)


if __name__ == "__main__":
    main()
