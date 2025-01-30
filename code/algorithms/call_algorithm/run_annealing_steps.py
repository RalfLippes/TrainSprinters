import time
import pandas as pd
import copy
import matplotlib.pyplot as plt
from code.classes.oplossing_class import Solution
from code.algorithms.annealing_steps import create_solution_annealing

def annealing_steps_with_time_limit(time_limit, min_trains, max_trains, original_connection_dict,
    station_dictionary, possible_directions, full_connection_dict,
    max_duration, max_connections, temperature, cooling_rate, total_connections):
    """
    Runs the annealing steps algorithm for a given amount of time. Saves and returns
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
        for trajectory_amount in range(min_trains, max_trains + 1):
            iteration += 1
            needed_connections_dict = copy.deepcopy(original_connection_dict)

            # create a solution
            new_solution = create_solution_annealing(station_dictionary,
                original_connection_dict, possible_directions, full_connection_dict,
                max_duration, max_connections, trajectory_amount)

            # calculate score and append to list
            current_score = new_solution.calculate_solution_score(original_connection_dict,
                total_connections)
            scores.append(current_score)

            # keep track of best solution
            if current_score > best_score:
                best_solution = new_solution
                best_score = current_score
                best_iteration = iteration

    return best_score, best_iteration, best_solution, scores

def plot_outcomes_annealing_steps(scores, national = False):
    """
    Creates histogram of the scores that were found in the annealing_steps_with_time_limit
    function. Saves it to data/output folder.
    """
    # create a histogram
    plt.hist(scores, bins = 'auto', color = 'blue', edgecolor = 'black')

    # add labels and title
    plt.title('Histogram of Scores')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.xlim(0, 10000)

    # save plot under correct name
    if national == True:
        plt.savefig('data/output/annealing_steps_histogram_national.png')
    else:
        plt.savefig('data/output/annealing_steps_histogram_holland.png')

def handle_annealing_steps(args, possible_directions, full_connection_dict, original_connection_dict,
    station_dictionary, max_connections, temperature, cooling_rate, min_trains, max_trains,
    max_duration, plot_title, total_connections):
    """
    Runs the annealing steps algorithm for a given time and saves the results
    in a csv file and a plot.
    """
    # save best scores, best iteration, best solution and all scores
    best_score, best_iteration, best_solution, scores = annealing_steps_with_time_limit(
        args.time, min_trains, max_trains, original_connection_dict, station_dictionary,
        possible_directions, full_connection_dict, max_duration,
        max_connections, temperature, cooling_rate, total_connections)

    # create a dataframe from the scores
    dataframe = best_solution.create_dataframe_from_solution(original_connection_dict,
        total_connections)

    # save the dataframe to a csv file under the right name
    if args.holland_nationaal == 'holland':
        dataframe.to_csv("data/output/annealing_steps_best_solution_holland.csv")
    else:
        dataframe.to_csv("data/output/annealing_steps_best_solution_national.csv")

    # plot if necessary
    if args.plot_scores:
        plot_outcomes_annealing_steps(
            scores, national = args.holland_nationaal == "nationaal")

    # simulate solution if necessary
    if args.simulate:
        best_solution.simulate_solution(station_dictionary, max_duration)

    print(f"The best iteration was iteration number {best_iteration}")
