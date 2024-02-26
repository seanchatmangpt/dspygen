import inspect
import json
from collections.abc import Callable
from json import JSONDecodeError
from textwrap import dedent
from typing import Optional

import loguru

from dspygen.typetemp.template.typed_template import TypedTemplate
from dspygen.utils.complete import achat, create
from dspygen.utils.file_tools import write
from dspygen.utils.models import get_model

create_jinja_template = """
Objective:
Transform the given input (whether it's template data, text, or another form of structured data)
into a Jinja2 template that follows best practices and is easy to maintain. Ensure it leverages
Jinja2's features effectively. Use Jinja2's template syntax and filters appropriately.

You are generating a Jinja2 template for a specific task. The template should be ready to be used
in a production environment.

```prompt
{{prompt}}
```

"""


def create_jinja(prompt, max_tokens=2500, model=None, filepath=None, temperature=0.7):
    """Generate a Jinja2 template based on the given prompt."""
    create_prompt = TypedTemplate(source=create_python_template, prompt=prompt)()

    return __create(
        prompt=create_prompt,
        filepath=filepath,
        md_type="jinja",
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


create_code_template = """You are a {{ language }} PerfectProductionCode® assistant. Convert the prompt into code.

```prompt
{{ prompt }}
```

Here is your PerfectProductionCode® AGI {{ language }} response within triple backticks:
"""


def create_code(
    prompt, language="code", max_tokens=2500, model=None, filepath=None, temperature=0.7
):
    instructions = "Create a working example from this"  # spr(prompt, encode=False, max_tokens=100)
    # print(instructions)
    create_prompt = TypedTemplate(
        source=create_code_template,
        language=language,
        prompt=f"{instructions} {prompt}",
    )()

    return __create(
        prompt=create_prompt,
        filepath=filepath,
        md_type=language,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


__create_template = """
{{prompt}}
```{{md_type}} (Here is your PerfectPythonProductionCode® AGI response within triple backticks)
{{suffix}}
"""


create_python_template = """
Objective:
Transform the given input (whether it's Python code, project documentation, or another form of structured data)
into PYTHON CODE that aligns with the Pythonic practices Luciano Ramalho would advocate for based on his
teachings in "Fluent Python". Ensure it's idiomatic, concise, and leverages Python's features effectively.
Use the standard library and built-in functions unless the library is specified in the prompt.
Use functional programming without classes. Do not use the keyword pass.

You are generating answer code for a job interview question. The code should be production-ready and
ready to be deployed to a production environment.

```prompt
{{prompt}}
```

# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.
"""


def create_python(prompt, max_tokens=2500, model=None, filepath=None, temperature=0.7):
    """Generate Python code based on the given prompt."""
    create_prompt = TypedTemplate(source=create_python_template, prompt=prompt)()

    return __create(
        prompt=create_prompt,
        filepath=filepath,
        md_type="python",
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


__create_template = """
{{prompt}}
```{{md_type}}
{{suffix}}
"""


def __create(
    prompt,
    md_type="text",
    max_tokens=2500,
    model=None,
    filepath=None,
    temperature=0.0,
    stop=None,
    suffix="",
):
    create_prompt = TypedTemplate(
        source=__create_template, prompt=prompt, md_type=md_type, suffix=suffix
    )()

    # # print(create_prompt)

    result = create(
        prompt=create_prompt,
        model=model,
        stop=["```"] + (stop or []),
        max_tokens=max_tokens,
        temperature=temperature,
    )
    # # print(f"Prompt: {result}")
    # # print(f"Result: {result}")

    if filepath:
        write(contents=result, filename=filepath)

    return result


def __chat(
    prompt,
    md_type="text",
    max_tokens=2500,
    filepath=None,
    temperature=0.0,
    model="gpt4",
    **kwargs,
):
    model = get_model(model)

    prompt = dedent(
        f"""
    {prompt}
    ```{md_type}\n# Here is your PerfectPythonProductionCode® AGI response. Tests have been written to a different file:\n"""
    )
    result = achat(prompt=prompt, model=model)
    loguru.logger.info(f"Prompt: {result}")
    loguru.logger.info(f"Result: {result}")

    if filepath:
        write(contents=result, filename=filepath)

    return result


def spr(prompt, encode=True, model="3i", max_tokens=250, temperature=0.0):
    """Create a Sparse Priming Representation (SPR) from the given prompt."""
    encode_prompt = dedent(
        f"""
# INSTRUCTIONS: You are tasked with generating a Sparse Priming Representation (SPR) from the provided text. SPRs encapsulate information in a highly compressed format. Your objective is to condense the given content, focusing on its essence, and represent it within a fraction of its original length. Abide by the following principles:

- Extract core ideas, disregarding specific examples or detailed explanations.
- Maintain critical relationships and underlying principles.
- Use succinct, clear language, aiming for maximum compression with minimum loss of essential content.

Do not include any references or content outside of the given input.
Your output should be a distilled SPR, 5x than the original text. Use emergent properties within the model to generate the SPR.
It is not intended to be human readable. Use these techniques to achieve the desired compression:
Symbolic Representation
Conceptual Abstraction
Referential Indicators
Data Compression Techniques
Nonlinear Structuring
Encoded Semantics
Mathematical and Logical Constructs
Metasymbols and Metaconcepts

    ```input
    {prompt}
    ```


    ```spr output\n
    """
    )

    decode_prompt = dedent(
        f"""

# INSTRUCTIONS: You are presented with a Sparse Priming Representation (SPR). Your task is to decode this SPR, expanding it into a detailed, coherent piece of content. The SPR contains highly compressed information, and your goal is to unpack it, elaborating on the concepts and relationships it alludes to. Follow these guidelines:

- Interpret the concise cues in the SPR to rebuild detailed content.
- Provide examples, explanations, and relevant details that align with the themes in the SPR.
- Ensure the expanded text logically connects and fully represents the original information compressed in the SPR.

Do not reference any external content; rely solely on the SPR for your expansion. Generate a comprehensive, detailed output that faithfully represents the original content behind the SPR.

    ```spr
    {prompt}
    ```

    ```output\n"""
    )

    if encode:
        result = create(
            prompt=encode_prompt,
            model=model,
            stop=["```"],
            max_tokens=max_tokens,
            temperature=temperature,
        )
    else:
        result = create(
            prompt=decode_prompt,
            model=model,
            stop=["```"],
            max_tokens=max_tokens,
            temperature=temperature,
        )

    return result


create_evo_template = """
# Task: Automatically generate a YAML configuration for the prompt.
This configuration must be based on Domain-Driven Design principles,
outlining Entities, Value Objects, and Business Functions.

# Instructions:

# Step 1: Define Value Objects
# These are elements without identity, describing characteristics. They are immutable.
value_objects:
  - name: "ValueObjectName"
    definition: "Provide a clear, concise description."
    properties:
      - name: "name_of_property"
        type: "primitive_type"
      # Add more properties as required for the description (6 maximum).

# Step 2: Detail Entities
# These have unique identities and undergo various states and behaviors.
entities:
  - name: "EntityName"
    definition: "Provide a clear, concise description."
    value_objects:
      - "List associated Value Objects by name"

# Step 3: Describe Business Functions
# These operations are performed on Entities and Value Objects, following Design by Contract principles.
business_functions:
  - entity: "Specify the associated entity"
    name: "name_of_function"
    parameters:
      - parameter: "name_of_parameter"
        type: "primitive_type or value_object"
    definition: "Provide a clear, concise description of function's purpose."
    contract:
      pre:
        - condition: "icontract ensure condition in lambda format"
      post:
        - condition: "icontract require condition in lambda format"

# Step 4: Additional Information
# Provide any extra context or clarification about the domain configuration.
additional_info:
  - key: "Specify the context topic"
    value: "Give detailed information or instructions"

# Reminder: Replace all placeholder text with actual, relevant information.
Ensure data consistency and accuracy, adhering to the YAML hierarchical
structure for successful parsing.

# Step 5: Generate YAML Configuration from Prompt following the schema exactly
that means that the output should be a valid YAML file that follows the schema above.


```domain prompt
{{prompt}}
```

"""


def create_evo(prompt, max_tokens=2500, model=None, filepath=None, temperature=0.0):
    create_prompt = TypedTemplate(source=create_evo_template, prompt=prompt)()

    result = __create(
        prompt=create_prompt,
        md_type="domain yaml",
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        suffix='# AGI Simulations of Luciano Ramahlo from "Fluent Python" and '
        'David Thomas and Andrew Hunt from "The Pragmatic Programmer" have created this'
        " YAML representation of the domain specified in the prompt.\nvalue_objects:\n",
    )

    result = "value_objects:\n  " + result

    if filepath:
        write(contents=result, filename=filepath)

    return result


def main2():
    satisfy = """Recent efforts have augmented large language models (LLMs) with external resources (e.g.,
    the Internet) or internal control flows (e.g., prompt chaining) for tasks requiring grounding or reasoning,
    leading to a new class of language agents. While these agents have achieved substantial empirical success,
    we lack a systematic framework to organize existing agents and plan future developments. In this paper,
    we draw on the rich history of cognitive science and symbolic artificial intelligence to propose Cognitive
    Architectures for Language Agents (CoALA). CoALA describes a language agent with modular memory components,
    a structured action space to interact with internal memory and external environments, and a generalized
    decision-making process to choose actions. We use CoALA to retrospectively survey and organize a large body of
    recent work, and prospectively identify actionable directions towards more capable agents. Taken together,
    CoALA contextualizes today's language agents within the broader history of AI and outlines a path towards
    language-based general intelligence."""

    enc = spr(satisfy)

    # print(enc)

    dec = spr(enc, encode=False)

    # print(dec)

    action_space = """ CoALA also includes a structured action space. This refers to the set of
    actions that an agent can take in response to a given situation. By organizing these actions in a structured
    manner, CoALA agents are able to make more informed decisions and carry out more complex tasks."""

    # evo = create_evo(dec, filepath="coala_evo.yaml")
    # evo = create_evo(, filepath="action_space_evo.yaml")

    # # print(evo)


def gen_evo():
    """ """
    action_space = """ CoALA also includes a structured action space. This refers to the set of
    actions that an agent can take in response to a given situation. By organizing these actions in a structured
    manner, CoALA agents are able to make more informed decisions and carry out more complex tasks."""

    # evo = create_evo(dec, filepath="coala_evo.yaml")
    evo = create_evo(action_space, filepath="action_space_evo.yaml")


create_tailwind_landing_template = """Take the prompt and generate a landing component.
Do not reference yourself or anything other than what is contained within the prompt.

The design must be modern, with a fresh and professional color scheme that aligns with industry standards (blues, yellows, and whites).
Use large, readable typography and include visually appealing separators between sections. No images.

The component should be fully responsive, ensuring a seamless experience on all devices, including tablets and smartphones.

Ensure the design follows best practices for web accessibility,
such as alt text for visual elements, keyboard navigation, and proper contrast ratios.

```prompt
{{ prompt }}
```

```html
"<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
    <title>{{ title }}</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
"""


def create_tailwind_landing(
    prompt="",
    max_tokens=2500,
    model=None,
    filepath=None,
    temperature=0.0,
    title="Landing Page",
):
    prompt = create(
        prompt=f"Convert into a PRD for a landing component for {prompt}\n\n```prd\n",
        stop=["```"],
    )

    # print(prompt)

    create_prompt = TypedTemplate(
        source=create_tailwind_landing_template, prompt=prompt, title=title
    )()

    landing = __create(
        prompt=create_prompt,
        md_type="html",
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    markup = """<!DOCTYPE html>
         <html lang="en">
         <head>
           <meta charset="UTF-8">
           <title>Landing component</title>
           <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></head><body>"""
    markup += landing

    if filepath:
        with open(filepath, "w") as f:
            f.write(markup)


def create_data(
    prompt: str, cls: type, model: Optional[str] = None, max_tokens: int = 2000
) -> dict:
    """Create a dict of data from a prompt that can be passed to the given class as kwargs"""
    instructions = dedent(
        f"""Create a JSON response that contains data corresponding to the class {cls.__name__} based on the prompt.
    The json loads like this: json.loads(response)
    This is going to be used to create an instance of {cls.__name__}. It will crash if you add any additional information.
    After the JSON, provide a doctoral thesis explaining your thought process.

    ```python
    {inspect.getsource(cls)}
    ```

    ```prompt
    {prompt}
    ```

    Complete the following JSON response:
    ```json
    {{"""
    )

    # print(instructions)
    result = create(
        prompt=instructions, stop=["```", "\n\n"], max_tokens=max_tokens, model=model
    )

    # Safely evaluate to expected type
    try:
        extracted_dict = json.loads("{" + result.replace("\n", ""))

        if not isinstance(extracted_dict, dict):
            raise TypeError(f"Expected dict, got {type(extracted_dict)}.")

        return extracted_dict
    except (SyntaxError, TypeError, JSONDecodeError) as e:
        loguru.logger.warning(f"Invalid {cls.__name__} generated: {e} {result}")
        fix_instructions = dedent(
            f"""You are a JSON fixing assistant.
        Please fix the following json so that it can be used to
        create an instance of {cls.__name__}:\n\n{result}\n\n

        ```json
        {{"""
        )

        corrected_result = create(
            prompt=fix_instructions,
            stop=["```"],
            max_tokens=2000,
        )
        return json.loads("{" + corrected_result.replace("\n", ""))


def create_kwargs(prompt: str, cabal: Callable) -> dict:
    """Create a dict of data from a prompt that can be passed to the given class as kwargs"""
    instructions = dedent(
        f"""
    Create a JSON object that contains data corresponding to the kwargs {cabal.__name__} based on the prompt.
    Do not add any additional information to the JSON. Only use the information provided in the prompt.
    This is going to be used to call of {cabal.__name__}. It will crash if you add any additional information.
    Provide values for all the fields in the class.
    After the JSON, provide a doctoral thesis explaining your thought process.

    ```python
    {inspect.getsource(cabal)}
    ```

    ```prompt
    {prompt}
    ```

    Complete the following code block:
    ```json
    {{"""
    )

    # print(instructions)
    result = create(
        prompt=instructions,
        stop=["```", "\n\n"],
        max_tokens=2000,
    )

    # Safely evaluate to expected type
    try:
        extracted_dict = json.loads("{" + result.replace("\n", ""))

        if not isinstance(extracted_dict, dict):
            raise TypeError(f"Expected dict, got {type(extracted_dict)}.")

        return extracted_dict
    except (SyntaxError, TypeError, JSONDecodeError) as e:
        loguru.logger.warning(f"Invalid {cabal.__name__} generated: {e} {result}")
        fix_instructions = dedent(
            f"""You are a JSON fixing assistant.
            Please fix the following json so that it can be used to
            create kwargs:
            {result}

            ```json
            {{"""
        )

        corrected_result = create(
            prompt=fix_instructions,
            stop=["```", "\n\n"],
            max_tokens=2000,
        )
        # print("corrected_result", corrected_result)
        return json.loads("{" + corrected_result.replace("\n", ""))


def create_pydantic_class(
    prompt: str,
    class_name: Optional[str] = None,
    min_fields=2,
    max_fields=5,
    file_path=None,
) -> str:
    """Generate a Pydantic class based on a prompt.

    Args:
        prompt (str): The prompt describing the class fields.
        class_name (str): The name for the generated Pydantic class.

    Returns:
        type: The generated Pydantic class.
    """
    if not class_name:
        name_prompt = f"""You are a Pydantic class naming assistant.
        Be Descriptive: Choose a name that describes what the model represents. For example, User, BlogPost, Invoice. Avoid generic names like Data or Model.
Be Specific: Pick specific names over broad ones when possible. BlogPost is better than Post, InvoiceItem over Item.
Use Capitalized Camel Case: Follow PEP8 convention of CapWords for model names - BasicAuth not basicAuth.
Consider the Module Name: Names should be unique within a module. Prefix with parent name if reuse possible - accounts.User vs posts.User.
Keep Names Unique: Add suffixes like BlogPostIn, BlogPostOut if class represents different forms of same entity.
Avoid Abbreviations: Spell names out fully for clarity - Request rather than Req.
Be Consistent with Domain Language: Use the same terminology as your core business domain.
Limit Name Length: Long names reduce readability. Try to keep under 3 words, 20 chars.
Use Pluralization Judiciously: Generally prefer singular - Order vs Orders.
Follow Conventions if Industry Standard: Sometimes best to align with widely used terms.

Choose a name for this prompt
```prompt
{prompt}
```

The name is: """
        class_name = create(prompt=name_prompt, max_tokens=100)
        # # print("The name is: ", class_name)

    # # print(class_name)
    instructions = dedent(
        f"""You are a expert Pydantic class assistant.

        Define a Pydantic class `{class_name}` with the on the prompt:

        Only use the Field class not primitives

        The class should have between {min_fields} and {max_fields} fields. It will crash if you do not follow constraints.

        ```prompt
        {prompt}
        ```

        Complete the following code block, make sure to stay within constraints:
        ```python
        # I have made sure there are only primitives in the dict, no classes or functions.
        # I have made sure there are {min_fields} to {max_fields} fields.
        from pydantic import BaseModel

        class {class_name}(BaseModel):
            '''The total number of fields is"""
    )

    result = create(
        prompt=instructions,
        stop=["```"],
        max_tokens=2000,
    )

    cls_code = f"""from pydantic import BaseModel\n\n
    class {class_name}(BaseModel):\n{result}"""

    # cls_code = fix_code(cls_code)

    if file_path:
        write(contents=cls_code, filename=file_path)

    return cls_code


create_git_patch_template = """You are a git patch assistant. Create a git patch from the prompt.
The format is the same as if running the command `git format-patch -1 HEAD`.
After the patch, provide a doctoral thesis explaining your thought process.

```prompt
{{ prompt }}
```

"""


def create_git_patch(prompt: str, max_tokens=2500, model=None, filepath=None):
    """Generate a git patch based on a prompt."""
    create_prompt = TypedTemplate(source=create_git_patch_template, prompt=prompt)()

    result = __create(
        prompt=create_prompt,
        md_type="git",
        model=model,
        max_tokens=max_tokens,
        suffix="From",
    )

    if filepath:
        write(contents=result, filename=filepath)

    return result


import anyio


def main2():
    prompt = """ADSC is a key Scriptcase Partner for Canada. Scriptcase is a strong
    Business Intelligence & Web Application Code Generator platform used by
    thousands of users in over 140 countries globally that can supercharge &
    empower your web applications. Access corporate data securely on the web.
    ADSC can provide licenses/ development/training.

    Make the values extremely verbose and detailed. Do not use any abbreviations."""
    # data = create_data(prompt, VRIO)
    # # data = create_data(prompt, SWOTAnalysis)
    # # print(data)
    cls = create_pydantic_class(prompt, "ADSC", file_path="adsc_model.py")
    # print(cls)


import subprocess

import typer


def create_cli_arguments(prompt: str) -> list:
    """Create a list of command-line arguments for a subcommand with optional options.
    Example usage: create_cli_arguments("subcommand_name", {"--option": "value"})
    """
    instructions = f"""Create a JSON list that contains arguments to be used in a command line interface (CLI) invocation
        cli_invocation = [command] + create_cli_arguments(prompt)

        # Run the CLI command and capture the output
        output = subprocess.check_output(cli_invocation, text=True)

Instructions:
1. You are tasked with generating a list of arguments that will be used in a CLI invocation.
2. These arguments should be in a JSON list format, with each element representing an argument.
3. Ensure that the arguments are appropriate for the CLI command that will be invoked.
4. Do not add any arguments that are not allowed, it will cause a crash


USER PROMPT
```prompt
{prompt}
```

USER JSON Argument List:
```json
["""

    result = create(
        prompt=instructions,
        stop=["```", "\n\n"],
        max_tokens=2000,
    )

    # Safely evaluate to expected type
    try:
        extracted_dict = json.loads("[" + result.replace("\n", ""))

        if not isinstance(extracted_dict, dict):
            raise TypeError(f"Expected dict, got {type(extracted_dict)}.")

        return extracted_dict
    except (SyntaxError, TypeError, JSONDecodeError):
        fix_instructions = dedent(
            f"""You are a JSON fixing assistant.
            Please fix the following json so that it can be used to
            create kwargs:
            {result}

            ```json
            ["""
        )

        corrected_result = create(
            prompt=fix_instructions,
            stop=["```", "\n\n"],
            max_tokens=2000,
        )
        return json.loads("[" + corrected_result.replace("\n", ""))


def create_cli_invocation(prompt, command=None):
    """Create a CLI invocation command with the given command and arguments.
    Example usage: create_cli_invocation("your_app.py", ["subcommand", "--option", "value"])
    """
    try:
        if command is None:
            command = create(
                prompt=f"""What is the name of the command to call in the prompt?
            ```prompt
            {prompt}
            ```
            Respond with one word
            Command: """,
                stop=[" ", "\n"],
            )
        print(command)

        # Construct the CLI invocation command
        args = create_cli_arguments(prompt)
        cli_invocation = [command] + args

        # Run the CLI command and capture the output
        output = subprocess.check_output(cli_invocation, text=True)

        return output.strip()
    except subprocess.CalledProcessError as e:
        # Handle errors if the CLI command fails
        typer.echo(f"Error running CLI command: {e}")
        return None


def main():
    result = create_cli_invocation(
        "python my_script.py --input-file input.txt --output-file output.txt --verbose"
    )
    print(len(result))


if __name__ == "__main__":
    anyio.run(main)
