from enum import Enum, auto

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class TrafficLightState(Enum):
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class TrafficLight(FSMMixin):
    def __init__(self):
        super().setup_fsm(TrafficLightState)
        # Initialize state-specific attributes if any

    @trigger(
        source=TrafficLightState.GREEN,
        dest=TrafficLightState.YELLOW,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def slow_down(self):
        print("Transitioning from green to yellow")

    @trigger(
        source=TrafficLightState.YELLOW,
        dest=TrafficLightState.RED,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def stop(self):
        print("Transitioning from yellow to red")

    @trigger(
        source=TrafficLightState.RED,
        dest=TrafficLightState.GREEN,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def go(self):
        print("Transitioning from red to green")

    def log_transition(self):
        print("Logging transition.")

    def celebrate_red(self):
        print("Celebrating red light!")


def main():
    """Main function"""
    tl = TrafficLight()
    tl.slow_down()  # Transition from GREEN to YELLOW
    tl.stop()  # Transition from YELLOW to RED

    assert tl.state == TrafficLightState.RED.name


if __name__ == "__main__":
    main()
