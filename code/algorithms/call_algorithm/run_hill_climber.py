import time
import pandas as pd
import copy
import matplotlib.pyplot as plt
from code.classes.oplossing_class import Solution
from code.algorithms.annealing_steps import create_annealing_steps_trajectory
from code.algorithms.hill_climber import hill_climber
from code.algorithms.greedy import generate_trajectory
from code.algorithms.baseline import choose_random_connections

def create_start_trajectory(start_algorithm, a, station_locations,
    needed_connections_dict, possible_directions, full_connection_dict,
    penalty_weight, max_duration, max_connections):

    trajectories = Solution()

    if start_algorithm == "annealing_steps":
        for traj in range(a):
            new_trajectory, needed_connections_dict = create_annealing_steps_trajectory(station_locations,
                needed_connections_dict, possible_directions, full_connection_dict,
                penalty_weight, max_duration, max_connections)
            trajectories.add_trajectory(new_trajectory)

    elif start_algorithm == "greedy":
        for traj in range(a):

            new_trajectory, needed_connections_dict = generate_trajectory(full_connection_dict, possible_directions,
                needed_connections_dict, max_duration)
            trajectories.add_trajectory(new_trajectory)

    elif start_algorithm == "baseline":
        for traj in range(a):
            new_trajectory = choose_random_connections(connection_object_dict, possible_connections_dict,
                max_connections, max_duration)
            trajectories.add_trajectory(new_trajectory)


    return trajectories



def hill_climber_with_time_limit(time_limit, min_trains, max_trains,
    original_connection_dict, station_locations, possible_directions, full_connection_dict,
    penalty_weight, max_duration, max_connections,
    iterations, total_connections, start_algorithm):
    """
    Runs the hill climber algorithm for a given amount of time. Saves and returns
    the best score, the iteration number of the best score and the best solution.
    Also saves every score in a list and return these.
    """
    best_score = 0
    iteration = 0
    best_iteration = 0
    best_solution = None
    scores = []
    high_scores = []
    start_time = time.time()

    # keep looping while in time limit
    while time.time() - start_time < time_limit:
        # run algorithm once for every possible amount of trajectories
        for a in range(min_trains, max_trains + 1):
            iteration += 1
            needed_connections_dict = copy.deepcopy(original_connection_dict)

            trajectories = create_start_trajectory(start_algorithm, a, station_locations,
                needed_connections_dict, possible_directions, full_connection_dict,
                penalty_weight, max_duration, max_connections)


            # apply simulated annealing
            try_out = hill_climber(trajectories, choose_random_connections,
                full_connection_dict, possible_directions, max_connections, a,
                iterations, original_connection_dict, max_duration, total_connections)

            # calculate score and append to list
            current_score = try_out.calculate_solution_score(original_connection_dict, total_connections)
            scores.append(current_score)

            # keep track of best solution
            if current_score > best_score:
                best_solution = try_out
                best_score = current_score
                best_iteration = iteration

            high_scores.append(best_score)

    return best_score, best_iteration, best_solution, scores, high_scores

def plot_outcomes_hill_climber(scores, high_scores, national = False):
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
        plt.savefig('data/output/hill_climber_histogram_national.png')
    else:
        plt.savefig('data/output/hill_climber_histogram_holland.png')

def handle_hill_climber(args, possible_directions, full_connection_dict, original_connection_dict,
    station_locations, total_connections, max_connections, min_trains, max_trains, iterations, max_duration, plot_title,
    penalty_weight, start_algorithm = "baseline"):
    """Runs the hill climber algorithm for a given time and saves the results."""
    # save best scores, best iteration, best solution and all scores
    best_score, best_iteration, best_solution, scores, high_scores = hill_climber_with_time_limit(
        args.time, min_trains, max_trains, original_connection_dict, station_locations,
        possible_directions, full_connection_dict, penalty_weight, max_duration,
        max_connections, iterations, total_connections, start_algorithm)

    # create a dataframe from the scores
    dataframe = best_solution.create_dataframe_from_solution(original_connection_dict,
        total_connections)

    # save the dataframe to a csv file under the right name
    if args.holland_nationaal == 'holland':
        dataframe.to_csv("data/output/hill_climber_best_solution_holland.csv", index = False)
    else:
        dataframe.to_csv("data/output/hill_climber_best_solution_national.csv", index = False)

    # plot if necessary
    if args.plot_scores:
        plot_outcomes_hill_climber(
            scores, high_scores, national = args.holland_nationaal == "nationaal")

    print(f"The best iteration was iteration number {best_iteration}")
