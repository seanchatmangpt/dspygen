"""
The source code is used to import the necessary libraries and modules for the program. It also defines a class called "InsightTweetModule" which contains a function called "forward" that takes in an "insight" parameter and returns a result. The "insight_tweet_call" function uses the "InsightTweetModule" class to call the "forward" function and return the result. The "call" function is used to initialize the program and print the result of the "insight_tweet_call" function. The "main" function is used to initialize the program and print the result of the "insight_tweet_call" function.
"""
import dspy
import pyperclip
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


class InsightTweetModule(dspy.Module):
    """InsightTweetModule"""

    def forward(self, insight):
        pred = dspy.Predict("insight -> tweet")
        result = pred(insight=insight).tweet
        return result


def insight_tweet_call(insight):
    insight_tweet = InsightTweetModule()
    return insight_tweet.forward(insight=insight)


@app.command()
def call(insight):
    """InsightTweetModule"""
    init_dspy()

    print(insight_tweet_call(insight=insight))


def main():
    init_dspy()
    insight = pyperclip.paste()
    print(insight_tweet_call(insight=insight))


if __name__ == "__main__":
    main()
