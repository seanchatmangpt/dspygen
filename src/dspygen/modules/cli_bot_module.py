"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class CLIBotModule(dspy.Module):
    """CLIBotModule"""

    def forward(self, prompt):
        pred = dspy.ChainOfThought("prompt -> bash_command_line_input")
        result = pred(prompt=prompt).bash_command_line_input
        return result


def cli_bot_call(prompt):
    cli_bot = CLIBotModule()
    return cli_bot.forward(prompt=prompt)


@app.command()
def call(prompt):
    """CLIBotModule"""
    init_dspy()
    
    print(cli_bot_call(prompt=prompt))


from fastapi import APIRouter
router = APIRouter()

@router.post("/cli_bot/")
async def cli_bot_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return cli_bot_call(**data)


def main():
    init_dspy()
    prompt = ""
    print(cli_bot_call(prompt=prompt))
    

if __name__ == "__main__":
    main()
