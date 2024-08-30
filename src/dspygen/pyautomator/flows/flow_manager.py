import json
from typing import List, Dict, Optional
from prefect import flow, task
from dspygen.utils.dspy_tools import init_dspy
import dspy

class FlowManager:
    def __init__(self):
        self.flows = {}
        init_dspy()

    @task
    def create_flow(self, name: str, description: str, tasks: List[Dict]) -> str:
        """Create a new flow using dspy."""
        flow_definition = self._generate_flow_definition(name, description, tasks)
        self.flows[name] = flow_definition
        return f"Flow '{name}' created successfully."

    @task
    def read_flow(self, name: str) -> Optional[Dict]:
        """Retrieve a flow by name."""
        return self.flows.get(name)

    @task
    def update_flow(self, name: str, description: str = None, tasks: List[Dict] = None) -> str:
        """Update an existing flow."""
        if name not in self.flows:
            return f"Flow '{name}' not found."
        
        flow_definition = self.flows[name]
        if description:
            flow_definition['description'] = description
        if tasks:
            flow_definition['tasks'] = tasks
        
        self.flows[name] = flow_definition
        return f"Flow '{name}' updated successfully."

    @task
    def delete_flow(self, name: str) -> str:
        """Delete a flow by name."""
        if name in self.flows:
            del self.flows[name]
            return f"Flow '{name}' deleted successfully."
        return f"Flow '{name}' not found."

    @task
    def list_flows(self) -> List[str]:
        """List all available flows."""
        return list(self.flows.keys())

    def _generate_flow_definition(self, name: str, description: str, tasks: List[Dict]) -> Dict:
        """Generate a flow definition using dspy."""
        class FlowGenerator(dspy.Module):
            def forward(self, name: str, description: str, tasks: List[Dict]):
                pred = dspy.Predict("name, description, tasks -> flow_definition")
                result = pred(name=name, description=description, tasks=json.dumps(tasks))
                return json.loads(result.flow_definition)

        generator = FlowGenerator()
        return generator(name, description, tasks)

@flow
def flow_manager_operations():
    manager = FlowManager()

    # Example usage
    create_result = manager.create_flow(
        "example_flow",
        "An example flow",
        [{"name": "task1", "description": "First task"}, {"name": "task2", "description": "Second task"}]
    )
    print(create_result)

    read_result = manager.read_flow("example_flow")
    print("Read result:", read_result)

    update_result = manager.update_flow(
        "example_flow",
        description="Updated example flow",
        tasks=[{"name": "task1", "description": "Updated first task"}]
    )
    print(update_result)

    list_result = manager.list_flows()
    print("Available flows:", list_result)

    delete_result = manager.delete_flow("example_flow")
    print(delete_result)

if __name__ == "__main__":
    flow_manager_operations()