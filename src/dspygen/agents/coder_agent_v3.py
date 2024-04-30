from enum import Enum, auto

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.modules.function_invoke_module import function_invoke_call
from dspygen.modules.python_source_code_module import python_source_code_call


class CoderAgentState(Enum):
    """ Enum representing the states in the coding task lifecycle. """
    ANALYZING_REQUIREMENTS = auto()
    WRITING_CODE = auto()
    TESTING_CODE = auto()
    HANDLING_ERRORS = auto()
    REFACTORING_CODE = auto()
    COMPLETING_TASK = auto()


class CoderAgent(FSMMixin):
    def __init__(self):
        super().setup_fsm(CoderAgentState, initial=CoderAgentState.ANALYZING_REQUIREMENTS)
        # prompt = "Create a function called 'add_numbers' that takes two arguments 'a' and 'b' and returns their sum."
        prompt = "Write the bubblesort algorithm in Python."
        # prompt = "Write the tetris game."
        self.requirements = prompt
        self.code = ""
        self.errors = []
        self.test_results = ""

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        """Simulate writing a simple Python function."""
        self.code = python_source_code_call(self.requirements)
        print(f"Code written:\n\n{self.code}")

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        """Test the written code."""
        # Simple simulation of testing by executing the function
        try:
            exec(self.code)
            invoke = function_invoke_call(self.code)
            print(f"Invoking function:\n\n{invoke}")
            result = eval(invoke)

            self.test_results = "Test Passed: Output = " + str(result)
            print(self.test_results)
        except Exception as e:
            self.errors.append(str(e))
            print("Test Failed: ", str(e))

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.HANDLING_ERRORS, conditions=['errors_detected'])
    def handle_errors(self):
        """Handle errors if any are detected during testing."""
        print("Handling coding errors.")
        # Assuming error handling involves correcting a simple mistake
        self.code = self.code.replace("b", "b")
        self.errors.clear()

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.COMPLETING_TASK, unless=['errors_detected'])
    def complete_task(self):
        """Complete the coding task after successful testing."""
        print("Task completed without errors.")

    @trigger(source=CoderAgentState.HANDLING_ERRORS, dest=CoderAgentState.REFACTORING_CODE, conditions=['errors_resolved'])
    def refactor_code(self):
        """Refactor code after errors are resolved."""
        # Simple refactoring example by adding comments
        self.code = "# Added by refactoring\n" + self.code
        print("Code after refactoring:\n", self.code)

    @trigger(source=CoderAgentState.REFACTORING_CODE, dest=CoderAgentState.COMPLETING_TASK)
    def complete_refactored_task(self):
        """Complete the coding task after refactoring."""
        print("Task completed after refactoring.")

    def errors_detected(self):
        """Check if there are any errors in the code."""
        return len(self.errors) > 0

    def errors_resolved(self):
        """Check if the errors have been successfully resolved."""
        return len(self.errors) == 0


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy(max_tokens=3000)
    agent = CoderAgent()
    print("Initial state:", agent.state)
    agent.start_coding()
    agent.test_code()
    if agent.errors_detected():
        agent.handle_errors()
        agent.refactor_code()
    agent.complete_task()
    print("Final state:", agent.state)


if __name__ == "__main__":
    main()
