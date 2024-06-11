"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class GenerateProblemPDDL(dspy.Signature):
    problem_content = dspy.InputField(
        desc="Content for the PDDL problem file.")
    problem_file = dspy.OutputField(
        desc="PDDL problem file path.",
        prefix="Here is the generated problem PDDL file path:\n\n")


class GenerateProblemPDDLModuleModule(dspy.Module):
    """GenerateProblemPDDLModuleModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, problem_content):
        pred = dspy.Predict(GenerateProblemPDDL)
        self.output = pred(problem_content=problem_content).problem_file
        return self.output


def generate_problem_pddl_module_call(problem_content):
    generate_problem_pddl_module = GenerateProblemPDDLModuleModule()
    return generate_problem_pddl_module.forward(problem_content=problem_content)



def main():
    init_dspy()
    problem_content = ""
    result = generate_problem_pddl_module_call(problem_content=problem_content)
    print(result)


if __name__ == "__main__":
    main()
