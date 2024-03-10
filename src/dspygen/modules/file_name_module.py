import dspy
import pyperclip
from typer import Typer
from inflection import underscore

app = Typer(
    help="Generate a file name from any text."
)


class FileContentToFileNameModule(dspy.Module):
    """Converts file content to a file name with extension"""

    def __init__(self, extension: str = None):
        super().__init__()
        self.extension = extension

    def forward(self, file_content):
        pred = dspy.ChainOfThought("file_content -> valid_file_name_with_extension")

        result = pred(file_content=file_content).valid_file_name_with_extension

        if self.extension == "py":
            result = underscore(result)

        return result


def file_name_call(file_content, extension: str = None):
    file_content_to_file_name = FileContentToFileNameModule(extension=extension)
    return file_content_to_file_name.forward(file_content=file_content)


def main():
    file_content = (
        pyperclip.paste()
    )  # Initialize your inputs here. Adjust as necessary.

    print(file_name_call(file_content=file_content))


@app.command()
def call(file_content: str):
    """Converts file content to a file name with extension"""
    print(file_name_call(file_content=file_content))


if __name__ == "__main__":
    # app()
    main()
