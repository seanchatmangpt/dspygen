import dspy
from dspygen.utils.dspy_tools import init_dspy


class ProductManagerSignature(dspy.Signature):
    """
    Generate an advanced Product Requirements Document (PRD) based on given file paths and README content.
    This class is designed to operate at the level expected of a FAANG product manager, ensuring that the
    generated PRD meets industry standards for clarity, comprehensiveness, and strategic alignment.
    """

    path = dspy.InputField(
        desc="The file path to the directory where the PRD will be generated. This should be a valid path on the filesystem where the output will be saved."
    )

    readme = dspy.InputField(
        desc="The content of the README file in markdown format. This content typically includes the project overview, objectives, target audience, key features, and other essential information that will guide the PRD generation process."
    )

    prd = dspy.OutputField(
        desc="The generated advanced Product Requirements Document (PRD) in a detailed and structured format, ready for review and implementation.",
        prefix="```markdown\n"
    )


class ProductManagerModule(dspy.Module):
    """ProductManagerModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, path, readme):
        pred = dspy.ChainOfThought(ProductManagerSignature)
        self.output = pred(path=path, readme=readme).prd
        return self.output


def prd_call(path, readme):
    prd_module = ProductManagerModule()
    return prd_module.forward(path=path, readme=readme)


def main():
    init_dspy()
    path = ""
    readme = ""
    result = prd_call(path=path, readme=readme)
    print(result)


if __name__ == "__main__":
    main()
