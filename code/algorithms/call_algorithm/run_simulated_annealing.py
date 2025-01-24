import time
import pandas as pd
import copy
import matplotlib.pyplot as plt
from code.classes.oplossing_class import Solution
from code.algorithms.annealing_steps import create_annealing_steps_trajectory
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.baseline import choose_random_connections

def run_with_time_limit(time_limit, min_trains, max_trains, original_connection_dict,
    station_locations, possible_directions, full_connection_dict, penalty_weight,
    max_duration, max_connections, temperature, cooling_rate, iterations, total_connections):
    """
    Runs the simulated annealing algorithm for a given amount of time. Saves and returns
    the best score, the iteration number of the best score and the best solution.
    Also saves every score in a list and return these.
    """
    best_score = 0
    iteration = 0
    best_iteration = 0
    best_solution = None
    scores = []
    start_time = time.time()

    # keep looping while in time limit
    while time.time() - start_time < time_limit:
        # run algorithm once for every possible amount of trajectories
        for a in range(min_trains, max_trains + 1):
            iteration += 1
            trajectories = Solution()
            needed_connections_dict = copy.deepcopy(original_connection_dict)

            # create a solution with annealing steps algorithm
            for b in range(a):
                new_trajectory, needed_connections_dict = create_annealing_steps_trajectory(station_locations,
                    needed_connections_dict, possible_directions, full_connection_dict,
                    penalty_weight, max_duration, max_connections)
                trajectories.add_trajectory(new_trajectory)

            # apply simulated annealing
            try_out = simulated_annealing(trajectories, choose_random_connections,
                full_connection_dict, possible_directions, max_connections, a,
                temperature, cooling_rate, iterations, original_connection_dict, max_duration)

            # calculate score and append to list
            current_score = try_out.calculate_solution_score(original_connection_dict, total_connections)
            scores.append(current_score)

            # keep track of best solution
            if current_score > best_score:
                best_solution = try_out
                best_score = current_score
                best_iteration = iteration

    return best_score, best_iteration, best_solution, scores

def plot_outcomes_simulated_annealing(scores, national = False):
    """
    Creates histogram of the scores that were found in the run_with_time_limit
    function. Saves it to data/output folder.
    """
    # create a histogram
    plt.hist(scores, bins = 'auto', color = 'blue', edgecolor = 'black')

    # add labels and title
    plt.title('Histogram of Scores')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.xlim(0, 10000)
    if national == True:
        plt.savefig('data/output/simulated_annealing_histogram_national.png')
    else:
        plt.savefig('data/output/simulated_annealing_histogram_holland.png')

    # show plot
    plt.show()
