from code.other_functions.load_data import get_possible_directions, create_connections, load_station_objects, set_parameters
from code.other_functions.argparser import create_arg_parser
from code.algorithms.call_algorithm.run_simulated_annealing import handle_simulated_annealing
from code.algorithms.call_algorithm.run_hill_climber import handle_hill_climber
from code.algorithms.call_algorithm.run_annealing_steps import handle_annealing_steps
from code.algorithms.call_algorithm.run_greedy import handle_greedy
from code.algorithms.call_algorithm.run_n_deep import handle_n_deep
from code.algorithms.call_algorithm.run_baseline import handle_baseline
from code.algorithms.finding_temperature import find_best_temp_and_cooling
import random
import argparse

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
            penalty_weight, temperature_values, cooling_rate_values
        ) = set_parameters(args.holland_nationaal, "data/Nationaal/ConnectiesNationaal.csv",
            "data/Nationaal/StationsNationaal.csv", "data/Noord_Holland/ConnectiesHolland.csv",
            "data/Noord_Holland/StationsHolland.csv")
    except Exception:
        print("-------------------------------------------------------------")
        print("Please run main in format 'python main.py [holland/nationaal] [algorithm] [time in seconds] [plot? yes/no]'")
        print("-------------------------------------------------------------")

    # run baseline
    if args.run_algorithm.lower() == 'baseline':
        handle_baseline(args, possible_directions, full_connection_dict,
            original_connection_dict, total_connections, min_trains, max_trains,
            max_duration, plot_title, max_connections)

    # run simulated annealing
    if args.run_algorithm.lower() == 'simulated_annealing':
        handle_simulated_annealing(args, possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections, temperature,
            cooling_rate, min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight)

    # run hill climber
    if args.run_algorithm.lower() == 'hill_climber':
        handle_hill_climber(args, possible_directions, full_connection_dict, original_connection_dict,
            station_dictionary, total_connections, max_connections, temperature,
            cooling_rate, min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight)

    # run greedy
    if args.run_algorithm.lower() == 'greedy':
        handle_greedy(args, possible_directions, full_connection_dict, original_connection_dict,
            total_connections, min_trains, max_trains, max_duration, plot_title)

    # run annealing steps
    if args.run_algorithm.lower() == 'annealing_steps':
        handle_annealing_steps(args, possible_directions, full_connection_dict,
            original_connection_dict, station_dictionary, max_connections, temperature,
            cooling_rate, min_trains, max_trains, max_duration, plot_title, penalty_weight,
            total_connections)

    if args.run_algorithm.lower() == 'n_deep':
        handle_n_deep(args, depth, iterations, min_trains, max_trains, full_connection_dict,
            original_connection_dict, possible_directions, total_connections)

    if args.run_algorithm.lower() == 'temp_cool':
        find_best_temp_and_cooling(full_connection_dict, possible_directions,
            original_connection_dict, station_dictionary, max_duration, max_connections, min_trains,
            max_trains, total_connections, iterations, penalty_weight, temperature_values,
            cooling_rate_values)


        # # get a list of iteration numbers
        # iterations = list(range(1, len(high_scores) + 1))
        #
        # # create a plot of high scores vs iteration
        # plt.plot(iterations, high_scores, linestyle='-', color='b', label='High Scores')
        # plt.title('High Scores vs Iterations')
        # plt.xlabel('Iteration Number')
        # plt.ylabel('High Score')
        # plt.xlim(0, len(high_scores))
        #
        # plt.show()
