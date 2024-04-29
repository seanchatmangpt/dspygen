##############################################################################
# Imports
##############################################################################

import py_trees
import py_trees.behaviours
import py_trees.composites
import py_trees.console
import py_trees.display
import py_trees.idioms
from dspygen.mixin.btrees.btree_mixin import BTMixin


class ContextSwitch(py_trees.behaviour.Behaviour):
    """
    An example of a context switching class.

    This class sets (in ``initialise()``)
    and restores a context (in ``terminate()``). Use in parallel with a
    sequence/subtree that does the work while in this context.

    .. attention:: Simply setting a pair of behaviours (set and reset context) on
        either end of a sequence will not suffice for context switching. In the case
        that one of the work behaviours in the sequence fails, the final reset context
        switch will never trigger.
    """

    def __init__(self, name: str = "ContextSwitch"):
        """Initialise with a behaviour name."""
        super(ContextSwitch, self).__init__(name)
        self.feedback_message = "no context"

    def initialise(self) -> None:
        """Backup and set a new context."""
        self.logger.debug("%s.initialise()[switch context]" % (self.__class__.__name__))
        # Some actions that:
        #   1. retrieve the current context from somewhere
        #   2. cache the context internally
        #   3. apply a new context
        self.feedback_message = "new context"

    def update(self) -> py_trees.common.Status:
        """Just returns RUNNING while it waits for other activities to finish."""
        self.logger.debug(
            "%s.update()[RUNNING][%s]"
            % (self.__class__.__name__, self.feedback_message)
        )
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status: py_trees.common.Status) -> None:
        """Restore the context with the previously backed up context."""
        self.logger.debug(
            "%s.terminate()[%s->%s][restore context]"
            % (self.__class__.__name__, self.status, new_status)
        )
        # Some actions that:
        #   1. restore the cached context
        self.feedback_message = "restored context"


##############################################################################
# Behavior Tree Integration
##############################################################################

class MyBehaviorTree(BTMixin):
    def setup_tree(self):
        """
        Overrides the BTMixin setup_tree method to define the specific structure
        of the behavior tree from the example.
        """
        root = py_trees.composites.Parallel(
            name="Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnOne()
        )
        context_switch = ContextSwitch(name="Context")
        sequence = py_trees.composites.Sequence(name="Sequence", memory=True)
        for job in ["Action 1", "Action 2"]:
            success_after_two = py_trees.behaviours.StatusQueue(
                name=job,
                queue=[py_trees.common.Status.RUNNING, py_trees.common.Status.RUNNING],
                eventually=py_trees.common.Status.SUCCESS,
            )
            sequence.add_child(success_after_two)
        root.add_child(context_switch)
        root.add_child(sequence)
        self.root = root  # Assign the constructed tree as the root of the mixin

    def register_keys(self):
        """
        Registers keys on the blackboard used by behaviors in the tree.
        """
        # This demo does not use the blackboard, so this method can be empty or contain relevant keys
        pass

##############################################################################
# Main Execution
##############################################################################

def main():
    """
    Entry point for running the behavior tree with BTMixin.
    """
    tree = MyBehaviorTree()  # Create an instance of the modified tree
    tree.print_tree()  # Print the initial state of the tree

    for i in range(1, 6):
        print("\n--------- Tick {0} ---------\n".format(i))
        tree.tick_tree()  # Perform a tick
        tree.print_tree()  # Print the tree after each tick

##############################################################################
# Running Main
##############################################################################

if __name__ == '__main__':
    main()
