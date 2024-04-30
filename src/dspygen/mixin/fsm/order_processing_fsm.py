from enum import Enum, auto

import dspy
from pydantic import BaseModel, Field

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class OrderProcessingFSMState(Enum):
    """ Enum representing the states in the order processing lifecycle. """
    ORDER_PLACED = auto()
    ORDER_CONFIRMED = auto()
    PAYMENT_PROCESSED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    RETURNED = auto()


class OrderProcessingFSM(FSMMixin):
    def __init__(self):
        super().setup_fsm(OrderProcessingFSMState)
        # Initialize state-specific attributes if any

    @trigger(
        source=OrderProcessingFSMState.ORDER_PLACED,
        dest=OrderProcessingFSMState.ORDER_CONFIRMED,
        conditions=['verify_data'],
        after=['send_notification']
    )
    def confirm_order(self):
        """Handle the transition from ORDER_PLACED to ORDER_CONFIRMED."""
        print("Order confirmed.")

    @trigger(
        source=OrderProcessingFSMState.ORDER_CONFIRMED,
        dest=OrderProcessingFSMState.PAYMENT_PROCESSED,
        conditions=['check_compliance', 'validate_input'],
        after=['generate_invoice', 'send_receipt']
    )
    def process_payment(self):
        """Process payment and transition to PAYMENT_PROCESSED."""
        print("Payment processed.")

    @trigger(
        source=OrderProcessingFSMState.PAYMENT_PROCESSED,
        dest=OrderProcessingFSMState.SHIPPED,
        before=['update_inventory'],
        after=['track_shipment', 'send_notification']
    )
    def ship_order(self):
        """Ship the order and transition to SHIPPED."""
        print("Order shipped.")

    @trigger(
        source=OrderProcessingFSMState.SHIPPED,
        dest=OrderProcessingFSMState.DELIVERED,
        after=['update_status', 'send_notification']
    )
    def deliver_order(self):
        """Confirm order delivery."""
        print("Order delivered.")

    @trigger(
        source=[OrderProcessingFSMState.ORDER_PLACED, OrderProcessingFSMState.ORDER_CONFIRMED],
        dest=OrderProcessingFSMState.CANCELLED,
        after=['refund_payment', 'update_status', 'send_notification']
    )
    def cancel_order(self):
        """Cancel the order and transition to CANCELLED."""
        print("Order cancelled.")

    @trigger(
        source=OrderProcessingFSMState.DELIVERED,
        dest=OrderProcessingFSMState.RETURNED,
        conditions=['validate_input'],
        after=['initiate_return', 'refund_payment', 'update_status']
    )
    def return_order(self):
        """Handle order return and transition to RETURNED."""
        print("Order returned.")

    # Placeholder methods to simulate actions
    def verify_data(self):
        """Check if the order data is complete and valid."""
        return True  # Always returns True for simulation purposes

    def send_notification(self):
        """Send a notification to the customer about the current order status."""
        print("Notification sent.")

    def validate_input(self):
        """Ensure all inputs are valid for processing."""
        return True  # Always returns True for simulation purposes

    def check_compliance(self):
        """Verify compliance with financial regulations."""
        return True  # Always returns True for simulation purposes

    def generate_invoice(self):
        """Create an invoice for the confirmed order."""
        print("Invoice generated.")

    def send_receipt(self):
        """Send a payment receipt to the customer."""
        print("Receipt sent.")

    def update_inventory(self):
        """Deduct the ordered items from inventory."""
        print("Inventory updated.")

    def track_shipment(self):
        """Initiate and track the shipment of the order."""
        print("Shipment tracked.")

    def update_status(self):
        """Update the status of the order in the system."""
        print("Status updated.")

    def refund_payment(self):
        """Process the refund for the customer."""
        print("Payment refunded.")

    def initiate_return(self):
        """Handle the return process for returned orders."""
        print("Return initiated.")


