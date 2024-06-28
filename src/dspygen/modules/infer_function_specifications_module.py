from textwrap import dedent

import dspy
from dspygen.utils.dspy_tools import init_ol, init_dspy
from dspygen.utils.markdown_tools import extract_triple_backticks
from rich import print


class InferFunctionSpecificationsSignature(dspy.Signature):
    """
    Infer the specifications of a given function by analyzing its source code, including input types, output types, and side effects.
    """
    func_source_code = dspy.InputField(desc="The source code of the function to infer specifications.")
    inferred_specifications = dspy.OutputField(
        desc="Inferred specifications including input types, output types, and side effects.")
    user_story = dspy.OutputField(
        desc="User story describing the inferred specifications in YAML. MAKE SURE TO INCLUDE \n",
        prefix=dedent("""```yaml
title: ...
description: ...
acceptance_criteria:
  - ...
input_types:
  - ...
output_types:
  - ...
side_effects:
  - ...
```""")
    )


class InferFunctionSpecificationsModule(dspy.Module):
    """InferFunctionSpecificationsModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, func_source_code):
        pred = dspy.Predict(InferFunctionSpecificationsSignature)
        self.output = pred(func_source_code=func_source_code)
        # print(str(self.output))
        return self.output


def infer_function_specifications_call(func_source_code) -> str:
    infer_function_specifications = InferFunctionSpecificationsModule()
    specifications: str = infer_function_specifications.forward(
        func_source_code=func_source_code).inferred_specifications
    return specifications


def infer_user_story_call(func_source_code) -> str:
    infer_function_specifications = InferFunctionSpecificationsModule()
    user_story = infer_function_specifications.forward(
        func_source_code=func_source_code).user_story
    return extract_triple_backticks(user_story)


test_code = """import os

def impure_function(x, y):
    # Modifies an environment variable
    os.environ['TEST_VAR'] = 'modified'

    # Writes to a file
    with open('test_file.txt', 'w') as f:
        f.write('This is a test.')

    # Print statement (side effect)
    print('This function is not pure.')
    return x + y"""

pure_function_code = """
def pure_function(x: int, y: int) -> int:
    return x + y
"""

elixir_code = """
defmodule PureFunction do
  def pure_function(x, y) do
    x + y
  end
end
"""


def main():
    init_dspy(model="gpt-4o")

    # func_source_code = test_code
    # specifications = infer_function_specifications_call(func_source_code=func_source_code)
    # print("Specifications for test_code:", specifications)
    #
    # func_source_code = elixir_code
    # specifications = infer_function_specifications_call(func_source_code=func_source_code)
    # print("Specifications for elixir_code:", specifications)
    #
    # func_source_code = pure_function_code
    # specifications = infer_function_specifications_call(func_source_code=func_source_code)
    # print("Specifications for pure_function_code:", specifications)

    # Example us4age
    user_story = infer_user_story_call(test_code)
    print(user_story)

    user_story = infer_user_story_call(elixir_code)
    print(user_story)

    user_story = infer_user_story_call(pure_function_code)
    print(user_story)


if __name__ == "__main__":
    main()
