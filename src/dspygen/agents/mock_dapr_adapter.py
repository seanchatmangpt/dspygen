from unittest.mock import MagicMock

from dspygen.agents.idapr_adapter import IDaprClientAdapter


import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='== APP == %(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S.%f')


from datetime import datetime

class MockDaprClientAdapter(IDaprClientAdapter):
    def __init__(self):
        self.workflows = {}
        self.activities = set()
        self.events = {}

    def start_workflow(self, workflow_component, workflow_name, input):
        instance_id = f"workflow_{len(self.workflows) + 1}"
        self.workflows[instance_id] = {
            "component": workflow_component,
            "name": workflow_name,
            "input": input,
            "status": "Running"
        }
        logging.info(f"Starting order workflow, purchasing {input.quantity} of {input.item_name}")
        return MagicMock(instance_id=instance_id)

    def get_workflow(self, instance_id, workflow_component):
        workflow = self.workflows.get(instance_id, {})
        status = workflow.get("status", "NotFound")
        logging.info(f"{instance_id}: Orchestration {status}")
        return MagicMock(runtime_status=status)

    def register_workflow(self, workflow):
        logging.info(f"Registered workflow: {workflow}")

    def register_activity(self, activity):
        self.activities.add(activity)
        logging.info(f"Registered activity: {activity}")

    def raise_workflow_event(self, instance_id, workflow_component, event_name, event_data):
        self.events[instance_id] = (event_name, event_data)
        logging.info(f"{instance_id} Event raised: {event_name}")
        if event_data.get('approval', False):
            workflow = self.workflows[instance_id]
            workflow['status'] = 'Approved'
            logging.info(f"Payment for order {instance_id} has been approved!")

