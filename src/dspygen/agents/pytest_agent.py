import os
import subprocess
import tempfile
import pytest
from unittest.mock import MagicMock
from dspygen.utils.dspy_tools import init_dspy

# Assuming FSM mixin and state definitions are as discussed earlier
from dspygen.agents.coder_agent import CoderAgentState
from dspygen.agents.coder_agent_v4 import CoderAgent
from dspygen.mixin.fsm.fsm_mixin import trigger, FSMMixin


class PytestAgent(FSMMixin):
    def __init__(self, code):
        super().setup_fsm(CoderAgentState, initial=CoderAgentState.ANALYZING_REQUIREMENTS)
        self.code = code
        self.errors = []
        self.filename = None
        self.test_filename = None

    @trigger(source=CoderAgentState.ANALYZING_REQUIREMENTS, dest=CoderAgentState.WRITING_CODE)
    def start_coding(self):
        """Write code and tests to files."""
        self.filename = self.write_code_to_file(self.code)
        test_code = self.generate_mock_tests()
        self.test_filename = self.write_test_code_to_file(test_code)

    def write_code_to_file(self, code):
        """Write code to a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as f:
            f.write(code)
            return f.name

    def write_test_code_to_file(self, test_code):
        """Write test code to a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='_test.py', mode='w') as f:
            f.write(test_code)
            return f.name

    def generate_mock_tests(self):
        """Generate basic pytest tests with mocks."""

        # Generate with dspygen
        from dspygen.typetemp.functional import render
        from dspygen.utils.dspy_tools import init_ol
        lm = init_ol()
        # source_code = bad_code
        source_code = example_code
        from dspygen.modules.pytest_module import pytest_call
        result = pytest_call(source_code=source_code)
        from dspygen.utils.file_tools import extract_code
        import_str = "from {{ module }} import fetch_user_name\n\n"
        # print(extract_code(result))
        # print(lm.inspect_history(n=1))
        result = import_str + extract_code(result)
        rcode = render(result, module=os.path.basename(self.filename)[:-3])

        return rcode

    @trigger(source=CoderAgentState.WRITING_CODE, dest=CoderAgentState.TESTING_CODE)
    def test_code(self):
        """Run tests using pytest."""
        result = subprocess.run(['pytest', self.test_filename, '-v'], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            self.errors.append(result.stderr)
            print("Test Failed:", result.stdout)
        else:
            print("Test Passed:", result.stdout)

    @trigger(source=CoderAgentState.TESTING_CODE, dest=CoderAgentState.COMPLETING_TASK, unless=['errors_detected'])
    def complete_task(self):
        """Complete the task if tests pass."""
        print("Task completed successfully.")
        os.remove(self.filename)
        os.remove(self.test_filename)

    def errors_detected(self):
        """Check if there are any errors in the code."""
        return len(self.errors) > 0


example_code = """def fetch_user_name(user_id):
    import requests
    response = requests.get(f'https://api.example.com/users/{user_id}')
    return response.json()['name']
"""

def main():
    init_dspy(max_tokens=3000)  # Initialize the dspy environment
    code_agent = CoderAgent()
    agent = PytestAgent(code=example_code)
    print("Initial state:", agent.state)
    agent.start_coding()
    agent.test_code()
    if not agent.errors_detected():
        agent.complete_task()
    print("Final state:", agent.state)

if __name__ == "__main__":
    main()
