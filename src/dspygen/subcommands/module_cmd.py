"""Generate DSPy module"""
from importlib import import_module

import os

import typer
from pydantic import BaseModel, Field

from dspygen.modules.gen_pydantic_instance_module import gen_pydantic_instance_call
from dspygen.modules.file_name_module import file_name_call
from typetemp.functional import render
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.file_tools import dspy_modules_dir, source_dir

app = typer.Typer()

dspy_module_template = '''import dspy
from typer import Typer


app = Typer()


{%- set module_name = model.class_name | class_name ~ "Module" %}
{%- set inputs_join = model.inputs | join(', ') %}    
{%- set inputs_join_kwargs = model.inputs | map('to_kwarg') | join(', ') %}        
{% set var_name = model.class_name | var_name %}


class {{ module_name }}(dspy.Module):
    """{{ model.docstring }}"""

    def forward(self, {{ inputs_join }}):
        pred = dspy.Predict("{{ inputs_join }} -> {{ model.output }}")
        result = pred({{ inputs_join_kwargs }}).{{ model.output }}
        return result


def {{ var_name }}_call({{ inputs_join }}):
    {{ var_name }} = {{ module_name }}()
    return {{ var_name }}.forward({{ inputs_join_kwargs }})
 

@app.command()
def module_test({{ inputs_join }}):
    """{{ model.docstring }}"""
    print({{ var_name }}_call({{ inputs_join_kwargs }}))
    
    
def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)
{% for input in model.inputs %}
    {{ input }} = ""
{% endfor %}
    print({{ var_name }}_call({{ inputs_join_kwargs }}))


if __name__ == "__main__":
    main()

'''


class DSPyModuleTemplate(BaseModel):
    '''
    class {{ class_name}}(dspy.Module):
    """{{ docstring }}"""

        def forward(self, {{ inputs }}):
            pred = dspy.Predict("{{ inputs }} -> {{ output }}")

            result = pred({{ inputs }}).{{ output }}
            return result
    '''
    docstring: str = Field(..., description="Verbose Documentation for the DSPy Module")
    class_name: str = Field(..., description="Class name combining the inputs and outputs")
    inputs: list[str] = Field(..., description="Inputs for dspy.Module")
    output: str = Field(..., description="Output for dspy.Module")


@app.command(name="new")
def new_module(prompt: str):
    """Generate a new dspy.Module. Example: dspygen module new 'text -> summary'"""
    init_dspy()

    tmpl_model = gen_pydantic_instance_call(prompt, DSPyModuleTemplate)

    source = render(dspy_module_template, model=tmpl_model)

    file_name = file_name_call(source + "\nName the file by the class name.", "py")

    with open(dspy_modules_dir() / file_name, "w") as file:
        file.write(source)

    print(source)

    print(f"Module saved to {dspy_modules_dir() / file_name}")


def load_commands(directory: str = "modules"):
    subcommands_dir = source_dir() / directory

    for filename in os.listdir(subcommands_dir):
        if filename.endswith("_module.py"):
            module_name = f'{__name__.split(".")[0]}.{directory}.{filename[:-3]}'
            module = import_module(module_name)
            if hasattr(module, "app"):
                app.add_typer(module.app, name=filename[:-10])


def main():
    print('main')


load_commands()

if __name__ == '__main__':
    main()
