"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class GenMessageModule(dspy.Module):
    """GenMessageModule"""

    def forward(self, prompt, message):
        pred = dspy.Predict("prompt, message -> pydantic_model_validate_str")
        result = pred(prompt=prompt, message=message).pydantic_model_validate_str
        return result


from typer import Typer
app = Typer()


@app.command()
def call(prompt, message):
    """GenMessageModule"""
    init_dspy()

    print(gen_message_call(prompt=prompt, message=message))



def gen_message_call(prompt, message):
    gen_message = GenMessageModule()
    return gen_message.forward(prompt=prompt, message=message)



def main():
    init_dspy()
    prompt = ""
    message = ""
    print(gen_message_call(prompt=prompt, message=message))



from fastapi import APIRouter
router = APIRouter()

@router.post("/gen_message/")
async def gen_message_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return gen_message_call(**data)



if __name__ == "__main__":
    main()
