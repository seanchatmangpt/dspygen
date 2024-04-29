import py_trees
import pytest
import time


class TrafficLightBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name, colour):
        super(TrafficLightBehaviour, self).__init__(name)
        self.colour = colour

    def initialise(self):
        self.logger.debug("%s.initialise()" % self.name)

    def update(self):
        py_trees.blackboard.Blackboard().set(self.name, self.colour)
        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        self.logger.debug("%s.terminate()[%s->%s]" % (self.name, self.status, new_status))



def create_traffic_light_tree():
    # Adding the memory parameter and setting it to False
    root = py_trees.composites.Sequence("Traffic Light Sequence", memory=False)

    green = TrafficLightBehaviour(name="Green Light", colour="GREEN")
    yellow = TrafficLightBehaviour(name="Yellow Light", colour="YELLOW")
    red = TrafficLightBehaviour(name="Red Light", colour="RED")

    root.add_children([green, yellow, red])
    return root


def test_traffic_light_sequence():
    traffic_light_tree = create_traffic_light_tree()

    # Using a shared blackboard for all traffic light states
    blackboard = py_trees.blackboard.Client(name="TrafficLightTest")
    blackboard.register_key(key="Green Light", access=py_trees.common.Access.WRITE)
    blackboard.register_key(key="Yellow Light", access=py_trees.common.Access.WRITE)
    blackboard.register_key(key="Red Light", access=py_trees.common.Access.WRITE)

    # Reset blackboard state
    blackboard.set("Green Light", None)
    blackboard.set("Yellow Light", None)
    blackboard.set("Red Light", None)

    # Tick the tree and check the states
    traffic_light_tree.tick_once()  # Tick to Green
    assert blackboard.get("Green Light") == "GREEN", "Failed at GREEN"

    traffic_light_tree.tick_once()  # Tick to Yellow
    assert blackboard.get("Yellow Light") == "YELLOW", "Failed at YELLOW"

    traffic_light_tree.tick_once()  # Tick to Red
    assert blackboard.get("Red Light") == "RED", "Failed at RED"

    # Check if the sequence restarts correctly after completion
    traffic_light_tree.tick_once()  # This should reset to Green
    assert blackboard.get("Green Light") == "GREEN", "Did not restart correctly to GREEN"

