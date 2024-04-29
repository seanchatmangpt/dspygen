from transitions.extensions import HierarchicalMachine
import logging

class HierarchicalFSMMixin:
    def setup_hsm(self, states, transitions, initial=None, ignore_invalid_triggers=True):
        self.machine = HierarchicalMachine(
            model=self, states=states, transitions=transitions,
            initial=initial, ignore_invalid_triggers=ignore_invalid_triggers
        )
        # self.machine.on_transition(self.log_transition)

    def log_transition(self, transition):
        logging.info(f"Transitioning from {transition.source} to {transition.dest} via {transition.event.name}")

class CoffeeMachine(HierarchicalFSMMixin):
    def __init__(self):
        states = [
            'idle', 'brewing',
            {'name': 'maintenance', 'children': [
                {'name': 'cleaning', 'initial': 'starting'},
                {'name': 'refilling', 'initial': 'starting'}
            ], 'initial': 'cleaning'}
        ]
        transitions = [
            {'trigger': 'brew', 'source': 'idle', 'dest': 'brewing'},
            {'trigger': 'finish_brewing', 'source': 'brewing', 'dest': 'idle'},
            {'trigger': 'maintain', 'source': '*', 'dest': 'maintenance'},
            {'trigger': 'finish_maintenance', 'source': 'maintenance_*', 'dest': 'idle'},
            {'trigger': 'clean', 'source': 'maintenance', 'dest': 'maintenance_cleaning'},
            {'trigger': 'refill', 'source': 'maintenance', 'dest': 'maintenance_refilling'}
        ]
        self.setup_hsm(states, transitions, initial='idle')

    def brew(self):
        print("Brewing coffee...")

    def finish_brewing(self):
        print("Coffee ready!")

    def maintain(self):
        print("Entering maintenance mode...")

    def finish_maintenance(self):
        print("Maintenance done, ready to brew!")

    def clean(self):
        print("Cleaning the machine...")

    def refill(self):
        print("Refilling ingredients...")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Example usage
coffee_machine = CoffeeMachine()
coffee_machine.brew()  # Transition from idle to brewing
coffee_machine.maintain()  # Entering maintenance mode...
coffee_machine.maintain()  # Entering maintenance mode...
coffee_machine.finish_brewing()  # Transition back to idle
coffee_machine.maintain()  # Transition to maintenance (and automatically to cleaning due to initial state setting)
coffee_machine.clean()  # Will actually not change the state since it's already in cleaning
coffee_machine.finish_maintenance()  # Will transition from maintenance (cleaning) back to idle
coffee_machine.refill()  # No effect because the machine is in idle, not in maintenance
