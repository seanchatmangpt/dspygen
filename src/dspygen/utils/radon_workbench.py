# Here is your PerfectPythonProductionCode® AGI response
from textwrap import dedent

# This Python module wraps around Radon's metrics functions to make them easier to use.
# We'll include functions for Cyclomatic Complexity, Raw Metrics, Halstead Metrics, and Maintainability Index.
# Note: You need to install radon library via pip for this to work.
from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze

from utils.complete import create
from utils.py_module import PyModule


def get_cyclomatic_complexity(source_code: str) -> dict:
    """Returns the Cyclomatic Complexity of the given source code."""
    return {func.actor_id: func.complexity for func in cc_visit(source_code)}


def get_raw_metrics(source_code: str) -> dict:
    """Returns raw metrics (LOC, LLOC, SLOC, Comments, Multi, Blank, etc.) of the given source code."""
    return analyze(source_code)._asdict()


def get_halstead_metrics(source_code: str) -> dict:
    """Returns the Halstead metrics (unique operators, unique operands, etc.) of the given source code."""
    return h_visit(source_code)


def get_maintainability_index(source_code: str) -> dict:
    """Returns the Maintainability Index of the given source code."""
    return mi_visit(source_code, False)


def check_for_bugs_with_metrics(source_code: str, metrics: dict) -> str:
    """Uses GPT-3.5-turbo to analyze the code and metrics for possible bugs."""
    # Create the prompt for GPT-3.5-turbo
    prompt = (
        "Review the following Python code and its metrics to identify any bugs.\n\n"
    )
    prompt += f"Code:\n```\n{source_code}\n```\n\n"
    prompt += "Metrics:\n"
    for metric_name, metric_value in metrics.items():
        prompt += f"- {metric_name}: {metric_value}\n"
    prompt += (
        "\nAre there any bugs in this code, True or False? "
        "If True, provide a description of the bug and how to fix it.\n\n"
    )

    # Make the API call
    response = create(prompt=prompt, max_tokens=2100, stop=["\n\n", "False"])

    return response


def fix_code(code: str, error: str = "", max_tokens=2000) -> str:
    """Use GPT-3.5-turbo to fix the code."""
    # Create the prompt for GPT-3.5-turbo
    prompt = (
        "Fix the following Python code and provide docstrings detailing fix. Do not add any functions "
        "or classes\nYou are only fixing what you are given:\n\n"
    )

    if error != "":
        prompt += f"Error:\n```\n{error}\n```\n\n"

    prompt += f"Code:\n```\n{code}\n```\n\n```python\n# Here is your PerfectPythonProductionCode® AGI fixed code\n"

    # Make the API call
    response = create(prompt=prompt, stop=["\n```"], max_tokens=max_tokens)

    # Get the response from GPT-3.5-turbo
    fixed_code = response

    return fixed_code


bad_add = dedent(
    """
    def add(a, b):
    asdljfaksdhfashkfdaskl;hfasdl;ihk
return a - b

    def sub(a, b):
    saddaosjfads;klfjsd
        return a - b12312390898327


    if __name__ == "__main__":
assert add(1, 2) == 3
        assert sub(1, 2) == -1
    """
)

bad_largest = dedent(
    """df quiq_Sorttttt(nums: List[int]) -> int:
    """
)


def get_code_metrics(sample_code):
    return {
        "Cyclomatic Complexity": get_cyclomatic_complexity(sample_code),
        "Raw Metrics": get_raw_metrics(sample_code),
        "Halstead Metrics": get_halstead_metrics(sample_code),
        "Maintainability Index": get_maintainability_index(sample_code),
    }


def refactor_code(sample_code):
    try:
        all_metrics = get_code_metrics(sample_code)
        print(all_metrics)
        result = check_for_bugs_with_metrics(sample_code, all_metrics)

        if result == "":
            return sample_code
        else:
            return fix_code(result)
    except SyntaxError:
        return fix_code(sample_code)


if __name__ == "__main__":
    # result = "GPT-3.5-turbo Analysis: There appears to be a bug in the add function, where it is returning the wrong value (a - b instead of a + b). To fix this, we can simply change the return statement to return a + b."
    result = refactor_code(bad_largest)
    # result = refactor_code(bad_add)
    print("GPT-3.5-turbo Analysis:", result)

    module = PyModule(source=result, filepath="demo_module.py")

    # print("Module:", module)
    # print("Functions:", module.functions)

    # add_fixed = dedent("""def add(a, b):
    # return a + b""")
    add_fixed = fix_code(result)

    module.add = add_fixed

    print(str(module))

    module.filepath = "demo_module.py"
    module.save()
