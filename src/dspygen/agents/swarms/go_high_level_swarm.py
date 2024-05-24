from dspygen.agents.challenger_agent import ChallengerSalesAgent
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.agents.coder_agent_v4 import CoderAgent

from enum import Enum, auto


class MarketingAgentState(Enum):
    IDLE = auto()
    ANALYZING_MARKET = auto()
    PLANNING_CAMPAIGNS = auto()
    EXECUTING_CAMPAIGNS = auto()


class CustomerSupportAgentState(Enum):
    IDLE = auto()
    PROVIDING_SUPPORT = auto()
    FOLLOWING_UP = auto()
    RESOLVING_ISSUES = auto()


class QualityAssuranceAgentState(Enum):
    IDLE = auto()
    CONDUCTING_TESTS = auto()
    REVIEWING_RESULTS = auto()
    REPORTING_ISSUES = auto()


class DataAnalysisAgentState(Enum):
    IDLE = auto()
    ANALYZING_DATA = auto()
    GENERATING_REPORTS = auto()
    PROVIDING_INSIGHTS = auto()


class ProductDevelopmentAgentState(Enum):
    IDLE = auto()
    DEVELOPING_PRODUCT = auto()
    TESTING_PRODUCT = auto()
    LAUNCHING_PRODUCT = auto()


class HumanResourcesAgentState(Enum):
    IDLE = auto()
    MANAGING_RECRUITMENT = auto()
    ONBOARDING_NEW_EMPLOYEES = auto()
    DEVELOPING_POLICIES = auto()


class FinanceAgentState(Enum):
    IDLE = auto()
    MANAGING_FINANCES = auto()
    PLANNING_BUDGETS = auto()
    CONDUCTING_AUDITS = auto()


class MarketingAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=MarketingAgentState, initial=MarketingAgentState.IDLE)

    @trigger(source=MarketingAgentState.IDLE, dest=MarketingAgentState.ANALYZING_MARKET)
    def analyze_market(self):
        print("Analyzing market trends and opportunities.")


class CustomerSupportAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=CustomerSupportAgentState, initial=CustomerSupportAgentState.IDLE)

    @trigger(source=CustomerSupportAgentState.IDLE, dest=CustomerSupportAgentState.PROVIDING_SUPPORT)
    def provide_support(self):
        print("Providing support and addressing customer queries.")


class QualityAssuranceAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=QualityAssuranceAgentState, initial=QualityAssuranceAgentState.IDLE)

    @trigger(source=QualityAssuranceAgentState.IDLE, dest=QualityAssuranceAgentState.CONDUCTING_TESTS)
    def conduct_testing(self):
        print("Conducting quality assurance tests on products and services.")


class DataAnalysisAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=DataAnalysisAgentState, initial=DataAnalysisAgentState.IDLE)

    @trigger(source=DataAnalysisAgentState.IDLE, dest=DataAnalysisAgentState.ANALYZING_DATA)
    def analyze_data(self):
        print("Performing data analysis to extract actionable insights.")


class ProductDevelopmentAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=ProductDevelopmentAgentState, initial=ProductDevelopmentAgentState.IDLE)

    @trigger(source=ProductDevelopmentAgentState.IDLE, dest=ProductDevelopmentAgentState.DEVELOPING_PRODUCT)
    def develop_product(self):
        print("Developing new products based on market and sales insights.")


class HumanResourcesAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=HumanResourcesAgentState, initial=HumanResourcesAgentState.IDLE)

    @trigger(source=HumanResourcesAgentState.IDLE, dest=HumanResourcesAgentState.MANAGING_RECRUITMENT)
    def manage_recruitment(self):
        print("Managing recruitment and employee relations.")


class FinanceAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=FinanceAgentState, initial=FinanceAgentState.IDLE)

    @trigger(source=FinanceAgentState.IDLE, dest=FinanceAgentState.MANAGING_FINANCES)
    def manage_finances(self):
        print("Handling financial operations and budgeting.")


class AdvancedInteractionSwarm:
    def __init__(self):
        self.challenger_agent = ChallengerSalesAgent()
        self.coder_agent = CoderAgent(requirements="Develop a feature integrating sales and coding processes.")
        self.marketing_agent = MarketingAgent()
        self.customer_support_agent = CustomerSupportAgent()
        self.quality_assurance_agent = QualityAssuranceAgent()
        self.data_analysis_agent = DataAnalysisAgent()
        self.product_development_agent = ProductDevelopmentAgent()
        self.human_resources_agent = HumanResourcesAgent()
        self.finance_agent = FinanceAgent()

    def execute_advanced_interactions(self):
        from dspygen.utils.dspy_tools import init_ol
        init_ol()

        print("Initiating advanced interactions among multiple agents.")
        # Marketing and data analysis
        self.marketing_agent.analyze_market()
        self.data_analysis_agent.analyze_data()

        # Sales and product development
        self.challenger_agent.start_research()
        self.product_development_agent.develop_product()

        # Coding and quality assurance
        self.coder_agent.start_coding()
        self.quality_assurance_agent.conduct_testing()

        # Customer support and finance operations
        self.customer_support_agent.provide_support()
        self.finance_agent.manage_finances()

        # Complete interactions
        self.challenger_agent.complete_sale()
        self.coder_agent.complete_task()

        print("Advanced interactions completed successfully among all agents.")


def main():
    swarm = AdvancedInteractionSwarm()
    swarm.execute_advanced_interactions()


if __name__ == '__main__':
    main()
