"""Composable DSPyGen module base classes and examples."""
from __future__ import annotations

from abc import ABC, abstractmethod

import dspy

from dspygen.modules.pipeline import pipe_forward, pipe_modules


class DGModule(dspy.Module, ABC):
    """DSPy module with deterministic ``|`` composition."""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other: "DGModule"):
        return pipe_modules(self, other)

    @abstractmethod
    def forward(self, **kwargs):
        """Execute the module's pure model-program boundary."""

    def pipe(self, input_value):
        return pipe_forward(self, input_value)


class TweetDGModule(DGModule):
    """Turn an insight into a short styled tweet."""

    def __init__(self, style, **forward_args):
        self.style = style
        forward_args.update({"style": style})
        super().__init__(**forward_args)

    def forward(self, insight, style=None):
        style = style or self.style
        pred = dspy.ChainOfThought("insight, style -> tweet_with_length_of_100_chars")
        self.output = pred(insight=insight, style=style).tweet_with_length_of_100_chars
        return self.output


class BusinessDevConsultantDGModule(DGModule):
    """Generate business-development advice."""

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt -> advice")
        self.output = pred(prompt=prompt).advice
        return self.output


class TextSummaryDGModule(DGModule):
    """Summarize text."""

    def forward(self, text):
        pred = dspy.Predict("text -> summary")
        self.output = pred(text=text).summary
        return self.output


class ReactJsxDGModule(DGModule):
    """Convert a prompt and requirements into React JSX."""

    def __init__(self, reqs="", **forward_args):
        self.reqs = reqs
        forward_args.update({"reqs": reqs})
        super().__init__(**forward_args)

    def forward(self, prompt, reqs=None):
        reqs = self.reqs if reqs is None else reqs
        pred = dspy.ChainOfThought("prompt, reqs -> react_jsx")
        self.output = pred(prompt=prompt, reqs=reqs).react_jsx
        return self.output


def main():
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()
    result_module = (
        BusinessDevConsultantDGModule(
            prompt="3 Paragraph example speech on the future of a company"
        )
        | TextSummaryDGModule()
        | TweetDGModule(style="business with a hint of humor and 5 hashtags")
        | ReactJsxDGModule(reqs="React, TypeScript, Material-UI, Axios")
    )
    print(result_module.output)


if __name__ == "__main__":
    main()
