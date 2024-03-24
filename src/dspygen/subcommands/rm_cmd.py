"""lm"""
import typer

from dspygen.typetemp.functional import render
from dspygen.utils.file_tools import rm_dir

app = typer.Typer(help="Generate Retrieval Models")


rm_template = """import dspy


class {{ name }}Retriever(dspy.Retrieve):
    def __init__(self, **kwargs):
        super().__init__()
    
    def forward(self, **kwargs):
        return None


def main():
    rm = {{ name }}Retriever()
    print(rm.forward())
    
    
if __name__ == '__main__':
    main()
      
"""


@app.command(name="new")
def new_rm(name: str = typer.Argument(...)):
    """Generates a new retrieval model."""
    to = f"{rm_dir()}/"
    source = render(rm_template, name=name, to=to + "{{ name | underscore }}_retriever.py")
    print(source)


def main():
    print('main')


if __name__ == '__main__':
    main()
