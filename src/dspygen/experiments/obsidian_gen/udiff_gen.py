from pydantic import BaseModel, Field
from typing import List, Optional

from dspygen.wip.code_blueprint.generate import Generate
from sungen.typetemp.template.render_mixin import RenderMixin
from sungen.typetemp.template.typed_template import TypedTemplate
from sungen.utils.dspy_tools import PredictType, predict_types


class UDiffInstructions(BaseModel, TypedTemplate):
    """
    Generic model for providing prescriptive instructions for generating udiffs for any code modification.
    """
    add_import: str = Field(
        ...,
        description="Add the required import statement for any new libraries or dependencies being used."
    )
    remove_function: str = Field(
        ...,
        description="Remove the function or code block that is being replaced or refactored, ensuring all related code is removed as well."
    )
    replace_calls: str = Field(
        ...,
        description="Identify all occurrences where the old function or method is called and replace them with the new function or method."
    )
    context_inclusion: str = Field(
        ...,
        description="Ensure that 3 lines of context are provided before and after each change in the diff for clarity during code review."
    )
    check_line_numbers: str = Field(
        ...,
        description="Check and confirm the line numbers where the changes are made. Ensure consistency between the original and modified code."
    )
    check_dependencies: str = Field(
        ...,
        description="Review any dependencies or related files that may rely on the modified function or code. Ensure those are updated as well."
    )
    verify_tests: str = Field(
        ...,
        description="After making the changes, run all relevant tests to ensure the code functions as expected."
    )
    document_changes: str = Field(
        ...,
        description="Update any comments, inline documentation, or external documentation that references the modified code."
    )

    source: str = """
    UDiff Instructions:
    - Add Import: {{ add_import }}
    - Remove Function/Code Block: {{ remove_function }}
    - Replace Function/Method Calls: {{ replace_calls }}
    - Context Inclusion: {{ context_inclusion }}
    - Check Line Numbers: {{ check_line_numbers }}
    - Check Dependencies: {{ check_dependencies }}
    - Verify Tests: {{ verify_tests }}
    - Document Changes: {{ document_changes }}
    """


# UDiffOutput class with TypedTemplate
class UDiffOutput(BaseModel, TypedTemplate):
    """
    Model for generating the final udiff output in a more reflective way.
    """
    modified_files: List[str] = Field(
        ...,
        description="Which files have been modified in the diff?"
    )
    changes_summary: List[str] = Field(
        ...,
        description="What are the key changes made in each file?"
    )
    diff_output: List[str] = Field(
        ...,
        description="What does the unified diff output look like, showing lines added and removed?"
    )
    context_provided: Optional[str] = Field(
        None,
        description="Is there enough context provided around each change to make it understandable?"
    )

    source: str = """
    UDiff Output:
    Modified Files:
    {% for file in modified_files %}
    - {{ file }}
    {% endfor %}

    Changes Summary:
    {% for summary in changes_summary %}
    - {{ summary }}
    {% endfor %}

    Diff Output:
    {% for diff in diff_output %}
    {{ diff }}
    {% endfor %}

    Context Provided: {{ context_provided }}
    """


code = """def is_prime(x):
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


def main():
    """Main function to create tasks for all REAP steps"""
    from sungen.utils.dspy_tools import init_dspy
    init_dspy()

    instructions = "Replace is_prime with a call to sympy."

    task = PredictType(
        input_data={"source_to_modify": code, "instructions": instructions},
        output_model=UDiffInstructions
    )

    result = predict_types([task])

    fixed = Generate(f"Task: {instructions}{result[0].render()}\nCode to Change\n```code\n{code}\n```\nDiff to fix:\n```diff\n")()
    print(fixed)

if __name__ == '__main__':
    main()
