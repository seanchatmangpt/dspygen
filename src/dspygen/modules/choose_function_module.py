"""Defines a class called ChooseFunctionModule, which has a forward method that takes
in a prompt and a list of functions and uses dspy's Predict function to return the name of the chosen function. The
choose_function_call function uses the ChooseFunctionModule to call the forward method and return the chosen function
name. The app.command() decorator is used to create a command line interface for the choose_function_call function.
The main function initializes dspy and then calls the choose_function_call function with empty prompt and
function_list parameters. The TODO comments indicate future plans for the code, including adding a streamlit
component and a FastAPI route."""
from typing import Callable

import dspy
from typer import Typer

from dspygen.experiments.function_calling.function_call import get_current_weather, get_n_day_weather_forecast
from dspygen.utils.dspy_tools import init_dspy

app = Typer()


def function_to_dict(func: Callable) -> dict:
    output = {
        "function__name__": func.__name__,
        "docstring": func.__doc__,
        "annotations": func.__annotations__
    }
    return output


def functions_to_dict(funcs: list[Callable]) -> dict:
    return {
        func.__name__: function_to_dict(func) for func in funcs
    }


class ChooseFunctionModule(dspy.Module):
    """ChooseFunctionModule"""
    def __init__(self, functions_list: list[Callable] = None) -> None:
        super().__init__()
        self._functions_list = functions_list

    @property
    def functions_list(self):
        return self._functions_list

    @property
    def functions_dict(self):
        if self._functions_list:
            return functions_to_dict(self._functions_list)
        return None

    def validate_output(self, chosen_function_name: str) -> bool:
        """
        Utilizes dspy.Assert to validate if the chosen function name exists within the functions dictionary.
        """
        # Using dspy.Assert to validate the chosen function name
        valid_choice = chosen_function_name in self.functions_dict if self.functions_dict else False
        dspy.Assert(valid_choice, f"Invalid function name chosen: {chosen_function_name}. "
                                  f"A name must be chosen within the functions dictionary. "
                                  f"Just return the function.__name__ for the key")
        return valid_choice

    def forward(self, prompt, function_list: list[Callable] = None) -> Callable:
        if function_list:
            self._functions_list = function_list

        pred = dspy.Predict("prompt, function_list -> matching_function__name__")
        matching_function__name__ = pred(prompt=prompt, function_list=str(self.functions_dict)).matching_function__name__

        try:
            if self.validate_output(matching_function__name__):
                return next(filter(lambda f: f.__name__ == matching_function__name__, self._functions_list))
        except AssertionError as e:
            # Handle the failure by attempting recovery or fallback logic
            pred = dspy.ChainOfThought("prompt, function_list, error -> matching_function__name__")
            matching_function__name__ = pred(prompt=prompt, function_list=function_list, error=str(e)).matching_function__name__

            if self.validate_output(matching_function__name__):
                return next(filter(lambda f: f.__name__ == matching_function__name__, self._functions_list))
            else:
                raise ValueError(f"Invalid function name chosen: {matching_function__name__}")


def choose_function_call(prompt, function_list):
    choose_function = ChooseFunctionModule()
    return choose_function.forward(prompt=prompt, function_list=function_list)


@app.command()
def call(prompt, function_list):
    """ChooseFunctionModule"""
    init_dspy()

    print(choose_function_call(prompt=prompt, function_list=function_list))


def main():
    init_dspy()

    prompt = "Today's weather in los angeles"
    function_list = [get_current_weather, get_n_day_weather_forecast]

    fn = choose_function_call(prompt=prompt, function_list=function_list)

    assert fn == get_current_weather

    prompt = "Years weather in paris, france"

    fn = choose_function_call(prompt=prompt, function_list=function_list)

    assert fn == get_n_day_weather_forecast


if __name__ == "__main__":
    main()
