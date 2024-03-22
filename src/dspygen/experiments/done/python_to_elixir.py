from dspygen.modules.file_name_module import file_name_call
from dspygen.modules.gen_keyword_arguments_module import invoke
from dspygen.modules.to_elixir_module import to_elixir_call
from dspygen.utils.dspy_tools import init_dspy


def python_to_elixir(python_code):
    return to_elixir_call(python_code)
    # Write to disk

TO_CONVERT = '''
def get_current_weather(location: str, temperature_unit: str) -> str:
    """
    Get the current weather for a given location in the specified format.

    :param location: The city and state, e.g., "San Francisco, CA".
    :param temperature_unit: The temperature unit to use, either "celsius" or "fahrenheit".
    :return: A string describing the current weather.
    """
    print(f"Retrieving weather for {location}, temperature unit: {temperature_unit}")
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
    print(f"Retrieving {num_days} day weather forecast for {location} in {temperature_unit}")
    return f"{location}, {temperature_unit}, {num_days}"
'''



def main():
    init_dspy(max_tokens=3000)

    elixir = to_elixir_call(TO_CONVERT)
    file_name = file_name_call(elixir)

    with(open(file_name, "w")) as f:
        f.write(elixir)

    print(f"Wrote {file_name}")


if __name__ == '__main__':
    main()
