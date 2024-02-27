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


