"""
The source code imports the necessary libraries and modules, including dspy and Typer. It also defines a class called GenKeywordArgumentsModule, which contains a forward function that takes in a prompt and function and returns a keyword_arguments_dict. The gen_keyword_arguments_call function uses the GenKeywordArgumentsModule to generate keyword arguments for a given prompt and function. The app.command() decorator defines a command for the Typer app, which calls the gen_keyword_arguments_call function. The main function initializes dspy and calls the gen_keyword_arguments_call function with empty prompt and function parameters. The TODO comments indicate future plans for the code, including adding a streamlit component and a FastAPI route.
"""
import ast
import inspect
from typing import Any, Callable

import dspy
from typer import Typer

from dspygen.experiments.function_calling.function_call import get_current_weather, get_n_day_weather_forecast
from dspygen.utils.dspy_tools import init_dspy


class GenerateKeywordArgumentsSignature(dspy.Signature):
    """
    A Signature class designed to generate keyword arguments for a function call
    based on a given prompt and the function's signature.
    """
    prompt = dspy.InputField(desc="Description or context to generate the keyword arguments.")
    function_signature = dspy.InputField(desc="A dictionary representing the function's signature, including name, docstring, and keyword arguments.")

    keyword_arguments_dict_for_function = dspy.OutputField(desc="A dictionary containing the generated keyword arguments for the specified function.",
                                                           prefix="kwargs_for_function_from_prompt: dict = ")



app = Typer()


def eval_dict_str(dict_str: str) -> dict:
    """Safely convert str to dict"""
    return ast.literal_eval(dict_str)


def function_to_dict(func: Callable) -> dict:
    output = {
        "function__name__": func.__name__,
        "docstring": func.__doc__,
        "keyword_arguments": {},
    }

    sig = inspect.signature(func)
    params = sig.parameters

    for name, param in params.items():
        # Check if the parameter has a type annotation; if not, default to str
        param_type = param.annotation if param.annotation is not inspect.Parameter.empty else str
        output["keyword_arguments"][name] = param_type.__name__  # Store the name of the type

    # Remove the return type annotation if present
    if "return" in output["keyword_arguments"]:
        del output["keyword_arguments"]["return"]

    return output


class GenKeywordArgumentsModule(dspy.Module):
    """GenKeywordArgumentsModule"""

    def validate_output(self, kwargs: dict[str, Any], function: Callable) -> bool:
        """Validates generated keyword arguments against the target function's signature."""
        sig = inspect.signature(function)
        params = sig.parameters

        for name, param in params.items():
            # Check for missing required arguments
            if param.default == inspect.Parameter.empty and name not in kwargs:
                dspy.Assert(False, f"Missing required argument: {name} from {kwargs}")

            # Optional: Type check based on annotations
            if param.annotation != inspect.Parameter.empty and name in kwargs:
                expected_type = param.annotation
                if not isinstance(kwargs[name], expected_type):
                    dspy.Assert(False, f"Argument '{name}' expected type {expected_type}, got {type(kwargs[name])}")

        return True

    def forward(self, prompt: str, function: Callable) -> dict:
        pred = dspy.ChainOfThought(GenerateKeywordArgumentsSignature)
        result = pred(prompt=prompt, function_signature=str(function_to_dict(function))).keyword_arguments_dict_for_function

        # Validate the output
        try:
            kwargs = eval_dict_str(result)
            if "return" in kwargs.keys():
                del kwargs["return"]

            if self.validate_output(kwargs, function):
                return kwargs
        except (AssertionError, SyntaxError) as e:
            # Handle the failure by attempting recovery or fallback logic
            pred = dspy.ChainOfThought("prompt, function, error -> keyword_arguments_dict_for_function")
            result = pred(prompt=prompt, function=str(function_to_dict(function)), error=str(e)).keyword_arguments_dict_for_function
            kwargs = eval_dict_str(result)

            if self.validate_output(kwargs, function):
                return kwargs
            else:
                raise ValueError(f"Generated keyword arguments {kwargs} do not match the function's requirements "
                                 f"{str(function_to_dict(function))}")


def gen_keyword_arguments_call(prompt: str, function: Callable) -> dict:
    gen_keyword_arguments = GenKeywordArgumentsModule()
    return gen_keyword_arguments.forward(prompt=prompt, function=function)


def invoke(fn: Callable, prompt: str):
    kwargs = gen_keyword_arguments_call(prompt, fn)
    return fn(**kwargs)


def main():
    init_dspy()

    prompt = "Today's weather in los angeles"

    invoke(get_current_weather, prompt)

    prompt = "Years weather in paris, france"

    invoke(get_n_day_weather_forecast, prompt)


if __name__ == "__main__":
    main()
