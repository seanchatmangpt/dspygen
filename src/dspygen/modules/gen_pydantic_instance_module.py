import ast
import dspy
import inspect
import logging
from typing import Optional, TypeVar, cast

from pydantic import BaseModel, ValidationError

from dspy import Assert, ChainOfThought, InputField, OutputField, Signature

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def eval_dict_str(dict_str: str) -> dict:
    """Safely convert str to dict"""
    return ast.literal_eval(dict_str)


class PromptToPydanticInstanceSignature(Signature):
    """Synthesize the prompt into the kwargs to fit the model.
    Do not duplicate the field descriptions
    """

    root_pydantic_model_class_name = InputField(
        desc="The class name of the pydantic model to receive the kwargs"
    )
    pydantic_model_definitions = InputField(
        desc="Pydantic model class definitions as a string"
    )
    prompt = InputField(
        desc="The prompt to be synthesized into data. Do not duplicate descriptions"
    )
    root_model_kwargs_dict = OutputField(
        prefix="kwargs_dict: dict = ",
        desc="Generate a Python dictionary as a string with minimized whitespace that only contains json valid values.",
    )


class PromptToPydanticInstanceErrorSignature(Signature):
    """Synthesize the prompt into the kwargs fit the model"""

    error = InputField(desc="Error message to fix the kwargs")

    root_pydantic_model_class_name = InputField(
        desc="The class name of the pydantic model to receive the kwargs"
    )
    pydantic_model_definitions = InputField(
        desc="Pydantic model class definitions as a string"
    )
    prompt = InputField(desc="The prompt to be synthesized into data")
    root_model_kwargs_dict = OutputField(
        prefix="kwargs_dict = ",
        desc="Generate a Python dictionary as a string with minimized whitespace that only contains json valid values.",
    )


T = TypeVar("T", bound=BaseModel)


class GenPydanticInstance(dspy.Module):
    """A module for generating and validating Pydantic model instances based on prompts.

    Usage:
        To use this module, instantiate the GenPydanticInstance class with the desired
        root Pydantic model and optional child models. Then, call the `forward` method
        with a prompt to generate Pydantic model instances based on the provided prompt.
    """

    def __init__(
        self,
        root_model: type[T],
        child_models: Optional[list[type[BaseModel]]] = None,
        generate_sig=PromptToPydanticInstanceSignature,
        correct_generate_sig=PromptToPydanticInstanceErrorSignature,
    ):
        super().__init__()

        self.models = [root_model]  # Always include root_model in models list

        if child_models:
            self.models.extend(child_models)

        self.output_key = "root_model_kwargs_dict"
        self.root_model = root_model

        # Concatenate source code of models for use in generation/correction logic
        self.model_sources = "\n".join(
            [inspect.getsource(model) for model in self.models]
        )

        # Initialize DSPy ChainOfThought modules for generation and correction
        self.generate = ChainOfThought(generate_sig)
        self.correct_generate = ChainOfThought(correct_generate_sig)
        self.validation_error = None

    def validate_root_model(self, output: str) -> bool:
        """Validates whether the generated output conforms to the root Pydantic model."""
        try:
            model_inst = self.root_model.model_validate(eval_dict_str(output))
            return isinstance(model_inst, self.root_model)
        except (ValidationError, ValueError, TypeError, SyntaxError) as error:
            self.validation_error = error
            logger.debug(f"Validation error: {error}")
            return False

    def validate_output(self, output) -> T:
        """Validates the generated output and returns an instance of the root Pydantic model if successful."""
        Assert(
            self.validate_root_model(output),
            f"""You need to create a kwargs dict for {self.root_model.__name__}\n
            Validation error:\n{self.validation_error}""",
        )

        return self.root_model.model_validate(eval_dict_str(output))

    def forward(self, prompt) -> T:
        """Takes a prompt as input and generates a Python dictionary that represents an instance of the
        root Pydantic model. It also handles error correction and validation.
        """
        output = self.generate(
            prompt=prompt,
            root_pydantic_model_class_name=self.root_model.__name__,
            pydantic_model_definitions=self.model_sources,
        )

        output = output[self.output_key]

        try:
            return self.validate_output(output)
        except (AssertionError, ValueError, TypeError) as error:
            logger.error(f"Error {error!s}\nOutput:\n{output}")

            # Correction attempt
            corrected_output = self.correct_generate(
                prompt=prompt,
                root_pydantic_model_class_name=self.root_model.__name__,
                pydantic_model_definitions=self.model_sources,
                error=f"str(error){self.validation_error}",
            )[self.output_key]

            return self.validate_output(corrected_output)

    def __call__(self, prompt):
        return self.forward(prompt=prompt)


def gen_pydantic_instance_call(prompt, root_model, child_models=None):
    model_module = GenPydanticInstance(root_model=root_model, child_models=child_models)
    model_inst = model_module(prompt)
    return model_inst
