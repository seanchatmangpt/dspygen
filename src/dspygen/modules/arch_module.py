"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class ProjectPrompt(dspy.Signature):
    """
    Dynamically generates detailed project prompts for Python Enterprise Systems Architect interviews.

    This class takes a specified focus area and generates a comprehensive project prompt that
    encompasses key aspects of enterprise system architecture. The prompt includes a project
    description, core requirements, potential challenges, and specific focus areas. This
    generation process ensures each prompt is tailored to assess the candidate's expertise
    in designing scalable, robust, and efficient systems suitable for enterprise-level applications.

    Input:
        focus_area: A string representing the primary focus area for the project prompt, such as
                    'scalability', 'microservices', 'data processing', or 'fault tolerance'. This
                    input guides the dynamic generation process to emphasize certain aspects within
                    the prompt.

    Output:
        prompt: An instance of a custom class or a structured dictionary containing the generated
                project prompt details, including a brief description, key requirements, expected
                challenges, and specific focus areas for the candidate to address.
    """
    focus_area = dspy.InputField(desc="Primary focus area for the project prompt.")

    prompt = dspy.OutputField(desc="Generated project prompt detailing the project scope and objectives.")


class ArchModule(dspy.Module):
    """ArchModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None


    def forward(self, focus_area):
        pred = dspy.ChainOfThought(ProjectPrompt)
        self.output = pred(focus_area=focus_area).prompt
        return self.output


def arch_call(focus_area):
    arch = ArchModule()
    return arch.forward(focus_area=focus_area)


def main():
    init_dspy()
    focus_area = "Pytests for a file generation system"
    print(arch_call(focus_area=focus_area))


if __name__ == "__main__":
    main()
