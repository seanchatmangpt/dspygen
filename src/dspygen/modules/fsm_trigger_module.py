import dspy
from pydantic import BaseModel, Field

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.utils.dspy_tools import init_ol


class ChosenTrigger(BaseModel):
    reasoning: str = Field(..., description="Let's think step by step about which trigger to choose.")
    chosen_trigger: str = Field(..., description="The chosen trigger based on the command.")


class FSMTriggerModule(dspy.Module):
    """FSMTriggerModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, prompt: str, fsm: FSMMixin) -> str:
        # Determine the best trigger for the given voice command
        from dspygen.modules.json_module import json_call
        possible_triggers = ",".join(fsm.possible_triggers())

        text = (f"Prompt: {prompt}\n\n"
                f"Choose from Possible State Transition Triggers based on prompt:\n\n{possible_triggers}")

        response = json_call(ChosenTrigger, text=text)

        return response.chosen_trigger


def fsm_trigger_call(prompt, fsm: FSMMixin):
    fsm_trigger = FSMTriggerModule()
    chosen_trigger = fsm_trigger.forward(prompt=prompt, fsm=fsm)
    if chosen_trigger and hasattr(fsm, chosen_trigger):
        action = getattr(fsm, chosen_trigger)
        action()
    else:
        raise ValueError(f"No valid action for command '{prompt}' in state {fsm.state}")


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

    @trigger(source=[ElevatorState.MOVING_UP, ElevatorState.MOVING_DOWN], dest=ElevatorState.IDLE,
             after="print_possible_triggers")
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


def main():
    init_ol(model="llama3")
    # init_ol(model="phi3:instruct")

    # Initialize the elevator and the FSM trigger module
    elevator = Elevator()
    print(f"Initial state: {elevator.state}")

    # Simulate voice commands as input to the elevator
    voice_commands = [
        "Ascend to a higher position.",
        "Halt all current actions.",
        "Descend to a lower position.",
        "Activate maintenance procedures.",
        "Finish maintenance procedures.",
        "Enter a state of rest without deactivation."
    ]

    for command in voice_commands:
        print(f"\nCommand: '{command}'")
        fsm_trigger_call(command, elevator)
        print(f"Current state: {elevator.state}")


if __name__ == "__main__":
    main()
