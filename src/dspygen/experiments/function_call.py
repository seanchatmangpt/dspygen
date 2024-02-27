import dspy

from dspygen.utils.dspy_tools import init_dspy


def get_current_weather(location: str, temperature_unit: str) -> str:
    """
    Get the current weather for a given location in the specified format.

    :param location: The city and state, e.g., "San Francisco, CA".
    :param temperature_unit: The temperature unit to use, either "celsius" or "fahrenheit".
    :return: A string describing the current weather.
    """
    print("Retrieving weather for", location)
    # TODO: API Call
    return f"{location}, {temperature_unit}"


def get_n_day_weather_forecast(
    location: str, temperature_unit: str, num_days: int
) -> str:
    """
    Get an N-day weather forecast for a given location in the specified format.

    :param location: The city and state, e.g., "San Francisco, CA".
    :param temperature_unit: The temperature unit to use, either "celsius" or "fahrenheit".
    :param num_days: The number of days to forecast.
    :return: A string describing the weather forecast.
    """
    print("Retrieving N-day weather forecast for", location)
    return f"{location}, {temperature_unit}, {num_days}"


def function_to_dict(func: "function") -> dict:
    output = {
        "function": func.__name__,
        "docstring": func.__doc__,
        "annotations": func.__annotations__,
    }
    return output


func_list = [get_current_weather, get_n_day_weather_forecast]


def lm_function_call(prompt, functions_list: list["function"]) -> str:
    funcs_str = ",".join([str(function_to_dict(func)) for func in functions_list])

    pred = dspy.Predict("prompt, functions_as_string -> chosen_function")
    choice = pred.forward(prompt=prompt, functions_as_string=funcs_str).chosen_function

    return choice


init_dspy()


assert (
    lm_function_call("Today's weather in los angeles", func_list)
    == "get_current_weather"
)

assert (
    lm_function_call("Months weather in los angeles", func_list)
    == "get_n_day_weather_forecast"
)


print()
