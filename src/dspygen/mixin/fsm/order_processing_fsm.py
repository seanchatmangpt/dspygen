from enum import Enum, auto
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
        source=OrderProcessingFSMState.ORDER_CONFIRMED,
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


def main():
    """Main function to simulate the FSM process."""
    fsm = OrderProcessingFSM()
    fsm.confirm_order()  # Transition from Order_Placed to Order_Confirmed
    fsm.process_payment()  # Transition from Order_Confirmed to Payment_Processed
    fsm.ship_order()  # Transition from Payment_Processed to Shipped
    fsm.deliver_order()  # Transition from Shipped to Delivered

    # Simulate a scenario where an order is returned
    fsm.return_order()  # Transition from Delivered to Returned

    assert fsm.state == OrderProcessingFSMState.RETURNED.name


if __name__ == '__main__':
    main()
