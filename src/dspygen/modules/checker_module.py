"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class CheckerModule(dspy.Module):
    """CheckerModule"""

    def forward(self, prompt, assertion):
        pred = dspy.ChainOfThought("prompt, assertion -> return_bool")
        result = pred(prompt=prompt, assertion=assertion).return_bool
        return result


def checker_call(prompt, assertion):
    checker = CheckerModule()
    return checker.forward(prompt=prompt, assertion=assertion)


@app.command()
def call(prompt, assertion):
    """CheckerModule"""
    init_dspy()
    
    print(checker_call(prompt=prompt, assertion=assertion))


from fastapi import APIRouter
router = APIRouter()

@router.post("/checker/")
async def checker_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return checker_call(**data)


def main():
    init_dspy()
    prompt = ""
    assertion = ""
    print(checker_call(prompt=prompt, assertion=assertion))
    

if __name__ == "__main__":
    main()
