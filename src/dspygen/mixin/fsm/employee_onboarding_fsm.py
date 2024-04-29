
from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class EmployeeOnboardingFSMState(Enum):
    START = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()


class EmployeeOnboardingFSM(FSMMixin):
    def __init__(self):
        super().setup_fsm(EmployeeOnboardingFSMState)
        # Initialize state-specific attributes if any

    @trigger(
        source=EmployeeOnboardingFSMState.START,
        dest=EmployeeOnboardingFSMState.IN_PROGRESS,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def start_onboarding(self):
        print("Transitioning from START to IN_PROGRESS")
        
    @trigger(
        source=EmployeeOnboardingFSMState.IN_PROGRESS,
        dest=EmployeeOnboardingFSMState.COMPLETED,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def complete_onboarding(self):
        print("Transitioning from IN_PROGRESS to COMPLETED")
        
    @trigger(
        source=EmployeeOnboardingFSMState.COMPLETED,
        dest=EmployeeOnboardingFSMState.START,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None
    )
    def cancel_onboarding(self):
        print("Transitioning from COMPLETED to START")
        


def main():
    """Main function"""
    fsm = EmployeeOnboardingFSM()
    fsm.start_onboarding()  # Transition from START to IN_PROGRESS
    fsm.complete_onboarding()  # Transition from IN_PROGRESS to COMPLETED
    fsm.cancel_onboarding()  # Transition from COMPLETED to START
    assert fsm.state == EmployeeOnboardingFSMState.START.name  # Verify final state


if __name__ == '__main__':
    main()    