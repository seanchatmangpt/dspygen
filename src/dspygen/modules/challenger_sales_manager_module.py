"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy

import dspy


class ChallengerSalesManager(dspy.Signature):
    """
    The Challenger Sales method is a powerful approach to sales that emphasizes teaching, tailoring, and taking control
    of the sales conversation. It involves understanding the client's business deeply, challenging their thinking,
    and guiding them towards a solution that they may not have considered initially.
    """

    prompt = dspy.InputField(
        desc=(
            "The input prompt describing the sales task. This prompt should provide sufficient context and detail "
            "about the current stage of the sales process, any specific challenges faced, and any relevant information "
            "about the client or market conditions. For instance, a prompt could describe the need to start market research, "
            "conduct outreach to potential leads, engage in the discovery process to understand client needs, tailor solutions "
            "based on discovered needs, handle client objections and concerns, close the deal, or finalize post-sale processes "
            "to ensure client satisfaction."
        )
    )

    response = dspy.OutputField(
        desc=(
            "The output response that contains advice or action based on the input prompt. The response will provide "
            "strategic guidance, actionable steps, or insightful recommendations tailored to the specific stage of the sales process "
            "described in the prompt. For example, it might suggest effective strategies for market research, best practices for "
            "client outreach, key questions to ask during discovery, techniques for tailoring solutions to client needs, methods for "
            "addressing common objections, tips for closing the deal successfully, or steps to complete the sale and ensure ongoing "
            "client satisfaction. 3 sentences maximum."
        )
    )


class ChallengerSalesManagerModule(dspy.Module):
    """ChallengerSalesManagerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, prompt):
        pred = dspy.Predict(ChallengerSalesManager)
        self.output = pred(prompt=prompt).response
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(prompt):
    """ChallengerSalesManagerModule"""
    init_dspy()

    print(challenger_sales_manager_call(prompt=prompt))



def challenger_sales_manager_call(prompt):
    challenger_sales_manager = ChallengerSalesManagerModule()
    return challenger_sales_manager.forward(prompt=prompt)


def main():
    init_dspy()
    prompt = ""
    result = challenger_sales_manager_call(prompt=prompt)
    print(result)


if __name__ == "__main__":
    main()
