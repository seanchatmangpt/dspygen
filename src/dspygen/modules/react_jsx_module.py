import dspy
from typer import Typer


app = Typer(help="Create React JSX source code.")


class PromptReactJsxModule(dspy.Module):

    """This is a DSPy Module that converts a prompt into react_jsx"""

    def forward(self, prompt):
        pred = dspy.Predict("prompt -> react_jsx")
        result = pred(prompt=prompt).react_jsx
        return result


def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    prompt = "Hello World Functional Component"

    prompt_react_jsx = PromptReactJsxModule()
    print(prompt_react_jsx.forward(prompt=prompt))


@app.command()
def module_test(prompt):
    """This is a DSPy Module that converts a prompt into react_jsx"""
    prompt_react_jsx = PromptReactJsxModule()

    print(prompt_react_jsx.forward(prompt=prompt))


if __name__ == "__main__":
    # app()
    main()
