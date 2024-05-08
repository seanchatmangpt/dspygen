from abc import ABC, abstractmethod


class IDaprClientAdapter(ABC):
    """ Interface for adapting the Dapr client operations. """

    @abstractmethod
    def start_workflow(self, workflow_component, workflow_name, input):
        pass

    @abstractmethod
    def get_workflow(self, instance_id, workflow_component):
        pass

    @abstractmethod
    def register_workflow(self, workflow):
        pass

    @abstractmethod
    def register_activity(self, activity):
        pass

    @abstractmethod
    def raise_workflow_event(self, instance_id, workflow_component, event_name, event_data):
        pass
