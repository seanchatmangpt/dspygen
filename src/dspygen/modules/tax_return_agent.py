"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class TaxReturnAgentModule(dspy.Module):
    """TaxReturnAgentModule"""

    def forward(self, income):
        pred = dspy.ChainOfThought("income -> tax_return_advice")
        result = pred(income=income).tax_return_advice
        return result


def tax_return_agent_call(income):
    tax_return_agent = TaxReturnAgentModule()
    return tax_return_agent.forward(income=income)


@app.command()
def call(income):
    """TaxReturnAgentModule"""
    init_dspy()
    
    print(tax_return_agent_call(income=income))


from fastapi import APIRouter
router = APIRouter()

@router.post("/tax_return_agent/")
async def tax_return_agent_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return tax_return_agent_call(**data)


def main():
    init_dspy()
    income = "$150,000 chennai india to USA"
    print(tax_return_agent_call(income=income))
    

if __name__ == "__main__":
    main()
