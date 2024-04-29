from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class MatterState(Enum):
    SOLID = auto()
    LIQUID = auto()
    GAS = auto()
    PLASMA = auto()


class Matter(FSMMixin):
    def __init__(self, initial=MatterState.SOLID):
        super().setup_fsm(MatterState, initial=initial)

    @trigger(source=MatterState.SOLID, dest=MatterState.LIQUID)
    def melt(self):
        print("Melted from solid to liquid.")

    @trigger(source=MatterState.LIQUID, dest=MatterState.GAS)
    def evaporate(self):
        print("Evaporated from liquid to gas.")

    @trigger(source=MatterState.SOLID, dest=MatterState.GAS)
    def sublimate(self):
        print("Sublimated from solid to gas.")

    @trigger(source=MatterState.GAS, dest=MatterState.PLASMA)
    def ionize(self):
        print("Ionized from gas to plasma.")

    @trigger(source=[MatterState.SOLID, MatterState.GAS, MatterState.PLASMA], dest=MatterState.LIQUID)
    def to_liquid(self):
        print("Transitioned to liquid.")

    @trigger(source=[MatterState.SOLID, MatterState.GAS, MatterState.PLASMA, MatterState.LIQUID],
             dest=None,
             after='change_shape')
    def internal(self):
        print("Internal transition within the state.")

    @trigger(source=[MatterState.LIQUID, MatterState.GAS, MatterState.PLASMA], dest='=', after='change_shape')
    def touch(self):
        print("Touched while in a non-solid state.")

    def change_shape(self):
        print("Changing shape due to touch.")




def test_matter():
    matter = Matter()
    matter.melt()  # Solid to liquid
    print(matter.state)  # Outputs: LIQUID
    matter.evaporate()  # Liquid to gas
    print(matter.state)  # Outputs: GAS
    matter.to_liquid()  # Any state to liquid
    print(matter.state)  # Outputs: LIQUID
    assert matter.state == MatterState.LIQUID.name, "State should be LIQUID."
