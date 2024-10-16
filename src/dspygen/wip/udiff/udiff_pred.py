# test_unified_diff.py

from pydantic import BaseModel, Field
from typing import List
import dspy

from dspygen.utils.dspy_tools import init_dspy


# Define the Input, DiffLine, and Output models
class Input(BaseModel):
    """Model representing the input for generating a unified diff."""
    file_path: str = Field(description="The path to the file to be modified.")
    user_request: str = Field(description="The user's request or modification description.")
    original_code: str = Field(description="The original code content of the file.")

class DiffLine(BaseModel):
    """Represents a single line in a unified diff."""
    content: str
    line_type: str = Field(description="Type of the diff line: 'added', 'removed', or 'context'.")

class Output(BaseModel):
    """Model representing the output of a unified diff generation."""
    file_path: str = Field(description="The path to the file that was modified.")
    diff: List[DiffLine] = Field(description="A list of diff lines representing the unified diff.")

# Define the signature for the Typed Predictor
class UnifiedDiffSignature(dspy.Signature):
    """
    Signature for generating a unified diff given the file path,
    user request, and original code content.
    """
    input: Input = dspy.InputField()
    output: Output = dspy.OutputField()

# Create the Typed Predictor using the UnifiedDiffSignature
predictor = dspy.TypedPredictor(UnifiedDiffSignature)

# Example test input
def test_unified_diff():
    init_dspy()

    # Define the input data for testing
    input_data = Input(
        file_path="mathweb/flask/app.py",
        user_request="Replace is_prime with a call to sympy.",
        original_code="""
import math

class MathWeb:
    ...

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

@app.route('/prime/<int:n>')
def nth_prime(n):
    count = 0
    num = 1
    while count < n:
        num += 1
        if is_prime(num):
            count += 1
    return str(num)
"""
    )

    # Run the predictor
    prediction = predictor(input=input_data)

    # Print the output for verification
    print(f"File Path: {prediction.output.file_path}")
    for line in prediction.output.diff:
        print(f"{line.line_type}: {line.content}")

    # Example assertions (adjust these based on expected results)
    assert prediction.output.file_path == "mathweb/flask/app.py"
    assert any(line.line_type == 'added' and 'sympy.isprime' in line.content for line in prediction.output.diff)
    assert any(line.line_type == 'removed' and 'def is_prime' in line.content for line in prediction.output.diff)

if __name__ == "__main__":
    # Execute the test function
    test_unified_diff()
