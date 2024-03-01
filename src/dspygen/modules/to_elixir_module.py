"""
This code imports the necessary libraries and defines a class called `ToElixirModule` that inherits from `dspy.Module`. The `forward` method takes in `code` as an argument and uses the `dspy.Predict` function to generate Elixir source code from the input code. The `to_elixir_call` function calls the `forward` method and returns the generated Elixir code. The `app` variable defines a Typer application and the `call` command takes in `code` as an argument and prints the generated Elixir code. The `router` variable defines an API router and the `to_elixir_route` function takes in a dictionary of data and returns the generated Elixir code. The `main` function calls the `to_elixir_call` function with an empty string as the input code.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class ToElixirModule(dspy.Module):
    """ToElixirModule"""

    def forward(self, code):
        style = "Proper formatting with newlines, etc"
        pred = dspy.ChainOfThought("code, style -> elixir_source_code")
        result = pred(code=code, style=style).elixir_source_code
        return result


def to_elixir_call(code):
    to_elixir = ToElixirModule()
    return to_elixir.forward(code=code)


@app.command()
def call(code):
    """ToElixirModule"""
    init_dspy()
    
    print(to_elixir_call(code=code))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/to_elixir/")
async def to_elixir_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return to_elixir_call(**data)


def main():
    init_dspy()
    code = ""
    print(to_elixir_call(code=code))
    

if __name__ == "__main__":
    main()
