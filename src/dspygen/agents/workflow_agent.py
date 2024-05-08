from dspygen.agents.order_payload import OrderPayload
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from enum import Enum, auto
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='== APP == %(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Business logic functions
def notify_activity(message):
    """Log notifications about the workflow."""
    logging.info(message)

def process_payment_activity(order_id, amount):
    """Process and authorize the payment for an order."""
    logging.info(f"Processing payment: {order_id} for ${amount}")
    return True

def verify_inventory_activity(item_name, quantity, inventory):
    """Check if there is enough inventory present for the purchase."""
    available = inventory.get(item_name, 0)
    if available >= quantity:
        logging.info(f"VerifyInventoryActivity: There are {available} {item_name}s available for purchase")
        return True
    else:
        logging.info("VerifyInventoryActivity: Insufficient inventory!")
        return False

def update_inventory_activity(item_name, quantity, inventory):
    """Remove the requested items from inventory and update the store."""
    if inventory[item_name] >= quantity:
        inventory[item_name] -= quantity
        logging.info(f"UpdateInventoryActivity: There are now {inventory[item_name]} {item_name}s left in stock")
        return True
    else:
        logging.error(f"UpdateInventoryActivity: Failed to update inventory for {item_name}")
        return False

def request_approval_activity(order_id, amount):
    """Request manager's approval if the payment amount is over $50,000."""
    if amount > 50000:
        logging.info(f"RequestApprovalActivity: Requesting approval for payment of ${amount} USD for order {order_id}")
        return True
    return False

# FSM State Enum
class WorkflowAgentState(Enum):
    INITIALIZING = auto()
    REGISTERING = auto()
    PROCESSING = auto()
    MONITORING = auto()
    COMPLETING = auto()

# FSM Agent Class
class WorkflowFSMAgent(FSMMixin):
    def __init__(self, dapr_adapter, baseInventory):
        super().setup_fsm(state_enum=WorkflowAgentState, initial=WorkflowAgentState.INITIALIZING)
        self.dapr_adapter = dapr_adapter
        self.baseInventory = baseInventory
        self.workflow_instance_id = None
        self.order_payload = None
        self.workflow_component = 'workflow_component'
        self.workflow_name = 'order_processing_workflow'

    @trigger(source=WorkflowAgentState.INITIALIZING, dest=WorkflowAgentState.REGISTERING)
    def register_workflow_and_activities(self):
        # self.dapr_adapter.register_workflow(order_processing_workflow)
        self.dapr_adapter.register_activity(notify_activity)
        self.dapr_adapter.register_activity(request_approval_activity)
        self.dapr_adapter.register_activity(verify_inventory_activity)
        self.dapr_adapter.register_activity(process_payment_activity)
        self.dapr_adapter.register_activity(update_inventory_activity)
        # self.dapr_adapter.start()

    @trigger(source=WorkflowAgentState.REGISTERING, dest=WorkflowAgentState.PROCESSING)
    def start_workflow(self, item_name, order_quantity):
        total_cost = int(order_quantity) * self.baseInventory[item_name].per_item_cost
        self.order_payload = OrderPayload(item_name=item_name, quantity=int(order_quantity), total_cost=total_cost)
        start_resp = self.dapr_adapter.start_workflow(self.workflow_component, self.workflow_name, input=self.order_payload)
        self.workflow_instance_id = start_resp.instance_id

    @trigger(source=WorkflowAgentState.PROCESSING, dest=WorkflowAgentState.MONITORING)
    def monitor_workflow(self):
        pass

    @trigger(source=WorkflowAgentState.MONITORING, dest=WorkflowAgentState.COMPLETING)
    def complete_workflow(self, result):
        print(f"Workflow completed! Result: {result}")

    # After completing go back to the initial state
    @trigger(source=WorkflowAgentState.COMPLETING, dest=WorkflowAgentState.INITIALIZING)
    def reset_workflow(self):
        print("Resetting workflow agent state")

    def prompt_for_approval(self):
        self.dapr_adapter.raise_workflow_event(self.workflow_instance_id, self.workflow_component, "manager_approval", {'approval': True})

    def check_workflow_state(self):
        state = self.dapr_adapter.get_workflow(self.workflow_instance_id, self.workflow_component)
        if state.runtime_status in ["Completed", "Failed", "Terminated"]:
            self.trigger('complete_workflow', result=state.runtime_status)


def main():
    from dspygen.utils.dspy_tools import init_ol
    from unittest.mock import MagicMock

    init_ol(max_tokens=3000)
    from dspygen.agents.mock_dapr_adapter import MockDaprClientAdapter
    adapter = MockDaprClientAdapter()
    inventory = {"item1": MagicMock(per_item_cost=100)}  # Setting up a mocked inventory

    agent = WorkflowFSMAgent(adapter, inventory)
    print("Initial state:", agent.state)

    # Simulate the registration and setup of workflows and activities
    agent.prompt("Initialize workflow and activities")
    print("State after initialization:", agent.state)

    # Start the workflow with specific item and quantity
    agent.prompt("Start workflow for item1 with quantity 10", item_name="item1", order_quantity=10)
    print("State after starting the workflow:", agent.state)

    # Mocking a scenario where monitoring might need to reprocess
    # Assuming we have a way to check and decide if reprocessing is necessary
    needs_reprocessing = True  # This should ideally be determined by some condition checks
    if needs_reprocessing:
        agent.prompt("Reprocess workflow")
        print("State after reprocessing:", agent.state)

    # Completing the workflow
    agent.prompt("Complete workflow", result="Success")
    print("State after completion:", agent.state)

    # Resetting the workflow for another cycle or end
    agent.prompt("Reset the workflow")
    print("Final state:", agent.state)


if __name__ == '__main__':
    main()
