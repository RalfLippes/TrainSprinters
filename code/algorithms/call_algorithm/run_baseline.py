import time
import copy
import matplotlib.pyplot as plt
from code.classes.oplossing_class import Solution
from code.algorithms.baseline import create_trajectories

def baseline_with_time_limit(time_limit, min_trains, max_trains, original_connection_dict,
    possible_directions, full_connection_dict, max_duration, total_connections, max_connections):
    """
    Runs the baseline algorithm for a given amount of time. Saves and returns
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
        for trajectory_amount in range(min_trains, max_trains + 1):
            iteration += 1
            needed_connections_dict = copy.deepcopy(original_connection_dict)

            # run baseline algorithm
            current_solution = create_trajectories(trajectory_amount, full_connection_dict,
                possible_directions, max_connections, max_duration)

            # calculate score and append to list
            current_score = current_solution.calculate_solution_score(original_connection_dict,
                total_connections)
            scores.append(current_score)

            # keep track of best solution
            if current_score > best_score:
                best_solution = current_solution
                best_score = current_score
                best_iteration = iteration

            high_scores.append(best_score)

    return best_score, best_iteration, best_solution, scores, high_scores

def plot_outcomes_baseline(scores, national = False):
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

    # save figure to appropriate file
    if national == True:
        plt.savefig('data/output/baseline_histogram_national.png')
    else:
        plt.savefig('data/output/baseline_histogram_holland.png')

def handle_baseline(args, possible_directions, full_connection_dict, original_connection_dict,
    total_connections, min_trains, max_trains, max_duration, plot_title, max_connections):
    """Runs the baseline algorithm for a given time and saves the results."""
    # save best scores, best iteration, best solution and all scores
    best_score, best_iteration, best_solution, scores, high_scores = baseline_with_time_limit(
        args.time, min_trains, max_trains, original_connection_dict,
        possible_directions, full_connection_dict, max_duration, total_connections,
        max_connections)

    # create a dataframe from the scores
    dataframe = best_solution.create_dataframe_from_solution(original_connection_dict,
        total_connections)

    # save the dataframe to a csv file under the right name
    if args.holland_nationaal == 'holland':
        dataframe.to_csv("data/output/baseline_best_solution_holland.csv", index = False)
    else:
        dataframe.to_csv("data/output/baseline_best_solution_national.csv", index = False)

    # plot if necessary
    if args.plot_scores:
        plot_outcomes_baseline(
            scores, national = args.holland_nationaal == "nationaal")

    if args.simulate:
        best_solution.simulate_solution(station_locations, max_duration)

    print(f"The best iteration was iteration number {best_iteration}")
