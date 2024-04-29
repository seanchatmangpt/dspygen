import py_trees
import time


class BTMixin:
    def __init__(self):
        self.root = None  # Root of the behavior tree
        self.board = py_trees.blackboard.Client(name="BTMixinClient")  # Shared blackboard
        self.setup_tree()  # Setup the tree structure
        self._register_keys()  # Auto-register keys

    def setup_tree(self):
        """
        This method should be overridden in subclasses to define the actual
        structure and composition of the behavior tree.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")

    def _register_keys(self):
        """
        Automatically register blackboard keys based on the requirements of the behaviors in the tree.
        This method uses the iterate method to find all behaviors.
        """
        keys = set()
        if self.root:
            for behaviour in self.root.iterate():
                if hasattr(behaviour, 'blackboard_keys'):
                    keys.update(behaviour.blackboard_keys)

        for key in keys:
            self.board.register_key(key=key, access=py_trees.common.Access.WRITE)

    def tick_tree(self):
        """
        Execute a single tick of the behavior tree.
        """
        self.root.tick_once()

    def print_tree(self):
        """
        Print a simple textual representation of the tree.
        """
        print(py_trees.display.ascii_tree(self.root))


class SetTrafficLightColor(py_trees.behaviour.Behaviour):
    def __init__(self, color, name="Set Color"):
        super().__init__(name)
        self.board = None
        self.color = color
        self.blackboard_keys = {color}  # Set of keys this behavior will use

    def initialise(self):
        self.logger.debug(f"{self.name}.initialise()")

    def update(self):
        self.board = py_trees.blackboard.Blackboard()
        self.board.set(self.color, True)
        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        self.logger.debug(f"{self.name}.terminate()[{self.status}->{new_status}]")
        self.board.set(self.color, False)


class TrafficLightControl(BTMixin):
    def setup_tree(self):
        """
        Setup the behavior tree for controlling a traffic light.
        """
        green = SetTrafficLightColor("GREEN", name="Green Light")
        yellow = SetTrafficLightColor("YELLOW", name="Yellow Light")
        red = SetTrafficLightColor("RED", name="Red Light")

        # Sequence ensures that the lights cycle in a fixed order
        sequence = py_trees.composites.Sequence("Traffic Light Sequence", memory=False)
        sequence.add_children([green, yellow, red])
        self.root = sequence  # Set the sequence as the root of the tree


def main():
    traffic_control = TrafficLightControl()
    traffic_control.print_tree()  # Print the structure of the tree

    # No need to initialize or register keys here; use the one from BTMixin
    blackboard = traffic_control.board  # Direct reference to the shared blackboard client

    # Simulate running the traffic light system
    for _ in range(10):  # Run enough cycles to see the lights cycle through multiple times
        traffic_control.tick_tree()
        print("Current Light State:")
        active_lights = []
        for color in ["GREEN", "YELLOW", "RED"]:
            # Directly access the board from the control instance
            if blackboard.get(color):
                active_lights.append(f"{color} light is on")
        if active_lights:
            print("\n".join(active_lights))
        else:
            print("No lights are on")
        print("-" * 20)
        time.sleep(1)  # Simulate time passing


if __name__ == "__main__":
    main()
