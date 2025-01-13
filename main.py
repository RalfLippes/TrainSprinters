from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.algorithms.random_start_random_choice import generate_trajectory, create_better_trajectories
from code.algorithms.baseline import choose_random_connections, create_trajectories
import copy
import random

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
        for j in range(100):

            # make dataframe with trajectories according to the random algorithm
            dataframe = create_trajectories(7, choose_random_connections, full_connection_dict, original_connection_dict, full_connection_dict, possible_directions)
            #print(dataframe)

            # test baseline algorithm
            needed_connections = copy.deepcopy(original_connection_dict)
            dataframe2, connection_number  = create_better_trajectories(i, generate_trajectory, full_connection_dict, original_connection_dict, needed_connections, full_connection_dict, possible_directions)
            # print(dataframe2)
            # print(connection_number)
            if connection_number == 28:
                total_connections += 1
                connections_list.append(dataframe2)

        print(f' total = {total_connections} with {i} amount of trajectories')
        print(connections_list)

    # get statistics from random samples of solutions
    for i in range(4,8):
        score = []
        connections = []
        duration = []
        for j in range(100):
            current_df = create_trajectories(i, choose_random_connections, full_connection_dict, original_connection_dict, full_connection_dict, possible_directions)
            score.append(current_df['stations'].iloc[-1])
            connections.append()
        print(f"average score for {i} trajectories is {sum(score) / 100}")

    create_map(dataframe2, "data/Noord_Holland/StationsHolland.csv")
