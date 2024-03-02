"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class TestModule(dspy.Module):
    """TestModule"""

    def forward(self, a1, s2, v3):
        pred = dspy.Predict("a1, s2, v3 -> test")
        result = pred(a1=a1, s2=s2, v3=v3).test
        return result


def test_call(a1, s2, v3):
    test = TestModule()
    return test.forward(a1=a1, s2=s2, v3=v3)


@app.command()
def call(a1, s2, v3):
    """TestModule"""
    init_dspy()
    
    print(test_call(a1=a1, s2=s2, v3=v3))


from fastapi import APIRouter
router = APIRouter()

@router.post("/test/")
async def test_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return test_call(**data)


def main():
    init_dspy()
    a1 = ""
    s2 = ""
    v3 = ""
    print(test_call(a1=a1, s2=s2, v3=v3))
    

if __name__ == "__main__":
    main()
