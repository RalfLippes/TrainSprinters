from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.visualisation.plot_distribution import plot_distribution, prepare_data_baseline
from code.algorithms.greedy import generate_trajectory, create_better_trajectories
from code.algorithms.baseline import choose_random_connections, create_trajectories
from code.algorithms.three_deep_algorithm import n_deep_algorithm, create_deep_trajectories
from code.algorithms.simulated_annealing import load_station_location_data, annealing_cost_function, find_nearest_connection, create_simulated_annealing_trajectory, create_dataframe_annealing
import copy
import random
import numpy as np
import pandas as pd

def create_connections(data):
    """
    reads a csv file and creates Connection objects for every connection listed
    in the file. Returns a dictionary with the name of the connection as the key,
    and the corresponding object as the value.
    """
    connections_dictionary = {}

    # find names of start station, end station and duration of connection
    for index, row in data.iterrows():
        station_1 = row.iloc[0]
        station_2 = row.iloc[1]
        duration = row.iloc[2]

        # initialize Connection object with correct data and add to dictionary
        connections_dictionary[station_1 + "-" + station_2] = Connection(station_1, station_2, duration)

    return connections_dictionary

def test_my_algorithm(penalty_weight, max_duration, max_connections, trajectory_amount,
    iterations):
    best_dataframe = None
    highest_score = 0
    total_highest_score = 0
    total_best_dataframe = None

    for a in range(iterations):
        new_needed_connections_dict = copy.deepcopy(original_connection_dict)
        trajectory_list = []
        # create certain amount of trajectories
        for i in range(trajectory_amount):
            trajectories_test, new_needed_connections_dict = create_simulated_annealing_trajectory(test,
                new_needed_connections_dict, possible_directions,
                full_connection_dict, penalty_weight, max_duration, max_connections)
            trajectory_list.append(trajectories_test)

        # make it into dataframe and print + visualize
        dataframe_test, number_connections = create_dataframe_annealing(trajectory_list, trajectory_amount,
            new_needed_connections_dict, 28)
        if dataframe_test['stations'].iloc[-1] > highest_score:
            highest_score = dataframe_test['stations'].iloc[-1]
            best_dataframe = dataframe_test

    return best_dataframe

def run_n_deep_algorithm(iterations, depth, loading_popup=False):
    # Load data and prepare variables
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)


    avg_scores = {}
    highest_scores = {}
    best_dataframe = []


    for i in range(4, 8):
        total_score = 0  # Initialize total score for the current trajectory amount
        highest_score = float('-inf')  # Initialize the highest score for this trajectory amount

        for j in range(iterations):
            needed_connections_dict = copy.deepcopy(original_connection_dict)
            possible_connections_dict = possible_directions


            dataframe, connections_made = create_deep_trajectories(
                trajectory_amount=i,
                connection_algorithm=n_deep_algorithm,
                full_connection_dict=full_connection_dict,
                original_connection_dict=original_connection_dict,
                needed_connections_dict=needed_connections_dict,
                arg1=full_connection_dict,
                arg2=possible_connections_dict,
                arg3=needed_connections_dict,
                arg4=depth #= Depth,
             )


            score = dataframe.loc[dataframe.index[-1], 'stations']
            total_score += score

            # Update highest score if the current score is higher
            if score > highest_score:
                highest_score = score
                best_dataframe = dataframe

            if loading_popup == True:
                if j % (iterations/10) == 0 and j > 0:
                    print(f"Traject {i}: {j} iteration completed...")

        # Calculate the average score for the current trajectory amount
        avg_scores[i] = total_score / iterations
        highest_scores[i] = highest_score  # Store the highest score for the current trajectory amount


        print(f"Average score for {i} trajectories: {avg_scores[i]}")
        print(f"Highest score for {i} trajectories: {highest_scores[i]}")
    print(best_dataframe)

    best_dataframe.to_csv("output2.csv", index=False)

if __name__ == "__main__":
    # load data
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)

    # set parameters
    penalty_weight = 0.01
    max_duration = 120
    trajectory_amount = 4
    max_connections = 24

    # load data
    test = load_station_location_data("data/Noord_Holland/StationsHolland.csv")

    best_dataframe = test_my_algorithm(penalty_weight, max_duration, max_connections,
        trajectory_amount, 1000)
    print(best_dataframe)
    create_map(best_dataframe, "data/Noord_Holland/StationsHolland.csv")






    # Call the n_deep algorithm
    # run_n_deep_algorithm(100, 3, loading_popup=False)










    # for i in range(4, 8):
    #
    #     total_connections = 0
    #     connections_list = []
    #     for j in range(1):
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
    #         dataframe2.to_csv("output.csv", index=False)
    #
    #     print(f' total = {total_connections} with {i} amount of trajectories')
    #     print(connections_list)
    #
    # print(dataframe2)
    #
    # find average values from the baseline algorithms
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
