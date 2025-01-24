from code.other_functions.load_data import get_possible_directions, create_connections, load_station_objects, set_parameters
from code.other_functions.argparser import create_arg_parser
from code.algorithms.call_algorithm.run_simulated_annealing import handle_simulated_annealing
from code.algorithms.call_algorithm.run_annealing_steps import handle_annealing_steps
from code.algorithms.call_algorithm.run_greedy import handle_greedy
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
            cooling_rate, min_trains, max_trains, iterations, max_duration, plot_title,
            penalty_weight
        ) = set_parameters(args.holland_nationaal, "data/Nationaal/ConnectiesNationaal.csv",
            "data/Nationaal/StationsNationaal.csv", "data/Noord_Holland/ConnectiesHolland.csv",
            "data/Noord_Holland/StationsHolland.csv")
    except Exception:
        print("-------------------------------------------------------------")
        print("Please run main in format 'python main.py [holland/nationaal] [algorithm] [time in seconds] [plot? yes/no]'")
        print("-------------------------------------------------------------")

    # run simulated annealing
    if args.run_algorithm.lower() == 'simulated_annealing':
        handle_simulated_annealing(args, possible_directions, full_connection_dict, original_connection_dict,
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

    # ----------------------------

    # TEST THE BASELINE ALGORITHM ON NATIONAL DATA
    # ----------------------------

    # total_score, total_connection_list, baseline_dataframe = prepare_data_baseline(89, 1000,
    #     full_connection_dict, original_connection_dict,
    #     possible_directions, choose_random_connections, max_connections, max_duration,
    #     min_trains, max_trains)
    #
    # print(baseline_dataframe)
    #
    # plot_distribution(baseline_dataframe, 50, 'Title', 'Score', 'Baseline national plot')
    #
    # total_score, total_connection_list, baseline_dataframe = prepare_data_baseline(89, 1000,
    #     full_connection_dict, original_connection_dict,
    #     possible_directions, choose_random_connections, max_connections, max_duration,
    #     20, 20)
    #
    # plot_distribution(baseline_dataframe, 50, 'Title', 'Score', 'Baseline national plot')

    # ----------------------------


    # TEST THE N_DEEP_ALGORITHM ALGORITHM
    # ----------------------------
    # random.seed()
    # run_n_deep_algorithm(100, 14, loading_popup=False)

    # ----------------------------

    # TEST THE BASE_LINE ALGORITHM
    # ----------------------------

    # for i in range(4, 8):
    #
    #     total_connections = 0
    #     connections_list = []
    #     for j in range(1000):
    #
    #         # test baseline algorithm
    #         needed_connections = copy.deepcopy(original_connection_dict)
    #         dataframe2, connection_number  = create_better_trajectories(i, generate_trajectory, full_connection_dict, original_connection_dict, needed_connections, full_connection_dict, possible_directions)
    #         # print(dataframe2)
    #         # print(connection_number)
    #         if connection_number == 28:
    #             total_connections += 1
    #             connections_list.append(dataframe2)
    #
    #         dataframe2.to_csv("data/output.csv", index=False)
    #
    #     print(f' total = {total_connections} with {i} amount of trajectories')
    #     print(connections_list)
    #
    # print(dataframe2)

    # ----------------------------


    # FIND AVERAGE VALUES FROM THE BASELINE ALGORITHM
    # ----------------------------

    # total_score, total_connections, baseline_dataframe = prepare_data_baseline(100,
    #     full_connection_dict, original_connection_dict, possible_directions,
    #     choose_random_connections)

    # score_7_trajectories, connections_7_trajectories, dataframe_7_trajectories = prepare_data_baseline(
    #     28, 100, full_connection_dict, original_connection_dict, possible_directions,
    #     choose_random_connections, max_connections, max_duration, min_trains, max_trains)
    #
    # # set correct amount of bins
    # bin_edges = np.linspace(0, 28, 29)
    #
    # # plot the values for 7 trajectories
    # plot_distribution(score_7_trajectories, 10000, "Average distribution of Scores with 7 Trajectories" ,
    #     "Score", "7_trajectories_score_distribution")
    # plot_distribution(connections_7_trajectories, bin_edges,
    #     "Average distribution of unique connections with 7 Trajectories" , "Connections",
    #     "7_trajectories_connections_distribution")

    # # plot the values for all trajectory amounts
    # plot_distribution(total_score, 30, "Average distribution of Scores" , "Score",
    #     "code/visualisation/total_score_distribution")
    # plot_distribution(total_connections, bin_edges, "Average distribution of Connections",
    #     "Connections", "code/visualisation/total_connections_distribution")

    # # display the dataframe
    # baseline_dataframe.to_csv('code/visualisation/trajectories_statistics.csv', index=False)
    #
    # create_map(dataframe2, "data/Noord_Holland/StationsHolland.csv")

    # ----------------------------
