from dspygen.experiments.function_calling.function_call import get_current_weather, get_n_day_weather_forecast
from dspygen.modules.choose_function_module import choose_function_call
from dspygen.modules.gen_keyword_arguments_module import gen_keyword_arguments_call
from dspygen.utils.dspy_tools import init_dspy


def chose_and_invoke(prompt, function_list):
    fn = choose_function_call(prompt=prompt, function_list=function_list)
    kwargs = gen_keyword_arguments_call(prompt, fn)
    return fn(**kwargs)

def main():
    init_dspy()

    function_list = [get_current_weather, get_n_day_weather_forecast]

    result = chose_and_invoke("Today's weather in los angeles", function_list)

    assert result == "Los Angeles, CA, fahrenheit"

    result = chose_and_invoke("Years weather in paris, france", function_list)

    assert result == 'Paris, France, celsius, 365'


if __name__ == '__main__':
    main()
