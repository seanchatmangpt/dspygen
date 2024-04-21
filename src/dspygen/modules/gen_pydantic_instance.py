import ast
import dspy
import logging
from typing import TypeVar
from typing import Type, Set
import inspect

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
        model: Type[T],
        generate_sig=PromptToPydanticInstanceSignature,
        correct_generate_sig=PromptToPydanticInstanceErrorSignature,
    ):
        super().__init__()

        self.output_key = "root_model_kwargs_dict"
        self.model = model

        # Concatenate source code of models for use in generation/correction logic
        self.model_sources = get_model_source(model)

        # Initialize DSPy ChainOfThought modules for generation and correction
        self.generate = ChainOfThought(generate_sig)
        self.correct_generate = ChainOfThought(correct_generate_sig)
        self.validation_error = None

    def validate_root_model(self, output: str) -> bool:
        """Validates whether the generated output conforms to the root Pydantic model."""
        try:
            model_inst = self.model.model_validate(eval_dict_str(output))
            return isinstance(model_inst, self.model)
        except (ValidationError, ValueError, TypeError, SyntaxError) as error:
            self.validation_error = error
            logger.debug(f"Validation error: {error}")
            return False

    def validate_output(self, output) -> T:
        """Validates the generated output and returns an instance of the root Pydantic model if successful."""
        Assert(
            self.validate_root_model(output),
            f"""You need to create a kwargs dict for {self.model.__name__}\n
            Validation error:\n{self.validation_error}""",
        )

        return self.model.model_validate(eval_dict_str(output))

    def forward(self, prompt) -> T:
        """Takes a prompt as input and generates a Python dictionary that represents an instance of the
        root Pydantic model. It also handles error correction and validation.
        """
        output = self.generate(
            prompt=prompt,
            root_pydantic_model_class_name=self.model.__name__,
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
                root_pydantic_model_class_name=self.model.__name__,
                pydantic_model_definitions=self.model_sources,
                error=f"str(error){self.validation_error}",
            )[self.output_key]

            return self.validate_output(corrected_output)

    def __call__(self, prompt):
        return self.forward(prompt=prompt)


class GenPydanticDict(dspy.Module):
    """A module for generating and validating dicts for Pydantic instances on prompts.

    Usage:
        To use this module, instantiate the GenPydanticInstance class with the desired
        root Pydantic model and optional child models. Then, call the `forward` method
        with a prompt to generate Pydantic model instances based on the provided prompt.
    """

    def __init__(
        self,
        model: Type[T],
        generate_sig=PromptToPydanticInstanceSignature,
        correct_generate_sig=PromptToPydanticInstanceErrorSignature,
    ):
        super().__init__()

        self.output_key = "root_model_kwargs_dict"
        self.model = model

        # Concatenate source code of models for use in generation/correction logic
        self.model_sources = get_model_source(model)

        # Initialize DSPy ChainOfThought modules for generation and correction
        self.generate = ChainOfThought(generate_sig)
        self.correct_generate = ChainOfThought(correct_generate_sig)
        self.validation_error = None

    def validate_root_model(self, output: str) -> bool:
        """Validates whether the generated output conforms to the root Pydantic model."""
        try:
            model_inst = self.model.model_validate(eval_dict_str(output))
            return isinstance(model_inst, self.model)
        except (ValidationError, ValueError, TypeError, SyntaxError) as error:
            self.validation_error = error
            logger.debug(f"Validation error: {error}")
            return False

    def validate_output(self, output) -> dict:
        """Validates the generated output and returns an instance of the root Pydantic model if successful."""
        Assert(
            self.validate_root_model(output),
            f"""You need to create a kwargs dict for {self.model.__name__}\n
            Validation error:\n{self.validation_error}""",
        )

        output_dict = eval_dict_str(output)

        self.model.model_validate(output_dict)

        return output_dict

    def forward(self, prompt) -> dict:
        """Takes a prompt as input and generates a Python dictionary that represents an instance of the
        root Pydantic model. It also handles error correction and validation.
        """
        output = self.generate(
            prompt=prompt,
            root_pydantic_model_class_name=self.model.__name__,
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
                root_pydantic_model_class_name=self.model.__name__,
                pydantic_model_definitions=self.model_sources,
                error=f"{str(self.validation_error)}",
            )[self.output_key]

            return self.validate_output(corrected_output)

    def __call__(self, prompt):
        return self.forward(prompt=prompt)


def get_model_source(model: Type[BaseModel], already_seen: Set[Type[BaseModel]] = None) -> str:
    """
    Recursively grab the source code of a given Pydantic model and all related models, including the inheritance chain.

    Args:
        model: The Pydantic model class to extract source code for.
        already_seen: A set of models that have already been processed to avoid infinite recursion.

    Returns:
        A string containing the Python source code for the model and all related models.
    """
    if already_seen is None:
        already_seen = set()

    if model in already_seen:
        return ""
    already_seen.add(model)

    source = inspect.getsource(model)

    # Inspect base classes for inheritance until BaseModel is reached
    for base in model.__bases__:
        if base is not BaseModel and issubclass(base, BaseModel):
            base_source = get_model_source(base, already_seen)
            if base_source:
                source = base_source + "\n\n" + source

    # Use model.__annotations__ to get the type of each field
    for field_name, field_type in model.__annotations__.items():
        # If it is a list, get the type of the list items
        if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
            list_item_type = field_type.__args__[0]
            if issubclass(list_item_type, BaseModel) and list_item_type not in already_seen:
                list_item_source = get_model_source(list_item_type, already_seen)
                source += "\n\n" + list_item_source

        # Check if the field is a subclass of BaseModel to identify Pydantic models
        try:
            if issubclass(field_type, BaseModel) and field_type not in already_seen:
                field_source = get_model_source(field_type, already_seen)
                source += "\n\n" + field_source
        except TypeError:
            # Not a class, ignore
            pass

    return source


def main():
    import dspy

    from dspygen.rdddy.event_storm_domain_specification_model import EventStormingDomainSpecificationModel

    lm = dspy.OpenAI(max_tokens=2000)
    dspy.settings.configure(lm=lm)

    model_module = GenPydanticInstance(EventStormingDomainSpecificationModel)
    model_inst = model_module("Create a new user account with email and password.")
    print(model_inst)


def instance(model: Type[BaseModel], prompt: str) -> BaseModel:
    model_module = GenPydanticInstance(model)
    return model_module(prompt)


if __name__ == "__main__":
    main()
