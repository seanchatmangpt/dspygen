"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class ProposalGeneratorModule(dspy.Module):
    """ProposalGeneratorModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, context, criteria):
        pred = dspy.Predict("context, criteria -> proposal")
        self.output = pred(context=context, criteria=criteria).proposal
        return self.output

    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer

app = Typer()


@app.command()
def call(context, criteria):
    """ProposalGeneratorModule"""
    init_dspy()

    print(proposal_generator_call(context=context, criteria=criteria))


def proposal_generator_call(context, criteria):
    proposal_generator = ProposalGeneratorModule()
    return proposal_generator.forward(context=context, criteria=criteria)


def main():
    init_dspy()
    context = ""
    criteria = ""
    result = proposal_generator_call(context=context, criteria=criteria)
    print(result)


from fastapi import APIRouter

router = APIRouter()


@router.post("/proposal_generator/")
async def proposal_generator_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return proposal_generator_call(**data)

if __name__ == "__main__":
    main()
