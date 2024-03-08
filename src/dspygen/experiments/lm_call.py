"""

"""
import ast
import inspect
from pydantic import BaseModel

from typing import TypeVar, Type, Set

import dspy
from dspygen.utils.dspy_tools import init_dspy

T = TypeVar("T", bound=BaseModel)


def eval_dict_str(dict_str: str) -> dict:
    """Safely convert str to dict"""
    return ast.literal_eval(dict_str)


class CallModuleSignature(dspy.Signature):
    """
    Signature for calling a Python callable with a specified prompt and returning the result.
    We only care about the return annotation not the parameters.
    """
    python_callable = dspy.InputField(desc="The Python callable to be invoked.")
    prompt = dspy.InputField(desc="The prompt to pass to the callable to turn into return_annotation_kwargs_dict.")
    return_annotation_class_name = dspy.InputField(desc="The class name of the return annotation.")

    kwargs_dict = dspy.OutputField(prefix="return_annotation_kwargs_dict = ",
                                   desc="The result returned by the callable when invoked with the prompt. "
                                        "You must only return python primitives. No classes or functions.")


class CallModule(dspy.Module):
    """CallModule"""

    def forward(self, cable, prompt):
        output_key = "kwargs_dict"
        pred = dspy.ChainOfThought(CallModuleSignature)
        # source code of cable
        sig = inspect.signature(cable)

        python_callable = "" # "You are a return annotation kwargs dict assistant\n"

        # get the source of each parameter since it is a pydantic model
        # for name, param in sig.parameters.items():
            # print(param)
            # python_callable += get_model_source(param.annotation) + "\n"

        python_callable += get_model_source(sig.return_annotation) + "\n"

        python_callable += inspect.getsource(cable) + "\n"

        print(python_callable)
        result = pred(python_callable=python_callable, return_annotation_class_name=sig.return_annotation.__name__, prompt=prompt)[output_key]
        result_dict = eval_dict_str(result)
        result_model = sig.return_annotation.model_validate(result_dict)
        return result_model


class CallModel(BaseModel):
    callable: str
    prompt: str


def call(cable, prompt):
    call_mod = CallModule()
    return call_mod.forward(cable=cable, prompt=prompt)


def get_model_source(model: Type[BaseModel], already_seen: Set[Type[BaseModel]] = None) -> str:
    """
    Recursively grab the source code of a given Pydantic model and all related models.

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

    # Use model.__annotations__ to get the type of each field
    for field_name, field_type in model.__annotations__.items():
        # Check if the field is a subclass of BaseModel to identify Pydantic models
        if issubclass(field_type, BaseModel) and field_type not in already_seen:
            field_source = get_model_source(field_type, already_seen)
            source += "\n\n" + field_source

    return source


def main():
    init_dspy()

    # hello_world = call(ping_pong, "Lorem Ipsum")
    # print(hello_world)


if __name__ == "__main__":
    main()
