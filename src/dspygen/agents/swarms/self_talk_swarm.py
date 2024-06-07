from enum import Enum, auto

from pydantic import BaseModel, Field

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
import dspy

from dspygen.modules.json_module import json_call

text_api = []


class SalesAgentState(Enum):
    PROSPECTING = auto()
    NEGOTIATING = auto()
    CLOSING = auto()


class CustomerAgentState(Enum):
    BROWSING = auto()
    EVALUATING = auto()
    NEGOTIATING = auto()
    NOT_INTERESTED = auto()
    PURCHASING = auto()


def add_sales_message(message):
    text_api.append(f"Sales Agent: {message}")


def add_customer_message(message):
    text_api.append(f"Customer: {message}")


class SalesAgent(FSMMixin):
    def __init__(self, initial_price, minimum_price):
        super().__init__()
        self.product = None
        self.current_price = initial_price
        self.minimum_price = minimum_price
        self.setup_fsm(state_enum=SalesAgentState, initial=SalesAgentState.PROSPECTING)

    @trigger(source=SalesAgentState.PROSPECTING, dest=SalesAgentState.NEGOTIATING)
    def engage_customer(self):
        self.product = dspy.Predict("prompt -> product_type")(prompt=self.prompts[0]).product_type
        message = f"Hello! We have a new {self.product}. Interested?"
        add_sales_message(message)

    @trigger(source=SalesAgentState.NEGOTIATING, dest=SalesAgentState.NEGOTIATING)
    def propose_price(self):
        message = f"The price for {self.product} is ${self.current_price}."
        print("Sales Agent:", message)
        add_sales_message(message)

    @trigger(source=SalesAgentState.NEGOTIATING, dest=SalesAgentState.CLOSING)
    def close_deal(self):
        message = f"Great! Finalizing the deal for {self.product} at ${self.current_price}."
        print("Sales Agent:", message)
        add_sales_message(message)

    def lower_price(self, amount):
        self.current_price -= amount
        if self.current_price < self.minimum_price:
            self.current_price = self.minimum_price

    def respond(self, prompt):
        from dspygen.modules.challenger_sales_manager_module import challenger_sales_manager_call
        response = challenger_sales_manager_call(prompt=prompt)
        return response.split("---")[0]


class IsInterested(BaseModel):
    reasoning: str = Field(..., description="Let's think step by step about if the customer is interested.")
    is_interested: bool = Field(..., description="The boolean value indicating if the customer is interested.")


class CustomerAgent(FSMMixin):
    def __init__(self, desired_products=None, budget=750):
        super().__init__()
        self.desired_products = desired_products
        self.budget = budget
        self.setup_fsm(state_enum=CustomerAgentState, initial=CustomerAgentState.BROWSING)

    @trigger(source=CustomerAgentState.BROWSING, dest=CustomerAgentState.EVALUATING)
    def evaluate_product(self):
        interest = json_call(IsInterested, text=f"The product for sale is {self.prompts[0]}.\n"
                                                f"The customer desired products are {str(self.desired_products)}.\n")

        if interest.is_interested:
            add_customer_message(f"I am interested in the {self.desired_products[0]}.")
        else:
            add_customer_message(f"I am not interested in the {self.desired_products[0]}.")

    @trigger(source=CustomerAgentState.EVALUATING, dest=CustomerAgentState.NEGOTIATING)
    def start_negotiation(self):
        message = "Let's talk about the price."
        print("Customer:", message)
        add_customer_message("Customer: Let's talk about the price.")

    @trigger(source=CustomerAgentState.EVALUATING, dest=CustomerAgentState.NOT_INTERESTED)
    def not_interested(self):
        message = "I'm not interested in the product."
        print("Customer:", message)
        add_customer_message("Customer: I'm not interested in the product.")

    @trigger(source=CustomerAgentState.NEGOTIATING, dest=CustomerAgentState.PURCHASING)
    def accept_price(self):
        message = "I'll take it at this price."
        print("Customer:", message)
        add_customer_message("Customer: I'll take it at this price.")

    def negotiate(self, sales_agent):
        prompt = f"The sales agent offered the {sales_agent.product} for ${sales_agent.current_price}. Can you go lower?"
        response = dspy.Predict("prompt -> decision")(prompt=prompt).decision
        decision = response.split("---")[0].strip()

        if sales_agent.current_price > self.budget:
            return False  # Continue negotiation
        else:
            return True  # Accept the price


def simulate_conversation():
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    sales_agent = SalesAgent(initial_price=1000, minimum_price=700)
    customer_agent = CustomerAgent(desired_products=["smartphone"], budget=800)

    # Simulate the conversation
    sales_agent.prompt("A new smartphone is available for sale.")

    customer_agent.prompt(text_api[-1])

    customer_agent.start_negotiation()

    negotiation_success = False
    while negotiation_success is False:
        sales_agent.propose_price()
        customer_decision = customer_agent.negotiate(sales_agent)

        if customer_decision is True:
            customer_agent.accept_price()
            sales_agent.close_deal()
            negotiation_success = True
        else:
            sales_agent.lower_price(50)

    # Output the conversation
    print("\n--- Conversation Log ---")
    for msg in text_api:
        print(msg)


if __name__ == '__main__':
    simulate_conversation()
