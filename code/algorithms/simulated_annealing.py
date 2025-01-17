import random
from code.algorithms.annealing_steps import annealing_cost_function
from code.algorithms.baseline import choose_random_connections

def simulated_annealing(trajectories):
    """
    Takes a list of trajectory objects. Removes 1 trajectory and makes a new one.
    Calculates score of current and new trajectory and uses acceptance function
    to decide if new step is accepted. Repeats until temperature is 0.
    """

    # remove random trajectory from list
    trajectories.pop(random.randrange(len(trajectories)))

    # create new random trajectory
