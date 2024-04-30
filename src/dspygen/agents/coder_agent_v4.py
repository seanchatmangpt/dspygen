import os
import subprocess
import tempfile

from dspygen.agents.coder_agent import CoderAgentState
from dspygen.mixin.fsm.fsm_mixin import trigger, FSMMixin
from dspygen.modules.function_invoke_module import function_invoke_call
from dspygen.modules.python_source_code_module import python_source_code_call


class CoderAgent(FSMMixin):
    def __init__(self):
        super().setup_fsm(CoderAgentState, initial=CoderAgentState.ANALYZING_REQUIREMENTS)
        prompt = "Write a tic tac toe pygame."
        self.requirements = prompt
        self.code = ""
        self.errors = []
        self.test_results = ""
        self.filename = None

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        """Simulate writing Python code."""
        self.code = python_source_code_call(self.requirements) + "\n\n"
        self.code += function_invoke_call(self.code) + "\n\n"
        print(f"Code written:\n\n{self.code}")
        self.filename = self.write_code_to_file(self.code)

    def write_code_to_file(self, code):
        """Write code to a temporary file and return the filename."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as f:
            f.write(code)
            return f.name

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        """Test the written code by executing the Python file."""
        output, error = self.execute_code(self.filename)
        if error:
            self.errors.append(error)
            print("Test Failed: ", error)
        else:
            self.test_results = "Test Passed: Output = " + output
            print(self.test_results)

    def execute_code(self, filepath):
        """Execute a Python script file and capture its output and errors."""
        try:
            result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "Execution timed out"

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.HANDLING_ERRORS, conditions=['errors_detected'])
    def handle_errors(self):
        """Handle errors if any are detected during testing."""
        print("Handling coding errors.")
        self.errors.clear()

    @trigger(source=CoderAgentState.HANDLING_ERRORS, dest=CoderAgentState.REFACTORING_CODE, conditions=['errors_resolved'])
    def refactor_code(self):
        """Refactor code after errors are resolved."""
        self.code = "# Added by refactoring\n" + self.code
        print("Code after refactoring:\n", self.code)
        os.remove(self.filename)  # Clean up the original file
        self.filename = self.write_code_to_file(self.code)  # Write the refactored code back to disk

    @trigger(source=CoderAgentState.REFACTORING_CODE, dest=CoderAgentState.COMPLETING_TASK)
    def complete_refactored_task(self):
        """Complete the coding task after refactoring."""
        print("Task completed after refactoring.")
        os.remove(self.filename)  # Clean up after completion

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.COMPLETING_TASK, unless=['errors_detected'])
    def complete_task(self):
        """Complete the coding task after successful testing."""
        print("Task completed without errors.")

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
