"""
This code imports the necessary libraries and modules to run the DFLSSModule. It also defines a function to call the DFLSSModule and a route for a streamlit component. The main function initializes the DFLSSModule and prints the result.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class DFLSSModule(dspy.Module):
    """DFLSSModule"""

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt -> design_for_lean_six_sigma")
        result = pred(prompt=prompt).design_for_lean_six_sigma
        return result


def dflss_call(prompt):
    dflss = DFLSSModule()
    return dflss.forward(prompt=prompt)


@app.command()
def call(prompt):
    """DFLSSModule"""
    init_dspy()
    
    print(dflss_call(prompt=prompt))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/dflss/")
async def dflss_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return dflss_call(**data)


def main():
    init_dspy()
    prompt = ""
    print(dflss_call(prompt=prompt))
    

if __name__ == "__main__":
    main()
