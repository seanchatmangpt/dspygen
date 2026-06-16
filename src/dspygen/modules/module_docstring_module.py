"""
Module for generating Python module docstrings using a DSPy language model pipeline.

Given a module dictionary and a context string, :class:`ModuleDocstringModule` uses
a DSPy ``Predict`` call to produce a concise, accurate docstring that describes the
module's purpose, inputs, and outputs. The module exposes both a programmatic API
(``module_docstring_call``) and a Typer CLI entry-point (``call``) for interactive use.
"""
import dspy
from typer import Typer

from dspygen.utils.dspy_tools import init_dspy

app = Typer()


class ModuleDocstringModule(dspy.Module):
    """ModuleDocstringModule"""

    def forward(self, module_dict, context):
        pred = dspy.Predict("module_dict, context -> module_docstring")
        result = pred(module_dict=module_dict, context=context).module_docstring
        return result


def module_docstring_call(module_dict, context):
    module_docstring = ModuleDocstringModule()
    return module_docstring.forward(module_dict=module_dict, context=context)


@app.command()
def call(module_dict, context):
    """ModuleDocstringModule"""
    init_dspy()

    print(module_docstring_call(module_dict=module_dict, context=context))



# TODO: Add streamlit component


from fastapi import APIRouter

router = APIRouter()

@router.post("/module_docstring/")
async def module_docstring_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return module_docstring_call(**data)


def main():
    init_dspy()
    module_dict = ""
    context = ""
    print(module_docstring_call(module_dict=module_dict, context=context))


if __name__ == "__main__":
    main()
