from enum import Enum, auto
import random
from dspygen.utils.fsm_mixin import FSMMixin, trigger


class SuperheroState(Enum):
    ASLEEP = auto()
    HANGING_OUT = auto()
    HUNGRY = auto()
    SWEATY = auto()
    SAVING_THE_WORLD = auto()


class NarcolepticSuperhero(FSMMixin):
    def __init__(self, name):
        self.name = name
        self.kittens_rescued = 0
        super().setup_fsm(SuperheroState, SuperheroState.ASLEEP)

    @trigger(source=SuperheroState.ASLEEP, dest=SuperheroState.HANGING_OUT)
    def wake_up(self):
        print(f"{self.name} woke up and is ready to hang out.")

    @trigger(source=SuperheroState.HANGING_OUT, dest=SuperheroState.HUNGRY)
    def work_out(self):
        print(f"{self.name} is now hungry after working out.")

    @trigger(source=SuperheroState.HUNGRY, dest=SuperheroState.HANGING_OUT)
    def eat(self):
        print(f"{self.name} is hanging out after eating.")

    @trigger(source='*', dest=SuperheroState.SAVING_THE_WORLD, before='change_into_super_secret_costume')
    def distress_call(self):
        print(f"{self.name} is off to save the world.")

    @trigger(source=SuperheroState.SAVING_THE_WORLD, dest=SuperheroState.SWEATY, after='update_journal')
    def complete_mission(self):
        print(f"{self.name} has completed the mission and is now sweaty.")

    @trigger(source=SuperheroState.SWEATY, dest=SuperheroState.ASLEEP, conditions=['is_exhausted'])
    def clean_up_exhausted(self):
        print(f"{self.name} is too exhausted and going back to sleep.")

    @trigger(source=SuperheroState.SWEATY, dest=SuperheroState.HANGING_OUT)
    def clean_up(self):
        print(f"{self.name} cleaned up and is hanging out again.")

    @trigger(source='*', dest=SuperheroState.ASLEEP)
    def nap(self):
        print(f"{self.name} has taken a nap.")

    def update_journal(self):
        self.kittens_rescued += 1
        print(f"Updated journal: {self.kittens_rescued} kittens rescued.")

    def is_exhausted(self):
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print(f"{self.name} is changing into their super-secret costume.")


def test_narcoleptic_superhero():
    hero = NarcolepticSuperhero("SleepyMan")
    hero.wake_up()
    hero.work_out()
    hero.eat()
    hero.distress_call()
    hero.complete_mission()
    if hero.is_exhausted():
        hero.clean_up_exhausted()
    else:
        hero.clean_up()
    hero.nap()

    assert hero.state == SuperheroState.ASLEEP.name
