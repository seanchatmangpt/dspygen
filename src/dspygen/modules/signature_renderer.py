from pydantic import BaseModel, Field

import dspy
from dspy import Signature
from dspy.signatures.field import InputField, OutputField

# from dspygen.modules.gen_pydantic_instance_module import gen_pydantic_instance_call
from dspygen.typetemp.template.typed_template import TypedTemplate


class InputFieldTemplateSpecModel(BaseModel):
    """Defines an input field for a DSPy Signature."""

    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str | None = Field(
        None,
        description="Optional additional context or labeling for the input field.",
    )
    desc: str = Field(
        ...,
        description="Description of the input field's purpose or the nature of content it should contain.",
    )


class OutputFieldTemplateSpecModel(BaseModel):
    """Defines an output field for a DSPy Signature."""

    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str | None = Field(
        None,
        description="Optional additional context or labeling for the output field.",
    )
    desc: str = Field(
        ...,
        description="Description of the output field's purpose or the nature of content it should contain.",
    )


class SignatureTemplateSpecModel(BaseModel):
    '''
        Generate a Signature for the DSPy Framework.

        Examples:
        ```python
    class CheckCitationFaithfulness(dspy.Signature):
        """Verify that the text is based on the provided context."""

        context = dspy.InputField(desc="facts here are assumed to be true")
        text = dspy.InputField()
        faithfulness = dspy.OutputField(desc="True/False indicating if text is faithful to context")

    class GenerateAnswer(dspy.Signature):
        """Answer questions with short factoid answers."""

        context = dspy.InputField(desc="contains cited relevant facts")
        question = dspy.InputField()
        answer = dspy.OutputField(desc="Descriptive answer to the question")

    class CheckForCitations(dspy.Signature):
        """Verify the text has proper citations."""

        context = dspy.InputField(desc="facts here are assumed to be true")
        text = dspy.InputField()
        cited = dspy.OutputField(desc="True/False indicating if citations are present")
        ```
    '''

    class_name: str = Field(
        ...,
        description="Signature class name. Use this to specify additional context or labeling.",
    )
    instructions: str = Field(
        ..., description="Documentation of the task's expected LM function and output."
    )
    input_fields: list[InputFieldTemplateSpecModel]
    output_fields: list[OutputFieldTemplateSpecModel]


def create_signature_class_from_model(model: SignatureTemplateSpecModel) -> type:
    """Create a DSPy Signature class from a Pydantic model.

    :param model: The Pydantic model to convert.
    :return: A DSPy Signature class.
    """
    class_dict = {"__doc__": model.instructions, "__annotations__": {}}

    # Process input fields
    for field in model.input_fields:
        input_field = InputField(prefix=field.prefix, desc=field.desc)
        class_dict[field.name] = input_field
        class_dict["__annotations__"][field.name] = InputField

    # Process output fields
    for field in model.output_fields:
        output_field = OutputField(prefix=field.prefix, desc=field.desc)
        class_dict[field.name] = output_field
        class_dict["__annotations__"][field.name] = OutputField

    # Dynamically create the Signature class
    signature_class = type(model.class_name, (Signature,), class_dict)
    return signature_class


class GenDSPySignatureTemplate(TypedTemplate):
    """
    Generates and renders DSPy Signature classes to disk using Jinja2 templates.
    """

    source = '''from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class {{ signature.class_name }}(Signature):
    """
    {{ signature.instructions }}
    """
    {% for input_field in signature.input_fields %}
    {{ input_field.name }} = InputField(desc="{{ input_field.desc }}")
    {% endfor %}

    {% for output_field in signature.output_fields %}
    {{ output_field.name }} = OutputField(desc="{{ output_field.desc }}")
    {% endfor %}
    '''
    to = "signatures/{{ signature.class_name | underscore }}.py"


business_sig_prompts = [
    "I need a signature called 'CodeInterviewSolver' that inputs a 'problem_statement', and outputs a 'detailed_code_solution'. This signature should first interpret the problem statement to identify key challenges and requirements. Each line of the code solution must be accompanied by comments that explain the purpose and logic of that line, ensuring that the thought process behind the solution is clear and educational. The aim is to not only solve the interview problem but also to provide a learning experience by demystifying complex solution steps and fostering a deeper understanding of algorithmic thinking and coding practices.",
]


# Assuming we have a function `generate_signature_from_prompt` that takes a sig_prompt and processes it.
def generate_signature_from_prompt(sig_prompt):
    # This function is a placeholder for the actual logic that would generate a signature model from a prompt.
    # sig_instance = gen_pydantic_instance_call(
    #     sig_prompt,
    #     root_model=SignatureTemplateSpecModel,
    #     child_models=[InputFieldTemplateSpecModel, OutputFieldTemplateSpecModel],
    # )

    # print(sig_instance)
    return None  # GenDSPySignatureTemplate(signature=sig_instance)()


def main():
    lm = dspy.OpenAI(max_tokens=500, model="gpt-4")
    dspy.settings.configure(lm=lm)

    # Now, let's call this function for each prompt in the list.
    print(generate_signature_from_prompt("celebrity, gossip -> tweet"))


if __name__ == "__main__":
    main()
