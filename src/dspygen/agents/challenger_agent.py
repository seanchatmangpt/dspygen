import logging
from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.rdddy.base_inhabitant import BaseInhabitant


class SalesState(Enum):
    INITIALIZING = auto()
    RESEARCHING = auto()
    OUTREACHING = auto()
    DISCOVERING = auto()
    TAILORING = auto()
    HANDLING_OBJECTIONS = auto()
    CLOSING = auto()
    COMPLETING = auto()


class ChallengerSalesAgent(FSMMixin, BaseInhabitant):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=SalesState, initial=SalesState.INITIALIZING)

    @trigger(source=SalesState.INITIALIZING, dest=SalesState.RESEARCHING)
    def start_research(self):
        print("Starting market and lead research.")

    @trigger(source=SalesState.RESEARCHING, dest=SalesState.OUTREACHING)
    def conduct_outreach(self):
        print("Conducting outreach to potential leads.")

    @trigger(source=SalesState.OUTREACHING, dest=SalesState.DISCOVERING)
    def perform_discovery(self):
        print("Engaging in discovery process to understand client needs.")

    @trigger(source=SalesState.DISCOVERING, dest=SalesState.TAILORING)
    def tailor_solution(self):
        print("Tailoring solutions based on discovered needs.")

    @trigger(source=SalesState.TAILORING, dest=SalesState.HANDLING_OBJECTIONS)
    def handle_objections(self):
        print("Addressing client objections and concerns.")

    @trigger(source=[SalesState.HANDLING_OBJECTIONS, SalesState.OUTREACHING], dest=SalesState.CLOSING)
    def close_deal(self):
        print("Closing the deal with the client.")

    @trigger(source=SalesState.CLOSING, dest=SalesState.COMPLETING)
    def complete_sale(self):
        print("Finalizing all post-sale processes and ensuring client satisfaction.")

    # Additional triggers to handle loops and branching
    @trigger(source=SalesState.HANDLING_OBJECTIONS, dest=SalesState.TAILORING)
    def revise_proposal(self):
        print("Revising proposal based on feedback.")

    @trigger(source=[SalesState.OUTREACHING, SalesState.TAILORING, SalesState.DISCOVERING], dest=SalesState.DISCOVERING)
    def deepen_discovery(self):
        print("Returning to discovery to gather more information.")

    @trigger(source=[SalesState.HANDLING_OBJECTIONS, SalesState.DISCOVERING], dest=SalesState.OUTREACHING)
    def restart_outreach(self):
        print("Restarting outreach with new strategy or contact.")

    @trigger(source=SalesState.CLOSING, dest=SalesState.HANDLING_OBJECTIONS)
    def negotiation_failed(self):
        print("Negotiation failed, addressing remaining objections.")

    @trigger(source=SalesState.COMPLETING, dest=SalesState.INITIALIZING)
    def new_opportunity(self):
        print("Completing current cycle, preparing for new opportunity.")

    def prompt(self, prompt, **kwargs):
        super().prompt(prompt, **kwargs)
        from dspygen.modules.challenger_sales_manager_module import challenger_sales_manager_call
        print(challenger_sales_manager_call(prompt=prompt).split("---")[0])


def main():
    from dspygen.utils.dspy_tools import init_dspy, init_ol
    # init_dspy(model="gpt-4o")
    init_ol(max_tokens=100)

    agent = ChallengerSalesAgent()
    print("Initial state:", agent.state)

    # Simulate the registration and setup of sales processes
    agent.prompt("begin researching the market")
    print("State after market research:", agent.state)

    agent.prompt("start reaching out to leads")
    print("State after outreach:", agent.state)

    agent.prompt("get to know the client needs")
    print("State after discovery:", agent.state)

    agent.prompt("customize the solutions for client")
    print("State after tailoring solutions:", agent.state)

    agent.prompt("deal with client concerns")
    print("State after handling objections:", agent.state)

    agent.prompt("update the proposal based on feedback")
    print("State after revising proposal:", agent.state)

    agent.prompt("gather more details about the client")
    print("State after deepening discovery:", agent.state)

    agent.prompt("reach out to more potential clients")
    print("State after restarting outreach:", agent.state)

    agent.prompt("finalize the deal")
    print("State after closing the deal:", agent.state)

    agent.prompt("wrap up the sale")
    print("State after completing the sale:", agent.state)

    agent.prompt("get ready for the next client")
    print("Final state:", agent.state)


if __name__ == '__main__':
    main()
