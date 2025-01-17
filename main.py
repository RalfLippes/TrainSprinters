from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.visualisation.plot_distribution import plot_distribution, prepare_data_baseline
from code.algorithms.greedy import generate_trajectory, create_better_trajectories
from code.algorithms.baseline import choose_random_connections, create_trajectories
from code.algorithms.three_deep_algorithm import n_deep_algorithm, create_deep_trajectories
from code.algorithms.simulated_annealing import load_station_location_data, annealing_cost_function, find_nearest_connection, create_simulated_annealing_trajectory, create_dataframe_annealing
from code.other_functions.create_connection_dict import create_connections
from code.algorithms.call_algorithm.run_n_deep_algorithm import run_n_deep_algorithm
from code.algorithms.call_algorithm.call_simulated_annaeling import run_simulated_annaeling
import copy
import random
import numpy as np
import pandas as pd

if __name__ == "__main__":

    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)


    # TEST THE SIMULATE_ANNEALING ALGORITHM
    # ----------------------------

    # set parameters
    penalty_weight = 0.01
    max_duration = 120
    trajectory_amount = 4
    max_connections = 24

    # load data
    #

    best_dataframe = run_simulated_annaeling(penalty_weight, max_duration, max_connections,
        trajectory_amount, 1000)
    print(best_dataframe)
    create_map(best_dataframe, "data/Noord_Holland/StationsHolland.csv")

    best_dataframe.to_csv("data/output.csv", index=False)

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
