import dspy
from pydantic import BaseModel, Field

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.utils.dspy_tools import init_ol


class FSMTriggerModule(dspy.Module):
    """FSMTriggerModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, prompt, possible_triggers):
        pred = dspy.Predict("prompt, possible_triggers -> chosen_trigger")
        self.output = pred(prompt=prompt, possible_triggers=possible_triggers).chosen_trigger
        return self.output


def fsm_trigger_call(prompt, possible_triggers):
    fsm_trigger = FSMTriggerModule()
    return fsm_trigger.forward(prompt=prompt, possible_triggers=possible_triggers)


from transitions import Machine
from transitions.core import State
import inspect

from enum import Enum, auto

class ElevatorState(Enum):
    """ Enum for the states of an elevator. """
    IDLE = auto()
    MOVING_UP = auto()
    MOVING_DOWN = auto()
    MAINTENANCE = auto()

class Elevator(FSMMixin):
    def __init__(self):
        super().setup_fsm(ElevatorState, initial=ElevatorState.IDLE)

    @trigger(source=ElevatorState.IDLE, dest=ElevatorState.MOVING_UP, after="print_possible_triggers")
    def move_up(self):
        print("Elevator is moving up.")

    @trigger(source=ElevatorState.IDLE, dest=ElevatorState.MOVING_DOWN, after="print_possible_triggers")
    def move_down(self):
        print("Elevator is moving down.")

    @trigger(source=[ElevatorState.MOVING_UP, ElevatorState.MOVING_DOWN], dest=ElevatorState.IDLE, after="print_possible_triggers")
    def stop(self):
        print("Elevator has stopped.")

    @trigger(source='*', dest=ElevatorState.MAINTENANCE, after="print_possible_triggers")
    def maintenance_mode(self):
        print("Elevator is in maintenance mode.")

    @trigger(source=ElevatorState.MAINTENANCE, dest=ElevatorState.IDLE, after="print_possible_triggers")
    def maintenance_complete(self):
        print("Elevator maintenance is complete and back to idle.")

    def print_possible_triggers(self):
        print(f"Possible triggers: {self.possible_triggers()}")


class ChosenTrigger(BaseModel):
    reasoning: str = Field(..., description="The reasoning behind the chosen trigger.")
    chosen_trigger: str = Field(..., description="The chosen trigger based on the command.")


def main():
    init_ol()

    # Initialize the elevator and the FSM trigger module
    elevator = Elevator()
    print(f"Initial state: {elevator.state}")

    # Simulate voice commands as input to the elevator
    voice_commands = [
        "move up",
        "stop",
        "move down",
        "maintenance mode",
        "maintenance complete"
        "idle",
    ]

    for command in voice_commands:
        # Fetch possible triggers based on the elevator's current state
        possible_triggers = ",".join(elevator.possible_triggers())

        # Determine the best trigger for the given voice command
        from dspygen.modules.json_module import json_call

        chosen_trigger = json_call(ChosenTrigger, text=f"{command} {possible_triggers}").chosen_trigger

        # Execute the chosen trigger if it matches the voice command
        if chosen_trigger and hasattr(elevator, chosen_trigger):
            action = getattr(elevator, chosen_trigger)
            action()
            print(f"State after '{command}': {elevator.state}")
        else:
            print(f"No valid action for command '{command}' in state {elevator.state}")


if __name__ == "__main__":
    main()
