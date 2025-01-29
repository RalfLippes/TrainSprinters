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
    """
    Creates a starting solution to feed into hill climber. Uses annealing steps,
    greedy or random algorithm to create this.
    """
    trajectories = Solution()

    # create solution based on parsed start algorithm
    if start_algorithm == "annealing_steps":
        for traj in range(a):
            new_trajectory, needed_connections_dict = create_annealing_steps_trajectory(station_locations,
                needed_connections_dict, possible_directions, full_connection_dict,
                max_duration, max_connections)
            trajectories.add_trajectory(new_trajectory)

    elif start_algorithm == "greedy":
        for traj in range(a):
            new_trajectory, needed_connections_dict = generate_trajectory(full_connection_dict, possible_directions,
                needed_connections_dict, max_duration)
            trajectories.add_trajectory(new_trajectory)

    elif start_algorithm == "baseline":
        for traj in range(a):
            new_trajectory = choose_random_connections(full_connection_dict, possible_directions,
                max_connections, max_duration)
            trajectories.add_trajectory(new_trajectory)

    return trajectories

def hill_climber_with_time_limit(time_limit, min_trains, max_trains,
    original_connection_dict, station_locations, possible_directions, full_connection_dict,
    penalty_weight, max_duration, max_connections,
    iterations, total_connections, start_algorithm, creating_algorithm):
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


            # apply hill climber
            try_out = hill_climber(trajectories, choose_random_connections,
                full_connection_dict, possible_directions, max_connections, a,
                iterations, original_connection_dict, max_duration, total_connections,
                creating_algorithm, station_locations)

            # calculate score and append to list
            current_score = try_out.calculate_solution_score(original_connection_dict, total_connections)
            scores.append(current_score)

            # keep track of best solution and score
            if current_score > best_score:
                best_solution = try_out
                best_score = current_score
                best_iteration = iteration

            high_scores.append(best_score)

    return best_score, best_iteration, best_solution, scores, high_scores

def hill_climber2_with_time_limit(time_limit, min_trains, max_trains,
    original_connection_dict, station_locations, possible_directions, full_connection_dict,
    penalty_weight, max_duration, max_connections,
    iterations, total_connections, start_algorithm, creating_algorithm, first_round_iterations):
    """
    Runs the hill climber2 algorithm for a given amount of time. Saves and returns
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
        best_solution_so_far = None
        best_score_so_far = 0
        iteration += 1

        for i in range(10):

            # run algorithm once for every possible amount of trajectories
            for a in range(min_trains, max_trains + 1):
                needed_connections_dict = copy.deepcopy(original_connection_dict)

                trajectories = create_start_trajectory(start_algorithm, a, station_locations,
                    needed_connections_dict, possible_directions, full_connection_dict,
                    penalty_weight, max_duration, max_connections)

                # apply hill climber
                try_out = hill_climber(trajectories, choose_random_connections,
                    full_connection_dict, possible_directions, max_connections, a,
                    first_round_iterations, original_connection_dict, max_duration, total_connections,
                    creating_algorithm, station_locations)

                # calculate score and append to list
                current_score = try_out.calculate_solution_score(original_connection_dict, total_connections)

                # keep track of best solution
                if current_score > best_score_so_far:
                    best_solution_so_far = try_out
                    best_score_so_far = current_score

        # find amount of trajectories
        trajectory_amount = len(best_solution_so_far.solution)

        # best solution goes through hill climber again
        this_solution = hill_climber(best_solution_so_far, choose_random_connections,
            full_connection_dict, possible_directions, max_connections, trajectory_amount,
            iterations, original_connection_dict, max_duration, total_connections,
            creating_algorithm, station_locations)

        # calculate solution score
        solution_score = this_solution.calculate_solution_score(original_connection_dict, total_connections)
        scores.append(solution_score)

        # save best solution and score
        if solution_score > best_score:
            best_solution = this_solution
            best_score = solution_score
            best_iteration = iteration

    return best_score, best_iteration, best_solution, scores, high_scores

def plot_outcomes_hill_climber(args, scores, high_scores, start_algorithm, creating_algorithm, national = False):
    """
    Creates histogram of the scores that were found in the hill_climber_with_time_limit
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
        plt.savefig(f"data/output/{args.run_algorithm}_histogram_national_{start_algorithm}_{creating_algorithm}.png")
    else:
        plt.savefig(f"data/output/{args.run_algorithm}_histogram_holland_{start_algorithm}_{creating_algorithm}.png")

def handle_hill_climber(args, possible_directions, full_connection_dict, original_connection_dict,
    station_locations, total_connections, max_connections, min_trains, max_trains, iterations, max_duration, plot_title,
    penalty_weight, start_algorithm, creating_algorithm, first_round_iterations):
    """Runs the hill climber algorithm for a given time and saves the results."""
    # check if we want to run hill climber or hill climber2
    if args.run_algorithm == 'hill_climber':
        # run hill climber for the given time
        best_score, best_iteration, best_solution, scores, high_scores = hill_climber_with_time_limit(
            args.time, min_trains, max_trains, original_connection_dict, station_locations,
            possible_directions, full_connection_dict, penalty_weight, max_duration,
            max_connections, iterations, total_connections, start_algorithm, creating_algorithm)

    elif args.run_algorithm == 'hill_climber2':
        best_score, best_iteration, best_solution, scores, high_scores = hill_climber2_with_time_limit(
            args.time, min_trains, max_trains, original_connection_dict, station_locations,
            possible_directions, full_connection_dict, penalty_weight, max_duration,
            max_connections, iterations, total_connections, start_algorithm, creating_algorithm,
            first_round_iterations)

    # create a dataframe from the scores
    dataframe = best_solution.create_dataframe_from_solution(original_connection_dict,
        total_connections)

    # save the dataframe to a csv file under the right name
    if args.holland_nationaal == 'holland':
        dataframe.to_csv(f"data/output/{args.run_algorithm}_best_solution_holland_{start_algorithm}_{creating_algorithm}.csv", index = False)
    else:
        dataframe.to_csv(f"data/output/{args.run_algorithm}_best_solution_national_{start_algorithm}_{creating_algorithm}.csv", index = False)

    # plot if necessary
    if args.plot_scores:
        plot_outcomes_hill_climber(
            args, scores, high_scores, start_algorithm, creating_algorithm, national = args.holland_nationaal == "nationaal")

    #simulate the best_solution when necessary
    if args.simulate:
        best_solution.simulate_solution(station_locations, max_duration)

    print(f"The best iteration was iteration number {best_iteration}")
