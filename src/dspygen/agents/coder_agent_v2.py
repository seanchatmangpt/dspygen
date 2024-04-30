from enum import Enum, auto

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


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
        super().setup_fsm(CoderAgentState)
        self.git_repo = None
        self.code_base = None
        self.tests = None
        self.errors = None
        self.console_output = None

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        """Transition from analyzing requirements to writing code."""
        print("Starting to write code.")

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        """Transition from writing code to testing code."""
        print("Testing code now.")

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.HANDLING_ERRORS, conditions=['errors_detected'])
    def handle_errors(self):
        """Handle errors if any are detected during testing."""
        print("Handling coding errors.")

    @trigger(source="*", dest=CoderAgentState.REFACTORING_CODE, conditions=['errors_resolved'])
    def refactor_code(self):
        """Refactor code after errors are resolved."""
        print("Refactoring code.")

    @trigger(source=CoderAgentState.REFACTORING_CODE, dest=CoderAgentState.COMPLETING_TASK)
    def complete_task(self):
        """Complete the coding task after successful refactoring."""
        print("Task completed.")

    def errors_detected(self):
        """Check if there are any errors in the code."""
        return False

    def errors_resolved(self):
        """Check if the errors have been successfully resolved."""
        return True

    def setup_transitions(self):
        pass  # All transitions are already set up via decorators


def main():
    agent = CoderAgent()
    assert agent.state == CoderAgentState.ANALYZING_REQUIREMENTS.name, "Should start in ANALYZING_REQUIREMENTS"
    agent.start_coding()
    assert agent.state == CoderAgentState.WRITING_CODE.name, "Should be in WRITING_CODE after starting coding"
    agent.test_code()
    assert agent.state == CoderAgentState.TESTING_CODE.name, "Should be in TESTING_CODE after testing code"
    agent.handle_errors()  # Will not transition if errors_detected returns False
    assert agent.state == CoderAgentState.TESTING_CODE.name, "Should still be in TESTING_CODE if no errors detected"
    agent.refactor_code()  # Assuming no errors, directly to refactoring to simulate resolved state
    assert agent.state == CoderAgentState.REFACTORING_CODE.name, "Should be in REFACTORING_CODE after handling errors"
    agent.complete_task()
    assert agent.state == CoderAgentState.COMPLETING_TASK.name, "Should be in COMPLETING_TASK after completing task"
    print("All transitions are valid and correctly executed.")


if __name__ == "__main__":
    main()
