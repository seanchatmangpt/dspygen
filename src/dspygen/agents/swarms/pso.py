from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
import random
import math


class ParticleState(Enum):
    INITIALIZING = auto()
    EVALUATING = auto()
    UPDATING = auto()
    CHECKING_TERMINATION = auto()
    TERMINATED = auto()


class Particle(FSMMixin):
    def __init__(self, dim, fitness_function):
        super().__init__()
        self.setup_fsm(state_enum=ParticleState, initial=ParticleState.INITIALIZING)
        self.position = [random.uniform(-10, 10) for _ in range(dim)]
        self.velocity = [random.uniform(-1, 1) for _ in range(dim)]
        self.best_position = list(self.position)
        self.best_fitness = float('inf')
        self.fitness_function = fitness_function

    @trigger(source=ParticleState.INITIALIZING, dest=ParticleState.EVALUATING)
    def initialize(self):
        print("Initializing particle.")

    @trigger(source=ParticleState.EVALUATING, dest=ParticleState.UPDATING)
    def evaluate(self):
        fitness = self.fitness_function(self.position)
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_position = list(self.position)
        print(f"Evaluating particle. Fitness: {fitness}")

    @trigger(source=ParticleState.UPDATING, dest=ParticleState.CHECKING_TERMINATION)
    def update(self, global_best_position, inertia=0.5, cognitive=1.5, social=1.5):
        for i in range(len(self.position)):
            r1 = random.random()
            r2 = random.random()
            cognitive_velocity = cognitive * r1 * (self.best_position[i] - self.position[i])
            social_velocity = social * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = inertia * self.velocity[i] + cognitive_velocity + social_velocity
            self.position[i] += self.velocity[i]
        print("Updating particle position and velocity.")

    @trigger(source=ParticleState.CHECKING_TERMINATION, dest=[ParticleState.TERMINATED, ParticleState.EVALUATING])
    def check_termination(self, iteration, max_iterations):
        if iteration >= max_iterations:
            print("Termination condition met.")
            return ParticleState.TERMINATED
        else:
            print("Continuing to next iteration.")
            return ParticleState.EVALUATING


def fitness_function(position):
    return sum(x ** 2 for x in position)  # Example fitness function: Sphere function


def main():
    dim = 2  # Dimensionality of the problem
    num_particles = 5  # Number of particles in the swarm
    max_iterations = 100  # Maximum number of iterations

    particles = [Particle(dim, fitness_function) for _ in range(num_particles)]
    global_best_position = [random.uniform(-10, 10) for _ in range(dim)]
    global_best_fitness = float('inf')

    for iteration in range(max_iterations):
        for particle in particles:
            particle.initialize()
            particle.evaluate()
            if particle.best_fitness < global_best_fitness:
                global_best_fitness = particle.best_fitness
                global_best_position = list(particle.best_position)
            particle.update(global_best_position)
            next_state = particle.check_termination(iteration, max_iterations)
            if next_state == ParticleState.TERMINATED:
                break
            else:
                particle.to_state(next_state)

    print("Optimization completed.")
    print(f"Best position: {global_best_position}")
    print(f"Best fitness: {global_best_fitness}")


if __name__ == '__main__':
    main()
