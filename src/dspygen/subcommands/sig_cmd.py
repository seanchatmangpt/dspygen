"""Generate dspy.Signatures"""
import typer

from dspygen.modules.file_name_module import file_name_call
from dspygen.modules.gen_signature_module import gen_signature_call
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.file_tools import signatures_dir

app = typer.Typer(help="Generate dspy.Signatures")


@app.command(name="new")
def sig(prompt: str):
    """Generate a new dspy.Module. Example: dspygen sig new 'text -> summary'"""
    init_dspy()

    source = gen_signature_call(prompt)

    file_name = file_name_call(source + "\nName the file by the class name.", "py")

    with open(signatures_dir() / file_name, "w") as file:
        file.write(source)

    print(source)

    print(f"Module saved to {signatures_dir() / file_name}")
