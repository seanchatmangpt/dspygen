import ast

from dspy import Assert

from dspygen.experiments.gen_module import GenModule
from dspygen.utils.dspy_tools import init_dspy


def is_primitive_type(data_type):
    primitive_types = {int, float, str, bool, list, tuple, dict, set}

    return data_type in primitive_types


class GenPythonPrimitive(GenModule):
    def __init__(self, primitive_type, lm=None):
        if not is_primitive_type(primitive_type):
            raise ValueError(
                f"primitive type {primitive_type.__name__} must be a Python primitive type"
            )
        super().__init__(f"{primitive_type.__name__}_str_for_ast_literal_eval", lm)
        self.primitive_type = primitive_type

    def validate_primitive(self, output) -> bool:
        try:
            return isinstance(ast.literal_eval(output), self.primitive_type)
        except SyntaxError:
            return False

    def validate_output(self, output):
        Assert(
            self.validate_primitive(output),
            f"You need to create a valid python {self.primitive_type.__name__} "
            f"primitive type for \n{self.output_key}\n"
            f"You will be penalized for not returning only a {self.primitive_type.__name__} for "
            f"{self.output_key}",
        )
        data = ast.literal_eval(output)

        if self.primitive_type is set:
            data = set(data)
        return data

    def __call__(self, prompt):
        return self.forward(prompt=prompt)


class GenDict(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=dict)


class GenList(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=list)


def gen_list(prompt):
    return GenList()(prompt)

class GenBool(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=bool)


def gen_bool(prompt):
    return GenBool()(prompt)


class GenInt(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=int)


class GenFloat(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=float)


class GenTuple(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=tuple)


class GenSet(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=set)


class GenStr(GenPythonPrimitive):
    def __init__(self):
        super().__init__(primitive_type=str)


def main():
    init_dspy()

    result = GenTuple()(
        "Create a list of planets in our solar system sorted by largest to smallest"
    )

    assert result == (
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Earth",
        "Venus",
        "Mars",
        "Mercury",
    )

    print(f"The planets of the solar system are {result}")


if __name__ == "__main__":
    main()
