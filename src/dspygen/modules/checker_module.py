"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class CheckerModule(dspy.Module):
    """CheckerModule"""

    def forward(self, prompt, assertion):
        pred = dspy.ChainOfThought("prompt, assertion -> return_bool")
        result = pred(prompt=prompt, assertion=assertion).return_bool
        return result


def checker_call(prompt, assertion):
    checker = CheckerModule()
    return checker.forward(prompt=prompt, assertion=assertion)


def main():
    init_dspy()
    prompt = "The earth is flat"
    assertion = "True"
    print(checker_call(prompt=prompt, assertion=assertion))
    

if __name__ == "__main__":
    main()
