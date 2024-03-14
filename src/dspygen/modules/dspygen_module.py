import dspy


class DGModule(dspy.Module):
    """DGModule that supports pipe operator with string processing convention."""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other: "DGModule"):
        print(
            f"Operation between {self.__class__.__name__} and {other.__class__.__name__}"
        )

        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, **kwargs):
        """Processes a string input. Override in subclasses for specific behavior."""
        raise NotImplementedError(
            "Please implement the forward method in your subclass."
        )

    def pipe(self, dg_module):
        """Pipes the output of one module to the input of another. Override in subclasses for specific behavior."""
        raise NotImplementedError("Please implement the pipe method in your subclass.")


class TweetDGModule(DGModule):
    """TweetModule"""

    def __init__(self, style, **forward_args):
        self.style = style
        forward_args.update({"style": style})
        super().__init__(**forward_args)

    def forward(self, insight):
        pred = dspy.ChainOfThought("insight, style -> tweet_with_length_of_100_chars")
        self.output = pred(
            insight=insight, style=self.style
        ).tweet_with_length_of_100_chars
        print(f"{self.__class__.__name__} output: {self.output}")
        return self.output

    def pipe(self, input_str):
        return self.forward(insight=input_str)


class BusinessDevConsultantDGModule(DGModule):
    """BusinessDevConsultantModule"""

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt -> advice")
        self.output = pred(prompt=prompt).advice
        print(f"{self.__class__.__name__} output: {self.output}")
        return self.output

    def pipe(self, input_str):
        return self.forward(prompt=input_str)


class TextSummaryDGModule(DGModule):
    """A DSPy Module that takes in text and produces a summary."""

    def forward(self, text):
        pred = dspy.Predict("text -> summary")
        self.output = pred(text=text).summary
        print(f"{self.__class__.__name__} output: {self.output}")
        return self.output

    def pipe(self, input_str):
        return self.forward(text=input_str)


class ReactJsxDGModule(DGModule):
    """This is a DSPy Module that converts a prompt into react_jsx"""
    def __init__(self, reqs="", **forward_args):
        self.reqs = reqs
        forward_args.update({"reqs": reqs})
        super().__init__(**forward_args)

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt, reqs -> react_jsx")
        self.output = pred(prompt=prompt, reqs=self.reqs).react_jsx
        print(f"{self.__class__.__name__} output: {self.output}")
        return self.output

    def pipe(self, input_str):
        return self.forward(prompt=input_str)


def main():
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()

    result_module = (
        BusinessDevConsultantDGModule(prompt="3 Paragraph example speech on the future of a company")
        | TextSummaryDGModule()
        | TweetDGModule(style="business with a hint of humor and 5 hashtags")
        | ReactJsxDGModule(reqs="React, TypeScript, Material-UI, Axios")
    )
    print(result_module.output)


if __name__ == "__main__":
    main()
