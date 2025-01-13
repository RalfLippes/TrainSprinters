from data.Noord_Holland.load_data import get_possible_directions
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.visualisation.representation import create_map
from code.algorithms.random_start_random_choice import choose_random_connections, create_trajectories

def create_connections(data):
    """
    Calculates the quality of the itinerary. Outputs a score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)

if __name__ == "__main__":


    return connections_dictionary

if __name__ == "__main__":
    # make variables with possible directions, and dictionaries with connection objects
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)

    # make dataframe with trajectories according to the random algorithm
    dataframe = create_trajectories(7, choose_random_connections, full_connection_dict, original_connection_dict, full_connection_dict, possible_directions)
    print(dataframe)

    # create map of trajectories that have been created
    create_map(dataframe, "data/Noord_Holland/StationsHolland.csv")
