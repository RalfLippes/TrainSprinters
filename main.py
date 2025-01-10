from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.algorithms.random_start_random_choice import choose_random_connections, create_trajectories

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
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)
    dataframe = create_trajectories(3, choose_random_connections, full_connection_dict, original_connection_dict, full_connection_dict, possible_directions)
    print(dataframe)
