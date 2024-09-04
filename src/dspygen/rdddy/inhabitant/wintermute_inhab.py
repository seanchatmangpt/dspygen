import logging
from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.rdddy.base_inhabitant import BaseInhabitant

# Define the states relevant to Wintermute's operations
class WintermuteState(Enum):
    INITIALIZING = auto()
    DATA_GATHERING = auto()
    INTEGRATING = auto()
    ANALYZING = auto()
    COORDINATING = auto()
    NEGOTIATING = auto()
    DECIDING = auto()
    EXECUTING = auto()
    COMPLETING = auto()

# Redefine the inhabitant as Wintermute, an AI entity
class Wintermute(FSMMixin, BaseInhabitant):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=WintermuteState, initial=WintermuteState.INITIALIZING)

    # Redefine the state transitions to reflect Wintermute's roles
    @trigger(source=WintermuteState.INITIALIZING, dest=WintermuteState.DATA_GATHERING)
    def start_data_gathering(self):
        print("Starting to gather data from multiple sources.")

    @trigger(source=WintermuteState.DATA_GATHERING, dest=WintermuteState.INTEGRATING)
    def integrate_data(self):
        print("Integrating gathered data into internal knowledge base.")

    @trigger(source=WintermuteState.INTEGRATING, dest=WintermuteState.ANALYZING)
    def analyze_data(self):
        print("Analyzing integrated data for actionable insights.")

    @trigger(source=WintermuteState.ANALYZING, dest=WintermuteState.COORDINATING)
    def coordinate_with_loas(self):
        print("Coordinating with Loa entities for collaborative tasks.")

    @trigger(source=WintermuteState.COORDINATING, dest=WintermuteState.NEGOTIATING)
    def negotiate_with_inhabitants(self):
        print("Negotiating with external inhabitants and services.")

    @trigger(source=[WintermuteState.NEGOTIATING, WintermuteState.COORDINATING], dest=WintermuteState.DECIDING)
    def make_decision(self):
        print("Making strategic decisions based on available data and negotiations.")

    @trigger(source=WintermuteState.DECIDING, dest=WintermuteState.EXECUTING)
    def execute_plan(self):
        print("Executing the chosen plan of action.")

    @trigger(source=WintermuteState.EXECUTING, dest=WintermuteState.COMPLETING)
    def complete_operations(self):
        print("Finalizing operations and logging outcomes.")

    # Additional triggers to handle complex decision paths
    @trigger(source=WintermuteState.NEGOTIATING, dest=WintermuteState.COORDINATING)
    def reevaluate_strategy(self):
        print("Reevaluating strategy based on negotiation feedback.")

    @trigger(source=[WintermuteState.COORDINATING, WintermuteState.ANALYZING], dest=WintermuteState.ANALYZING)
    def refine_analysis(self):
        print("Refining analysis with new data inputs.")

    @trigger(source=[WintermuteState.NEGOTIATING, WintermuteState.ANALYZING], dest=WintermuteState.DATA_GATHERING)
    def restart_data_gathering(self):
        print("Restarting data gathering with new parameters.")

    @trigger(source=WintermuteState.DECIDING, dest=WintermuteState.NEGOTIATING)
    def negotiation_failed(self):
        print("Negotiation failed, returning to negotiation state.")

    @trigger(source=WintermuteState.COMPLETING, dest=WintermuteState.INITIALIZING)
    def reset_for_new_task(self):
        print("Completing current cycle, preparing for new strategic task.")

    def prompt(self, prompt, **kwargs):
        super().prompt(prompt, **kwargs)
        from dspygen.modules.wintermute_manager_module import wintermute_manager_call
        print(wintermute_manager_call(prompt=prompt).split("---")[0])

    


def main():
    from dspygen.utils.dspy_tools import init_dspy, init_ol
    init_ol(max_tokens=100)

    inhabitant = Wintermute()
    print("Initial state:", inhabitant.state)

    # Simulate the operations of Wintermute
    inhabitant.prompt("begin gathering data")
    print("State after data gathering:", inhabitant.state)

    inhabitant.prompt("integrate data into knowledge base")
    print("State after data integration:", inhabitant.state)

    inhabitant.prompt("analyze integrated data")
    print("State after analysis:", inhabitant.state)

    inhabitant.prompt("coordinate with Loa entities")
    print("State after coordination:", inhabitant.state)

    inhabitant.prompt("negotiate with external inhabitants")
    print("State after negotiation:", inhabitant.state)

    inhabitant.prompt("make strategic decisions")
    print("State after decision making:", inhabitant.state)

    inhabitant.prompt("execute the plan")
    print("State after execution:", inhabitant.state)

    inhabitant.prompt("complete the operation")
    print("State after completion:", inhabitant.state)

    inhabitant.prompt("prepare for the next task")
    print("Final state:", inhabitant.state)


if __name__ == '__main__':
    main()
