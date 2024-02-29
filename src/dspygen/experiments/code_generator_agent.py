from dspygen.modules.gen_keyword_arguments_module import invoke
from dspygen.modules.python_expert_module import python_expert_call
from dspygen.utils.dspy_tools import init_dspy


def main():
    init_dspy()
    result = invoke(python_expert_call, "User Story: FastAPI CRUD routes for Fire Alarm IoT")
    print(result)


if __name__ == '__main__':
    main()
