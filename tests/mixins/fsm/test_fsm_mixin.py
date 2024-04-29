from enum import Enum, auto

import pytest
from transitions import MachineError

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger, state_transition_possibilities


class LightState(Enum):
    """ Enum for the states of a traffic light. """
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class TrafficLight(FSMMixin):
    def __init__(self):
        super().setup_fsm(LightState)

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

    assert tl.state == LightState.RED.name


def test_possibilities():
    """Main function"""
    tl = TrafficLight()
    tl.slow_down()  # Transition from GREEN to YELLOW

    poss = state_transition_possibilities(tl)

    assert poss == ['RED']


def test_traffic_light_transitions(capfd):
    tl = TrafficLight()
    assert tl.state == LightState.GREEN.name  # Verify initial state is GREEN

    # Transition from GREEN to YELLOW
    tl.slow_down()
    captured = capfd.readouterr()
    assert "Transition from GREEN initiated." in captured.out
    assert "Light turned yellow!" in captured.out
    assert tl.state == LightState.YELLOW.name  # Verify state after transition

    # Transition from YELLOW to RED
    tl.stop()
    captured = capfd.readouterr()
    assert "Light turned red!" in captured.out
    assert "Red light celebration!" in captured.out
    assert tl.state == LightState.RED.name  # Verify state after transition

    # Transition from RED to GREEN
    tl.go()
    captured = capfd.readouterr()
    assert "Light turned green!" in captured.out
    assert tl.state == LightState.GREEN.name  # Verify state after transition back to GREEN


def test_invalid_transitions(capfd):
    tl = TrafficLight()
    # Starting at GREEN
    assert tl.state == LightState.GREEN.name

    # Invalid transition: GREEN to RED
    with pytest.raises(MachineError) as excinfo:
        tl.stop()
    assert "Can\'t trigger event stop from state GREEN" in str(excinfo.value)
    captured = capfd.readouterr()
    assert "Light turned red!" not in captured.out
    assert tl.state == LightState.GREEN.name

    # Proceed to YELLOW
    tl.slow_down()
    captured = capfd.readouterr()
    assert "Light turned yellow!" in captured.out

    # Invalid transition: YELLOW to GREEN
    with pytest.raises(MachineError) as excinfo:
        tl.go()
    assert "Can\'t trigger event go from state YELLOW" in str(excinfo.value)
    captured = capfd.readouterr()
    assert "Light turned green!" not in captured.out
    assert tl.state == LightState.YELLOW.name

    # Proceed to RED
    tl.stop()
    captured = capfd.readouterr()
    assert "Light turned red!" in captured.out

    # Invalid transition: RED to YELLOW
    with pytest.raises(MachineError) as excinfo:
        tl.slow_down()
    assert "Can\'t trigger event slow_down from state RED" in str(excinfo.value)
    captured = capfd.readouterr()
    assert "Light turned yellow!" not in captured.out
    assert tl.state == LightState.RED.name

    # Return to GREEN
    tl.go()
    captured = capfd.readouterr()
    assert "Light turned green!" in captured.out
