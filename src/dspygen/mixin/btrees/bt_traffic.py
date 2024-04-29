import py_trees
import time

class TrafficLightSequence(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(TrafficLightSequence, self).__init__(name)
        self.red_duration = 5
        self.yellow_duration = 2
        self.green_duration = 5

    def update(self):
        print("Red light")
        time.sleep(self.red_duration)
        print("Yellow light")
        time.sleep(self.yellow_duration)
        print("Green light")
        time.sleep(self.green_duration)
        return py_trees.common.Status.SUCCESS

def create_tree():
    root = py_trees.composites.Sequence("Traffic Light Sequence", memory=False)
    traffic_light = TrafficLightSequence("Traffic Light")
    root.add_child(traffic_light)
    return root

def main():
    py_trees.logging.level = py_trees.logging.Level.DEBUG
    tree = create_tree()
    print("Created tree")
    while True:
        tree.tick_once()

if __name__ == "__main__":
    main()