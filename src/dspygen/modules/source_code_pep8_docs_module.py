"""The `SourceCodePep8DocsModule` class is used to create documentation for source code using best practices. It
first imports the necessary libraries and modules, including `dspy`, `pyperclip`, and `typer`. Then, in the `forward`
method, it checks if a context is provided and if not, sets a default context. The source code is then formatted and
passed through a `ChainOfThought` model to generate the pep8_docs. The `source_code_pep8_docs_call` function calls
the `forward` method and returns the result. In the `call` command, the source code is passed through `pyperclip` and
the result is printed and copied to the clipboard. The `main` function sets the `lm` variable to use the `OpenAI`
model and calls the `source_code_pep8_docs_call` function with an empty source code to test it."""
import dspy
import pyperclip
import typer
from typer import Typer

from dspygen.utils.dspy_tools import init_dspy

app = Typer()


class SourceCodePep8DocsModule(dspy.Module):
    """SourceCodePep8DocsModule"""

    def forward(self, source_code):
        pred = dspy.Predict("source_code -> simple_documentation")
        result = pred(source_code=source_code).simple_documentation
        return result


def source_code_docs_call(source_code):
    source_code_pep8_docs = SourceCodePep8DocsModule()
    return source_code_pep8_docs.forward(source_code=source_code)


@app.command()
def call(source_code):
    """SourceCodePep8DocsModule"""
    init_dspy(max_tokens=3000)

    result = source_code_docs_call(source_code=source_code)
    typer.echo(result)
    pyperclip.copy(result)


def main():
    init_dspy(max_tokens=3000)

    source_code = ""
    print(source_code_docs_call(source_code=source_code))


if __name__ == "__main__":
    main()
