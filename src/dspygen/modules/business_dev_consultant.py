"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class BusinessDevConsultantModule(dspy.Module):
    """BusinessDevConsultantModule"""

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt -> advice")
        result = pred(prompt=prompt).advice
        return result


def business_dev_consultant_call(prompt):
    business_dev_consultant = BusinessDevConsultantModule()
    return business_dev_consultant.forward(prompt=prompt)


@app.command()
def call(prompt):
    """BusinessDevConsultantModule"""
    init_dspy()
    
    print(business_dev_consultant_call(prompt=prompt))


from fastapi import APIRouter
router = APIRouter()

@router.post("/business_dev_consultant/")
async def business_dev_consultant_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return business_dev_consultant_call(**data)


def main():
    init_dspy()
    prompt = "Merger of financial institution"
    print(business_dev_consultant_call(prompt=prompt))
    

if __name__ == "__main__":
    main()
