from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.utils.dspy_tools import init_ol
from dspygen.modules.fsm_trigger_module import fsm_trigger_call

class AnalyticsAgentState(Enum):
    IDLE = auto()
    ANALYZING = auto()
    REPORTING = auto()
    HANDLING_ERRORS = auto()
    COMPLETING_TASK = auto()

class AnalyticsAgent(FSMMixin):
    def __init__(self):
        super().setup_fsm(AnalyticsAgentState, initial=AnalyticsAgentState.IDLE)

    @trigger(source=AnalyticsAgentState.IDLE, dest=AnalyticsAgentState.ANALYZING)
    def start_analysis(self):
        print("Starting data analysis.")

    @trigger(source=AnalyticsAgentState.ANALYZING, dest=AnalyticsAgentState.REPORTING)
    def generate_report(self):
        print("Generating analysis report.")

    @trigger(source=[AnalyticsAgentState.ANALYZING, AnalyticsAgentState.REPORTING], dest=AnalyticsAgentState.HANDLING_ERRORS)
    def handle_error(self):
        print("Handling error in data analysis.")

    @trigger(source=AnalyticsAgentState.HANDLING_ERRORS, dest=AnalyticsAgentState.IDLE)
    def resolve_error(self):
        print("Error resolved, returning to idle.")

    @trigger(source=[AnalyticsAgentState.ANALYZING, AnalyticsAgentState.REPORTING], dest=AnalyticsAgentState.COMPLETING_TASK)
    def complete_task(self):
        print("Data analysis task completed.")

def main():
    init_ol(max_tokens=3000)  # Initialize any required DSPy settings
    agent = AnalyticsAgent()
    print("Initial state:", agent.state)

    # Simulate voice commands
    fsm_trigger_call("I want you to start analyzing the data", agent)
    fsm_trigger_call("Please generate the report now", agent)
    fsm_trigger_call("There is an issue, handle the error", agent)
    fsm_trigger_call("Now resolve the error", agent)
    fsm_trigger_call("Complete the data analysis task", agent)

    print("Final state:", agent.state)

if __name__ == "__main__":
    main()
