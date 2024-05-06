# Signature for generating mocks based on classes and methods
import dspy
from dspy.teleprompt import MIPRO


class GenerateMocks(dspy.Signature):
    """Generate mocks for classes and functions."""
    class_names = dspy.InputField(desc="List of classes to generate mocks for.")
    method_names = dspy.InputField(desc="List of methods to generate mocks for.")
    mocks = dspy.OutputField(desc="Generated mocks for the input classes and methods.")


class GenerateTestCases(dspy.Signature):
    """Generate test cases for the given mocks."""
    mocks = dspy.InputField(desc="The mocks generated for the buggy file.")
    test_cases = dspy.OutputField(desc="Generated test cases.")


# Define a module to create and optimize the mocks and tests
class AutoPytestMockRover(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_mocks = dspy.ChainOfThought("class_names,method_names->mocks")
        self.generate_test_cases = dspy.ChainOfThought("mocks->test_cases")

    def forward(self, class_names, method_names):
        mocks = self.generate_mocks(class_names=str(class_names), method_names=str(method_names)).mocks
        test_cases = self.generate_test_cases(mocks=mocks).test_cases
        return dspy.Prediction(mocks=mocks, test_cases=test_cases)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    apmr = AutoPytestMockRover()
    class_names = ["ChatGPTRetriever", "ChatGPTChromaDBRetriever"]
    method_names = ["forward", "prepare_queries"]
    result = apmr.forward(class_names=class_names, method_names=method_names)
    print(result)


if __name__ == '__main__':
    main()
