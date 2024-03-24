"""lm"""
import typer

from dspygen.typetemp.functional import render
from dspygen.utils.file_tools import lm_dir

app = typer.Typer(help="Generate Language Models")


lm_template = """from dsp import LM


class {{ name }}(LM):
    def __init__(self):
        super().__init__(model)
        
        self.provider = "default"

        self.history = []

    def basic_request(self, prompt, **kwargs):
        pass

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        pass
        
"""


@app.command(name="new")
def new_lm(name: str = typer.Argument(...)):
    """Generates a new language model."""
    to = f"{lm_dir()}/"
    source = render(lm_template, name=name, to=to + "{{ name | underscore }}_lm.py")
    print(source)


def main():
    print('main')
    name = "Groq"
    to = f"{lm_dir()}/"
    source = render(lm_template, name=name, to=to + "{{ name | underscore }}_lm.py")
    print(source)


if __name__ == '__main__':
    main()
