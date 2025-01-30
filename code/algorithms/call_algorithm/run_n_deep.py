import time
import copy
import matplotlib.pyplot as plt
from code.classes.oplossing_class import Solution
from code.algorithms.n_deep import create_deep_trajectories, n_deep_algorithm

def n_deep_with_time_limit(time_limit, iterations, depth, min_trains, max_trains,
    full_connection_dict, original_connection_dict, possible_directions, total_connections):
    """
    Finds a solution by looking for connections n deep. By checking the score that
    would be gained by that path, decides which route is the best. Does this for given
    amount of time. Returns best solution, best score and list of all scores.
    """
    best_score = 0
    best_iteration = 0
    best_solution = None
    scores = []
    iteration = 0
    start_time = time.time()

    # Keep looping while within the time limit
    while time.time() - start_time < time_limit:
        for trajectory_amount in range(min_trains, max_trains + 1):
            iteration += 1

            # Deep copy the original connection dictionary
            needed_connections_dict = copy.deepcopy(original_connection_dict)

            # Create trajectories using the n_deep algorithm
            final_solution = create_deep_trajectories(
                trajectory_amount=trajectory_amount,
                connection_algorithm=n_deep_algorithm,
                full_connection_dict=full_connection_dict,
                original_connection_dict=original_connection_dict,
                needed_connections_dict=needed_connections_dict,
                possible_directions=possible_directions,
                depth=depth,
                total_connections=total_connections)

            # Track scores
            current_score = final_solution.calculate_solution_score(original_connection_dict, total_connections)

            scores.append(current_score)

            # Track the best solution
            if current_score > best_score:
                best_score = current_score
                best_iteration = iteration
                best_solution = final_solution

    return best_score, best_iteration, best_solution, scores


def plot_outcomes_n_deep(scores, national = False):
    """
    Creates histogram of the scores that were found in the n_deep_with_time_limit
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
        plt.savefig('data/output/n_deep_histogram_national.png')
    else:
        plt.savefig('data/output/n_deep_histogram_holland.png')


def handle_n_deep(args, depth, iterations, min_trains, max_trains, full_connection_dict,
    original_connection_dict, possible_directions, total_connections, station_dictionary):
    """
    Handles the n_deep algorithm using the structure of annealing steps.
    """
    # Run the n_deep algorithm with the specified time limit
    best_score, best_iteration, best_solution, scores = n_deep_with_time_limit(
        time_limit=args.time,
        depth=depth,
        iterations=iterations,
        min_trains=min_trains,
        max_trains=max_trains,
        full_connection_dict=full_connection_dict,
        original_connection_dict=original_connection_dict,
        possible_directions=possible_directions,
        total_connections=total_connections)

    dataframe = best_solution.create_dataframe_from_solution(original_connection_dict, total_connections)

    # Save the results
    if args.holland_nationaal == 'holland':
        dataframe.to_csv("data/output/n_deep_best_solution_holland.csv", index=False)
    else:
        dataframe.to_csv("data/output/n_deep_best_solution_national.csv", index=False)

    # Optionally plot the scores
    if args.plot_scores:
        plot_outcomes_n_deep(
            scores, national = args.holland_nationaal == "nationaal")

    # simulate solution if necessary
    if args.simulate:
        best_solution.simulate_solution(station_dictionary, max_duration)

    print(f"The best iteration was iteration number {best_iteration}")
