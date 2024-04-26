"""

"""
import inspect

import dspy
from typer import Typer

# from dspygen.modules.gen_pydantic_instance_module import GenPydanticInstance
from dspygen.rdddy.browser.browser_domain import TypeText
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class MessageModule(dspy.Module):
    """MessageModule"""

    def forward(self, prompt, pydantic_class):
        # pred = GenPydanticInstance(root_model=pydantic_class)
        return None  # pred(prompt)


def message_call(prompt, pydantic_class):
    message_module = MessageModule()
    return message_module.forward(prompt=prompt, pydantic_class=pydantic_class)


@app.command()
def call(prompt, pydantic_class):
    """MessageModule"""
    init_dspy()
    
    print(message_call(prompt=prompt, pydantic_class=pydantic_class))


from fastapi import APIRouter
router = APIRouter()

@router.post("/message/")
async def message_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return message_call(**data)


def main():
    init_dspy()
    prompt = "selector: #searchInput, text: How many storeys are in the castle that David Gregory inherited?"
    pydantic_class = TypeText
    instance = message_call(prompt=prompt, pydantic_class=pydantic_class)
    print(instance)
    

if __name__ == "__main__":
    main()