def main2():
    """Main function to simulate the FSM process."""
    fsm = OrderProcessingFSM()
    fsm.confirm_order()  # Transition from Order_Placed to Order_Confirmed
    fsm.process_payment()  # Transition from Order_Confirmed to Payment_Processed
    fsm.ship_order()  # Transition from Payment_Processed to Shipped
    fsm.deliver_order()  # Transition from Shipped to Delivered

    # Simulate a scenario where an order is returned
    fsm.return_order()  # Transition from Delivered to Returned

    assert fsm.state == OrderProcessingFSMState.RETURNED.name


class Choice(BaseModel):
    choice: str = Field(..., description="The choice made by the user based on the possible possible_triggers.")


# def message_to_trigger(fsm, message):
#     from dspygen.utils.dspy_tools import init_dspy
#     from dspygen.lm.groq_lm import Groq
#     # init_dspy(Groq, 1000, "mixtral-8x7b-32768")
#     # init_dspy(Groq, max_tokens=1000, model="llama3-70b-8192")  # for Groq you must pass an Groq provided model
#
#     init_dspy()
#     poss = fsm.possible_triggers()
#     # from dspygen.modules.json_module import json_call
#     # response = json_call(schema=Choice.model_json_schema(),
#     #           text=f"{{\"possible_triggers\": {str(poss)}, \"prompt\": \"{message}\"}}")
#     choice = dspy.Predict("possible_triggers, prompt -> choice")(possible_triggers=str(poss), prompt=message).choice
#     # choice = Choice.model_validate_json(response)
#     # print(choice.choice)
#     # getattr(fsm, choice.choice)()


def message_to_trigger(fsm, message):
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()
    print(f"Current state: {fsm.state}")
    print(f"Message received: {message}")
    poss = fsm.possible_triggers()
    choice = dspy.Predict("possible_triggers, prompt -> choice")(possible_triggers=str(poss), prompt=message).choice
    print(f"GPT 3.5 can choose from these transitions:\n{poss}")
    print(f"GPT 3.5 chose: {choice}")
    getattr(fsm, choice)()


from faker import Faker
import json
import datetime

fake = Faker()


def create_json_message(action, **kwargs):
    message = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": fake.uuid4(),
        "session_id": fake.uuid4(),
        "action": action,
        "parameters": kwargs,
        "source": "web",
        "metadata": {
            "ip_address": fake.ipv4(),
            "user_agent": fake.user_agent()
        },
        "trace_info": {
            "correlation_id": f"corid-{fake.random_number(digits=8)}",
            "transaction_id": f"txn-{fake.random_number(digits=8)}"
        },
        "data": {
            "order_id": kwargs.get("order_id", fake.uuid4()),
            "details": "Details of the action to be taken"
        }
    }
    return json.dumps(message)


# Example usage in a main function
def main3():
    fsm = OrderProcessingFSM()

    # Creating a message to confirm an order with additional irrelevant details
    json_message = create_json_message("confirm_order", order_id="ORD002", quantity=3)
    message_to_trigger(fsm, str(json_message))

    # Creating a message to process payment
    msg2 = create_json_message("process_payment", order_id="ORD002", amount=100)
    message_to_trigger(fsm, str(msg2))

    # Creating a message to ship the order
    msg3 = create_json_message("ship_order", order_id="ORD002")
    message_to_trigger(fsm, str(msg3))

    print(json_message)  # Just to see what the message looks like


def main():
    fsm = OrderProcessingFSM()
    prompt = "I want to confirm the order."
    message_to_trigger(fsm, prompt)
    prompt = "I want to process the payment."
    message_to_trigger(fsm, prompt)
    prompt = "I want to ship the order."
    message_to_trigger(fsm, prompt)
    prompt = "I want to deliver the order."
    message_to_trigger(fsm, prompt)
    prompt = "I want to return the order."
    message_to_trigger(fsm, prompt)


if __name__ == '__main__':
    main()





