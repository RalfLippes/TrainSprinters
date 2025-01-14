from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.visualisation.plot_distribution import plot_distribution, prepare_data_baseline
from code.algorithms.greedy import generate_trajectory, create_better_trajectories
from code.algorithms.baseline import choose_random_connections, create_trajectories
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


if __name__ == "__main__":

    # make variables with possible directions, and dictionaries with connection objects
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)

    for i in range(4, 8):

        total_connections = 0
        connections_list = []
        for j in range(1):

            # test baseline algorithm
            needed_connections = copy.deepcopy(original_connection_dict)
            dataframe2, connection_number  = create_better_trajectories(i, generate_trajectory, full_connection_dict, original_connection_dict, needed_connections, full_connection_dict, possible_directions)
            # print(dataframe2)
            # print(connection_number)
            if connection_number == 28:
                total_connections += 1
                connections_list.append(dataframe2)

            dataframe2.to_csv("output.csv", index=False)

        print(f' total = {total_connections} with {i} amount of trajectories')
        print(connections_list)

    print(dataframe2)

    # find average values from the baseline algorithms
    total_score, total_connections, baseline_dataframe = prepare_data_baseline(100,
        full_connection_dict, original_connection_dict, possible_directions,
        choose_random_connections)

    score_7_trajectories, connections_7_trajectories, dataframe_7_trajectories = prepare_data_baseline(
        100, full_connection_dict, original_connection_dict, possible_directions,
        choose_random_connections, False)

    # set correct amount of bins
    bin_edges = np.linspace(0, 28, 29)

    # plot the values
    plot_distribution(total_score, 30, "Average distribution of Scores" , "Score",
        "code/visualisation/total_score_distribution")
    plot_distribution(total_connections, bin_edges, "Average distribution of Connections",
        "Connections", "code/visualisation/total_connections_distribution")
    plot_distribution(score_7_trajectories, 30, "Average distribution of Scores with 7 Trajectories" ,
        "Score", "code/visualisation/7_trajectories_score_distribution")
    plot_distribution(connections_7_trajectories, bin_edges,
        "Average distribution of unique connections with 7 Trajectories" , "Connections",
        "code/visualisation/7_trajectories_connections_distribution")

    # display the dataframe
    baseline_dataframe.to_csv('code/visualisation/trajectories_statistics.csv', index=False)

    # create_map(dataframe2, "data/Noord_Holland/StationsHolland.csv")
