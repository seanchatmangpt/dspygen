from pathlib import Path
import dspy
from pydantic import BaseModel, Field

from sungen.utils.dspy_tools import predict_type


# class HunkHeader(BaseModel):
#     old_start: int = Field(..., description="Line number where the change starts in the original file.")
#     old_length: int = Field(..., description="Number of lines the change spans in the original file.")
#     new_start: int = Field(..., description="Line number where the change starts in the new file.")
#     new_length: int = Field(..., description="Number of lines the change spans in the new file.")
#
#     @classmethod
#     def from_string(cls, header_line: str):
#         """
#         Parses a hunk header line and returns a HunkHeader instance.
#         Example header_line: '@@ -1,4 +1,5 @@'
#         """
#         import re
#
#         pattern = r'^@@ -(\d+),(\d+) \+(\d+),(\d+) @@'
#         match = re.match(pattern, header_line.strip())
#         if not match:
#             raise ValueError("Invalid hunk header format")
#
#         old_start, old_length, new_start, new_length = map(int, match.groups())
#         return cls(
#             old_start=old_start,
#             old_length=old_length,
#             new_start=new_start,
#             new_length=new_length
#         )


initial_source = """
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


applied_first_diff = """import sympy
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


fixed_source = """import sympy

class MathWeb:
    ...

@app.route('/prime/<int:n>')
def nth_prime(n):
    count = 0
    num = 1
    while count < n:
        num += 1
        if sympy.isprime(num):
            count += 1
    return str(num)
"""


from typing import List

class CorrectSourceCode(dspy.Signature):
    """
    Applies the required changes to the source code based on the provided hunk headers.
    Maintain correct indentation.
    """
    source_code = dspy.InputField(desc="The original source code to be modified.")
    hunk_headers = dspy.InputField(
        desc="List of hunk headers in diff format, e.g., '@@ -<line>,<count> +<line>,<count> @@'."
    )
    required_changes = dspy.InputField(
        desc="List of required changes corresponding to the hunk headers."
    )

    corrected_source_code = dspy.OutputField(desc="The source code after applying all the required changes. Fix indentation to be correct.")


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    reqs = "Replace is_prime with a call to sympy."

    hunks = predict_type({"initial_source": initial_source,
                         "required_changes": reqs},
                         HunkHeader)

    pred = dspy.Predict(CorrectSourceCode)(source_code=initial_source, hunk_headers=str(hunks), required_changes=str(reqs))
    print(pred)
    

    Path("fixed_source.py").write_text(pred.corrected_source_code)


if __name__ == '__main__':
    main()
