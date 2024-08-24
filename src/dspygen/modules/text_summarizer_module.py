"""

"""
import dspy
from dspy import Signature, InputField, OutputField


class TextSummarization(Signature):
    """
    Summarize a given text, capturing the main points concisely.
    """
    text = InputField(desc="The original text to be summarized.")
    summary = OutputField(desc="The summary of the original text, capturing the main points concisely.")


# Example usage within the existing TextSummarizerModule
class TextSummarizerModule(dspy.Module):
    """TextSummarizerModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, text):
        pred = dspy.Predict(TextSummarization)
        self.output = pred(text=text).summary
        return self.output


def text_summarizer_call(text):
    text_summarizer = TextSummarizerModule()
    return text_summarizer.forward(text=text)


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()
    text = "Hello World"
    result = text_summarizer_call(text=text)
    print(result)


if __name__ == "__main__":
    main()
