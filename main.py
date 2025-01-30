from code.algorithms.load_data import get_possible_directions, create_connections, load_station_objects, set_parameters
from code.algorithms.argparser import create_arg_parser
from code.algorithms.call_algorithm.run_simulated_annealing import handle_simulated_annealing
from code.algorithms.call_algorithm.run_hill_climber import handle_hill_climber
from code.algorithms.call_algorithm.run_annealing_steps import handle_annealing_steps
from code.algorithms.call_algorithm.run_greedy import handle_greedy
from code.algorithms.call_algorithm.run_n_deep import handle_n_deep
from code.algorithms.call_algorithm.run_baseline import handle_baseline
from code.algorithms.finding_temperature import find_best_temp_and_cooling
from code.algorithms.baseline import create_trajectories, choose_random_connections
from code.algorithms.hill_climber import find_best_iterations
import random
import argparse
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # set a seed for the randomizations
    random.seed(42)

    # arg parser
    args = create_arg_parser().parse_args()

    # load required data and set parameters dependent on parsed arguments
    try:
        (possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections, temperature,
            cooling_rate, min_trains, max_trains, iterations, depth, max_duration, plot_title,
            penalty_weight, temperature_values, cooling_rate_values, experiment_iterations, first_round_iterations
        ) = set_parameters(args.holland_nationaal, "data/Nationaal/ConnectiesNationaal.csv",
            "data/Nationaal/StationsNationaal.csv", "data/Noord_Holland/ConnectiesHolland.csv",
            "data/Noord_Holland/StationsHolland.csv")
    except Exception:
        print("-------------------------------------------------------------")
        print("Please carefully look at the README file to see how to run main")
        print("-------------------------------------------------------------")

    # run baseline
    if args.run_algorithm.lower() == 'baseline':
        handle_baseline(args, possible_directions, full_connection_dict,
            original_connection_dict, total_connections, min_trains, max_trains,
            max_duration, plot_title, max_connections, station_dictionary)

    # run simulated annealing
    if args.run_algorithm.lower() == 'simulated_annealing':
        handle_simulated_annealing(args, possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections, temperature,
            cooling_rate, min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight)

    # run hill climber
    if args.run_algorithm.lower() == 'hill_climber':
        handle_hill_climber(args, possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections,
            min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight, args.start_algorithm, args.creating_algorithm, first_round_iterations = None)

    if args.run_algorithm.lower() == 'hill_climber2':
        handle_hill_climber(args, possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections,
            min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight, args.start_algorithm, args.creating_algorithm, first_round_iterations)

    # run greedy
    if args.run_algorithm.lower() == 'greedy':
        handle_greedy(args, possible_directions, full_connection_dict, original_connection_dict,
            total_connections, min_trains, max_trains, max_duration, plot_title, station_dictionary)

    # run annealing steps
    if args.run_algorithm.lower() == 'annealing_steps':
        handle_annealing_steps(args, possible_directions, full_connection_dict,
            original_connection_dict, station_dictionary, max_connections, temperature,
            cooling_rate, min_trains, max_trains, max_duration, plot_title,
            total_connections)

    # run n deep algorithm
    if args.run_algorithm.lower() == 'n_deep':
        handle_n_deep(args, depth, iterations, min_trains, max_trains, full_connection_dict,
            original_connection_dict, possible_directions, total_connections, station_dictionary)

    # find best cooling rate and temperature
    if args.run_algorithm.lower() == 'temp_cool':
        find_best_temp_and_cooling(full_connection_dict, possible_directions,
            original_connection_dict, station_dictionary, max_duration, max_connections, min_trains,
            max_trains, total_connections, iterations, penalty_weight, temperature_values,
            cooling_rate_values)

    # find best number of iterations for hill climber
    if args.run_algorithm.lower() == 'find_iteration':
        trajectory_amount = random.randint(min_trains, max_trains)
        solution = create_trajectories(trajectory_amount, full_connection_dict,
            possible_directions, max_connections, max_duration)
        for i in range(min_trains, max_trains + 1):
            scores = find_best_iterations(solution, choose_random_connections, full_connection_dict,
                possible_directions, max_connections, trajectory_amount, experiment_iterations,
                original_connection_dict, max_duration, total_connections)
            iterations = list(range(1, len(scores) + 1))

            # create a plot of scores vs iteration
            plt.plot(iterations, scores, linestyle='-', label='High Scores')
        plt.title('High Scores vs Iterations')
        plt.xlabel('Iteration Number')
        plt.ylabel('High Score')
        plt.xlim(0, len(scores))

        plt.show()
