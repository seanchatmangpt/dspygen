from transitions import Machine
from enum import Enum


class MatterState(Enum):
    SOLID = 'solid'
    LIQUID = 'liquid'
    GAS = 'gas'
    PLASMA = 'plasma'


class Matter(Machine):
    def __init__(self, **kwargs):
        # States are defined using the MatterState enum
        states = list(MatterState)
        Machine.__init__(self, states=states, initial=MatterState.SOLID)

        # Initialize the state machine

        # Define transitions using the state machine
        self.add_transition('melt', MatterState.SOLID, MatterState.LIQUID)
        self.add_transition('evaporate', MatterState.LIQUID, MatterState.GAS)
        self.add_transition('sublimate', MatterState.SOLID, MatterState.GAS)
        self.add_transition('ionize', MatterState.GAS, MatterState.PLASMA)

        # Add multi-state transitions
        self.add_transition('transmogrify', [MatterState.SOLID, MatterState.LIQUID, MatterState.GAS],
                            MatterState.PLASMA)
        self.add_transition('transmogrify', MatterState.PLASMA, MatterState.SOLID)
        self.add_transition('to_liquid', '*', MatterState.LIQUID)

        # Add reflexive transitions
        self.add_transition('touch', [MatterState.LIQUID, MatterState.GAS, MatterState.PLASMA], '=',
                            after='change_shape')

        # Add internal transitions
        self.add_transition('internal', [MatterState.LIQUID, MatterState.GAS], None, after='change_shape')

    def melt(self):
        # Placeholder for the melt method
        print(f"Melted from {self.state} to liquid.")
        self.to_liquid()

    def change_shape(self):
        # Placeholder for the change shape method
        print(f"Changing shape in {self.state} state.")


if __name__ == "__main__":
    matter = Matter()

    # Testing transitions
    assert matter.state == MatterState.SOLID
    matter.melt()
    assert matter.state == MatterState.LIQUID
    matter.evaporate()
    assert matter.state == MatterState.GAS
    matter.ionize()
    assert matter.state == MatterState.PLASMA
    matter.transmogrify()
    assert matter.state == MatterState.SOLID

    matter.to_liquid()
    assert matter.state == MatterState.LIQUID

    # Reflexive transition with action
    matter.touch()
    assert matter.state == MatterState.LIQUID

    # Internal transition, should not change state but run 'change_shape'
    matter.internal()
    assert matter.state == MatterState.LIQUID

    print("All transitions completed successfully.")
