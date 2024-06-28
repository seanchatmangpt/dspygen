from dspygen.agents.coder_agent import CoderAgentState
from dspygen.mixin.fsm.fsm_mixin import trigger, FSMMixin


class CoderAgent(FSMMixin):
    def __init__(self, requirements: str):
        super().setup_fsm(CoderAgentState, initial=CoderAgentState.ANALYZING_REQUIREMENTS)

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        ...

    def write_code_to_file(self, code):
        ...

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        ...

    def execute_code(self, filepath):
        ...

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.HANDLING_ERRORS, conditions=['errors_detected'])
    def handle_errors(self):
        ...

    @trigger(source=[CoderAgentState.TESTING_CODE, CoderAgentState.HANDLING_ERRORS], dest=CoderAgentState.REFACTORING_CODE, conditions=['errors_resolved'])
    def refactor_code(self):
        ...

    @trigger(source=CoderAgentState.REFACTORING_CODE, dest=CoderAgentState.COMPLETING_TASK)
    def complete_refactored_task(self):
        ...

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.COMPLETING_TASK, unless=['errors_detected'])
    def complete_task(self):
        ...

    def errors_detected(self):
        """Check if there are any errors in the code."""
        return len(self.errors) > 0

    def errors_resolved(self):
        """Check if the errors have been successfully resolved."""
        return len(self.errors) == 0
