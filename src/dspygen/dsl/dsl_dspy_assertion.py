import dspy
from pydantic import BaseModel

from dspygen.typetemp.functional import render


class AssertionModel(BaseModel):
    label: str
    constraint: str
    message: str
    args: dict


class AssertionExecutor:
    def __init__(self, assertion_model: AssertionModel):
        self.assertion_model = assertion_model

    def execute_assertion(self, result):
        self.assertion_model.args["result"] = result
        constraint = render(self.assertion_model.constraint, **self.assertion_model.args)
        message = render(self.assertion_model.message, **self.assertion_model.args)

        dspy.Assert(eval(constraint), message)


# Example usage
assertion_data = {
    "label": "AssertLen",
    "constraint": "{{ result | length }} >= {{ min_length }}",
    "message": "The length of the {{ result }} should be {{ min_length }} minimum but was {{ result | length }}",
    "args": {"min_length": 10}
}


def main():
    assertion_model = AssertionModel(**assertion_data)
    executor = AssertionExecutor(assertion_model)

    # Assuming result is some data you want to test
    result = "Hello, world!"

    try:
        executor.execute_assertion(result)
    except AssertionError as e:
        print(e)


if __name__ == '__main__':
    main()
