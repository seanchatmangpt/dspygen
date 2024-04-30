# import pytest
#
# from dspygen.agents.coder_agent import CoderAgent, CoderAgentState
#
#
# @pytest.fixture
# def coder_agent():
#     return CoderAgent()
#
#
# @pytest.fixture
# def coder_in_writing_code(coder_agent):
#     coder_agent.start_coding()  # Assuming this transition sets the state correctly
#     return coder_agent
#
#
# @pytest.fixture
# def coder_in_testing_code(coder_agent):
#     coder_agent.start_coding()
#     coder_agent.test_code()  # Transition to TESTING_CODE
#     return coder_agent
#
#
# @pytest.fixture
# def coder_in_handling_errors(coder_agent):
#     coder_agent.start_coding()
#     coder_agent.test_code()
#     # Assuming `test_code` could transition to HANDLING_ERRORS under certain conditions
#     # For the fixture, we can manually set it for consistency if the transition isn't guaranteed
#     coder_agent.state = CoderAgentState.HANDLING_ERRORS.name
#     return coder_agent
#
#
# @pytest.fixture
# def coder_in_refactoring_code(coder_agent):
#     coder_agent.start_coding()
#     coder_agent.test_code()
#     coder_agent.handle_errors()
#     coder_agent.refactor_code()  # Transition to REFACTORING_CODE
#     return coder_agent
#
#
# @pytest.fixture
# def coder_in_completing_task(coder_agent):
#     coder_agent.start_coding()
#     coder_agent.test_code()
#     coder_agent.handle_errors()
#     coder_agent.refactor_code()
#     coder_agent.complete_task()  # Transition to COMPLETING_TASK
#     return coder_agent
#
#
# def test_start_coding(coder_in_writing_code, capsys):
#     assert coder_in_writing_code.state == CoderAgentState.WRITING_CODE.name
#     captured = capsys.readouterr()
#     assert "Starting to write code." in captured.out
#
#
# def test_transition_to_testing(coder_in_testing_code, capsys):
#     assert coder_in_testing_code.state == CoderAgentState.TESTING_CODE.name
#     captured = capsys.readouterr()
#     assert "Testing code now." in captured.out
#
#
# def test_handle_errors_conditionally(coder_in_testing_code, capsys):
#     coder_in_testing_code.errors_detected = lambda: True  # Force errors to be detected
#     coder_in_testing_code.handle_errors()
#     assert coder_in_testing_code.state == CoderAgentState.HANDLING_ERRORS.name
#     captured = capsys.readouterr()
#     assert "Handling coding errors." in captured.out
