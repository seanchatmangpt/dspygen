import dspy
from typer import Typer


app = Typer()


class TextSummaryModuleModule(dspy.Module):
    """A DSPy Module that takes in text and produces a summary."""

    def forward(self, text):
        pred = dspy.Predict("text -> summary")
        result = pred(text=text).summary
        return result


def text_summary_module_call(text):
    text_summary_module = TextSummaryModuleModule()
    return text_summary_module.forward(text=text)


def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    text = ""
    print(text_summary_module_call(text=text))


@app.command()
def module_test(text):
    """A DSPy Module that takes in text and produces a summary."""
    print(text_summary_module_call(text=text))


if __name__ == "__main__":
    app()
    # main()
