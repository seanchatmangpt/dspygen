"""
The source code imports the necessary libraries and modules, including dspy and Typer. It also defines a class called GenKeywordArgumentsModule, which contains a forward function that takes in a prompt and function and returns a keyword_arguments_dict. The gen_keyword_arguments_call function uses the GenKeywordArgumentsModule to generate keyword arguments for a given prompt and function. The app.command() decorator defines a command for the Typer app, which calls the gen_keyword_arguments_call function. The main function initializes dspy and calls the gen_keyword_arguments_call function with empty prompt and function parameters. The TODO comments indicate future plans for the code, including adding a streamlit component and a FastAPI route.
"""
import ast
import inspect
from typing import Any, Callable

import dspy
from typer import Typer

from dspygen.experiments.function_call import get_current_weather, get_n_day_weather_forecast
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


def eval_dict_str(dict_str: str) -> dict:
    """Safely convert str to dict"""
    return ast.literal_eval(dict_str)


def function_to_dict(func: Callable) -> dict:
    output = {
        "function__name__": func.__name__,
        "docstring": func.__doc__,
        "keyword_arguments": func.__annotations__,
    }

    if output["keyword_arguments"]["return"]:
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

        # Optional: Check for extraneous arguments
        for kwarg in kwargs:
            if kwarg not in params:
                dspy.Assert(False, f"Unexpected argument: {kwarg}")

        return True

    def forward(self, prompt: str, function: Callable) -> dict:
        pred = dspy.Predict("prompt, function -> keyword_arguments_dict_for_function")
        result = pred(prompt=prompt, function=str(function_to_dict(function))).keyword_arguments_dict_for_function

        # Validate the output
        try:
            kwargs = eval_dict_str(result)

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


def invoke(prompt: str, fn: Callable):
    kwargs = gen_keyword_arguments_call(prompt, fn)
    return fn(**kwargs)


@app.command()
def call(prompt, function):
    """GenKeywordArgumentsModule"""
    init_dspy()
    
    print(gen_keyword_arguments_call(prompt=prompt, function=function))


def main():
    init_dspy()

    prompt = "Today's weather in los angeles"

    keyword_arguments = gen_keyword_arguments_call(prompt=prompt, function=get_current_weather)

    get_current_weather(**keyword_arguments)

    prompt = "Years weather in paris, france"

    keyword_arguments = gen_keyword_arguments_call(prompt=prompt, function=get_n_day_weather_forecast)

    get_n_day_weather_forecast(**keyword_arguments)


if __name__ == "__main__":
    main()
