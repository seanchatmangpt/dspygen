"""GenDspyModule — generate DSPy module source code from a specification."""

import dspy
from dspygen.utils.dspy_tools import init_dspy


class GenDspyModule(dspy.Module):
    """Generate a complete DSPy module class from a natural language specification.

    Takes a description of what the module should do and returns ready-to-use
    DSPy source code including the class definition, forward method, and CLI
    scaffolding.
    """

    def __init__(self, **forward_args):
        """Initialise GenDspyModule."""
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, specification):
        """Generate DSPy module source code.

        Args:
            specification: Natural language description of the module to generate.

        Returns:
            Python source code string for the requested module.
        """
        pred = dspy.Predict("specification -> dspy_module_source")
        self.output = pred(specification=specification).dspy_module_source
        return self.output

    def pipe(self, input_str):
        """Pipe support for DSL chaining."""
        return self.forward(specification=input_str)


def gen_dspy_module_call(specification):
    """Convenience wrapper around GenDspyModule."""
    module = GenDspyModule()
    return module.forward(specification=specification)


def main():
    """CLI entry point."""
    init_dspy()
    specification = "A module that translates English text to French."
    result = gen_dspy_module_call(specification=specification)
    print(result)


if __name__ == "__main__":
    main()
