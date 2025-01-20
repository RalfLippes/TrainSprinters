from code.other_functions.load_data import get_possible_directions, create_connections, load_station_objects, set_parameters
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.classes.oplossing_class import Solution
from code.visualisation.representation import create_map, plot_trajectories
from code.visualisation.plot_distribution import plot_distribution, prepare_data_baseline
from code.algorithms.greedy import generate_trajectory, create_better_trajectories
from code.algorithms.baseline import choose_random_connections, create_trajectories
from code.algorithms.three_deep_algorithm import n_deep_algorithm, create_deep_trajectories
from code.algorithms.annealing_steps import load_station_location_data, annealing_cost_function, find_nearest_connection, create_annealing_steps_trajectory, create_dataframe_annealing
from code.algorithms.simulated_annealing import simulated_annealing
import copy
import random
import numpy as np
import pandas as pd
import argparse

if __name__ == "__main__":

    # arg parser
    parser = argparse.ArgumentParser(description = 'Holland or Nationaal')
    parser.add_argument('holland_nationaal', help = 'Wil je alle data gebruiken of alleen van Noord- en Zuid-Holland?')
    args = parser.parse_args()

    # load the required data dependent on parsed arguments
    try:
        (possible_directions, full_connection_dict, original_connection_dict,
            station_locations, total_connections, max_connections, temperature,
            cooling_rate, min_trains, max_trains, iterations, max_duration
        ) = set_parameters(args.holland_nationaal, "data/Nationaal/ConnectiesNationaal.csv",
            "data/Nationaal/StationsNationaal.csv", "data/Noord_Holland/ConnectiesHolland.csv",
            "data/Noord_Holland/StationsHolland.csv")
    except Exception:
        print("-------------------------------------------------------------")
        print("Please run main in format 'python main.py [holland/nationaal]'")
        print("-------------------------------------------------------------")


    # TEST THE SIMULATE_ANNEALING ALGORITHM
    # ----------------------------
    # do a few simulated annealings
    best_score = 0
    best_solution = None
    best_temperature = None
    best_cooling_rate = None
    penalty_weight = 0.1

    for x in range(10):
        for a in range(min_trains, max_trains + 1):
            trajectories = Solution()
            needed_connections_dict = copy.deepcopy(original_connection_dict)
            for b in range(a):
                new_trajectory, needed_connections_dict = create_annealing_steps_trajectory(station_locations,
                    needed_connections_dict, possible_directions, full_connection_dict,
                    penalty_weight, max_duration, max_connections)
                trajectories.add_trajectory(new_trajectory)
            try_out = simulated_annealing(trajectories, choose_random_connections,
                full_connection_dict, possible_directions, max_connections, a,
                temperature, cooling_rate, iterations, original_connection_dict, max_duration)
            if try_out.calculate_solution_score(original_connection_dict, total_connections) > best_score:
                best_solution = try_out
                print(f"{b + 1} trajectories of {max_trains} max")

    df = best_solution.create_dataframe_from_solution(original_connection_dict, total_connections)
    print(df)
    plot_trajectories(df, "data/Noord_Holland/StationsHolland.csv")

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

    # TEST THE ANNEALING_STEPS ALGORITHM
    # ----------------------------

    # set parameters
    # penalty_weight = 0.01
    # max_duration = 120
    # trajectory_amount = 4
    # max_connections = 100
    # iterations = 100
    #

    # ----------------------------


    # TEST THE N_DEEP_ALGORITHM ALGORITHM
    # ----------------------------

    # run_n_deep_algorithm(100, 3, loading_popup=False)

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
    #
    # score_7_trajectories, connections_7_trajectories, dataframe_7_trajectories = prepare_data_baseline(
    #     100, full_connection_dict, original_connection_dict, possible_directions,
    #     choose_random_connections, False)
    #
    # # set correct amount of bins
    # bin_edges = np.linspace(0, 28, 29)
    #
    # # plot the values
    # plot_distribution(total_score, 30, "Average distribution of Scores" , "Score",
    #     "code/visualisation/total_score_distribution")
    # plot_distribution(total_connections, bin_edges, "Average distribution of Connections",
    #     "Connections", "code/visualisation/total_connections_distribution")
    # plot_distribution(score_7_trajectories, 30, "Average distribution of Scores with 7 Trajectories" ,
    #     "Score", "code/visualisation/7_trajectories_score_distribution")
    # plot_distribution(connections_7_trajectories, bin_edges,
    #     "Average distribution of unique connections with 7 Trajectories" , "Connections",
    #     "code/visualisation/7_trajectories_connections_distribution")
    #
    # # display the dataframe
    # baseline_dataframe.to_csv('code/visualisation/trajectories_statistics.csv', index=False)

    # create_map(dataframe2, "data/Noord_Holland/StationsHolland.csv")

    # ----------------------------
