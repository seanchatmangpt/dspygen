"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class FunctionInvokeModule(dspy.Module):
    """FunctionInvokeModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, function_declaration):
        pred = dspy.Predict("function_declaration -> invocation_command")
        self.output = pred(function_declaration=function_declaration).invocation_command
        return self.output

    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer

app = Typer()


@app.command()
def call(function_declaration):
    """FunctionInvokeModule"""
    init_dspy()

    print(function_invoke_call(function_declaration=function_declaration))


def function_invoke_call(function_declaration):
    function_invoke = FunctionInvokeModule()
    return function_invoke.forward(function_declaration=function_declaration)


quick = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left) + [pivot] + quicksort(right)"""


def main():
    init_dspy()
    function_declaration = quick
    result = function_invoke_call(function_declaration=function_declaration)
    print(result)
    exec(function_declaration)
    eval(result)


from fastapi import APIRouter

router = APIRouter()


@router.post("/function_invoke/")
async def function_invoke_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return function_invoke_call(**data)


"""
import streamlit as st


# Streamlit form and display
st.title("FunctionInvokeModule Generator")
function_declaration = st.text_input("Enter function_declaration")

if st.button("Submit FunctionInvokeModule"):
    init_dspy()

    result = function_invoke_call(function_declaration=function_declaration)
    st.write(result)
"""

if __name__ == "__main__":
    main()
