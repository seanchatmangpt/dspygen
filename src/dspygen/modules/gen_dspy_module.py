import dspy
from pydantic import BaseModel, Field
from typer import Typer

from dspygen.typetemp.functional import render

app = Typer()


class DSPyModuleTemplate(BaseModel):
    """{{ input or list of inputs }} -> {{ outputs }}"""

    inputs: list[str] = Field(..., description="Inputs for dspy.Module jinja template.")
    output: str = Field(..., description="Output for dspy.Module jinja template.")
    class_name: str = Field(
        ..., description="Class name combining the inputs and outputs"
    )


dspy_module_template = '''"""
{{ docstring }}
"""
import dspy
from dspygen.utils.dspy_tools import init_dspy

{%- set module_name = model.class_name | class_name ~ "Module" %}
{%- set inputs_join = model.inputs | join(', ') %}    
{%- set inputs_join_kwargs = model.inputs | map('to_kwarg') | join(', ') %}        
{% set var_name = model.class_name | var_name %}


class {{ module_name }}(dspy.Module):
    """{{ module_name }}"""

    def forward(self, {{ inputs_join }}):
        pred = dspy.Predict("{{ inputs_join }} -> {{ model.output }}")
        result = pred({{ inputs_join_kwargs }}).{{ model.output }}
        return result


{% include 'dspy_module_cli_call.j2' %}



{% include 'dspy_module_def_call.j2' %}



{% include 'dspy_module_main.j2' %}



{% include 'dspy_module_route.j2' %}



if __name__ == "__main__":
    main()

'''


class SignatureDspyModuleModule(dspy.Module):
    """SignatureDspyModuleModule"""

    def forward(self, tmpl_model):
        source = render(dspy_module_template, model=tmpl_model, docstring="")

        return source

