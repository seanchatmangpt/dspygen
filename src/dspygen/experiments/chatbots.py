from dspygen.modules.gen_keyword_arguments_module import invoke
from dspygen.utils.dspy_tools import init_dspy


def main():
    chat("bot: Hello world")


def chat(message: str):
    response = chat(invoke(chat, f"{message}\nbot:"))
    print(response)
    return response


if __name__ == '__main__':
    init_dspy()

    main()
