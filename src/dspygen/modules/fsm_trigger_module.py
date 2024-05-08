import typing

import dspy
from pydantic import BaseModel, Field


if typing.TYPE_CHECKING:
    from dspygen.mixin.fsm.fsm_mixin import FSMMixin


class ChosenTrigger(BaseModel):
    reasoning: str = Field(..., description="Let's think step by step about which trigger to choose.")
    chosen_trigger: str = Field(..., description="The chosen trigger based on the command.")


class FSMTriggerModule(dspy.Module):
    """FSMTriggerModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, prompt: str, fsm: "FSMMixin") -> str:
        # Determine the best trigger for the given voice command
        from dspygen.modules.json_module import json_call
        possible_triggers = "\n".join(fsm.possible_triggers())

        text = (f"```prompt\n{prompt}```\n\n"
                f"Choose from Possible State Transition Triggers based on prompt:\n\n```possible_triggers\n{possible_triggers}\n```\n\n"
                f"You must choose one of the possible triggers to proceed.")

        print(text)

        response = json_call(ChosenTrigger, text=text)

        return response.chosen_trigger


def fsm_trigger_call(prompt, fsm: "FSMMixin", **kwargs):
    fsm_trigger = FSMTriggerModule()
    chosen_trigger = fsm_trigger.forward(prompt=prompt, fsm=fsm)
    if chosen_trigger and hasattr(fsm, chosen_trigger):
        action = getattr(fsm, chosen_trigger)
        action(**kwargs)
    else:
        raise ValueError(f"No valid action for command '{prompt}' in state {fsm.state}")

def main():
    """Main function"""


if __name__ == '__main__':
    main()
