from enum import Enum, auto

from transitions import MachineError

from dspygen.utils.fsm_mixin import FSMMixin, trigger, state_transition_possibilities


class LightState(Enum):
    """ Enum for the states of a traffic light. """
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class TrafficLight(FSMMixin):
    def __init__(self):
        super().setup_fsm(LightState, LightState.GREEN)

    @trigger(source=LightState.GREEN, dest=LightState.YELLOW, before='log_transition')
    def slow_down(self):
        print("Light turned yellow!")

    @trigger(source=LightState.YELLOW, dest=LightState.RED, after='celebrate_red')
    def stop(self):
        print("Light turned red!")

    @trigger(source=LightState.RED, dest=LightState.GREEN)
    def go(self):
        print("Light turned green!")

    def log_transition(self):
        print(f"Transition from {self.state} initiated.")

    def celebrate_red(self):
        print("Red light celebration!")


def test_fsm():
    """Main function"""
    tl = TrafficLight()
    tl.slow_down()  # Transition from GREEN to YELLOW
    tl.stop()  # Transition from YELLOW to RED

    assert tl.state == LightState.RED


def test_possibilities():
    """Main function"""
    tl = TrafficLight()
    tl.slow_down()  # Transition from GREEN to YELLOW

    poss = state_transition_possibilities(tl)

    assert poss == ['RED']


def test_fsm():
    """Main function"""
    tl = TrafficLight()
    try:
        tl.slow_down()  # Transition from GREEN to YELLOW
        print("Successfully transitioned from GREEN to YELLOW.")
    except MachineError as e:
        print(f"Failed to transition from GREEN to YELLOW: {e}")

    try:
        tl.stop()  # Transition from YELLOW to RED
        print("Successfully transitioned from YELLOW to RED.")
    except MachineError as e:
        print(f"Failed to transition from YELLOW to RED: {e}")

    try:
        tl.slow_down()  # Attempt transition from RED to YELLOW (not defined, should raise error)
        print("Successfully transitioned from RED to YELLOW.")
    except MachineError as e:
        print(f"Failed to transition from RED to YELLOW: {e}")

    print("Final state:", tl.state)
