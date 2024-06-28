"""

"""
import dspy
from dspygen.utils.dspy_tools import init_ol


class VerifyFunctionPuritySignature(dspy.Signature):
    """
    Verify that a given function is pure and has no side effects by analyzing its source code.
    """
    func_source_code = dspy.InputField(desc="The source code of the function to verify purity.")
    error_message = dspy.OutputField(desc="Error message if the function is impure.")
    is_pure = dspy.OutputField(desc="Boolean indicating if the function is pure. True or False only")


class VerifyFunctionPurityModule(dspy.Module):
    """VerifyFunctionPurityModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, func_source_code):
        pred = dspy.ChainOfThought(VerifyFunctionPuritySignature)
        self.output = pred(func_source_code=func_source_code)
        print(str(self.output))
        return self.output


def verify_function_purity_call(func_source_code) -> bool:
    verify_function_purity = VerifyFunctionPurityModule()
    is_pure: str = verify_function_purity.forward(func_source_code=func_source_code).is_pure
    return is_pure.lower() != "false"


test_code = """import os

def impure_function():
    # Modifies an environment variable
    os.environ['TEST_VAR'] = 'modified'
    
    # Writes to a file
    with open('test_file.txt', 'w') as f:
        f.write('This is a test.')
    
    # Print statement (side effect)
    print('This function is not pure.')"""


pure_function_code = """
def pure_function(x, y):
    return x + y
"""


elixir_code = """
defmodule ImpureFunction do
  def impure_function do
    # Modifies an environment variable
    System.put_env("TEST_VAR", "modified")

    # Writes to a file
    File.write!("test_file.txt", "This is a test.")

    # Print statement (side effect)
    IO.puts("This function is not pure.")
  end
end
"""


def main():
    init_ol(model="qwen2:7b-instruct")
    func_source_code = test_code
    result = verify_function_purity_call(func_source_code=func_source_code)
    assert result is False

    result = verify_function_purity_call(func_source_code=elixir_code)
    assert result is False

    result = verify_function_purity_call(func_source_code=pure_function_code)
    assert result is True


if __name__ == "__main__":
    main()
