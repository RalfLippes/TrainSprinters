#from load_data import get_possible_directions
#from verbinding_class import Connection
#from verbinding_class import Trajectory
#from code.algorithms import random_start_random_choice #choose_random_connections
def calculate_score(connections, trajectory_amount, duration, total_connections = 28):
    """
    Calculates the quality of the itinerary. Outputs a score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)

if __name__ == "__main__":




    # dataframe = create_trajectories(3, choose_random_connections, test_dict, original_dict, test_dict, possible_connections)
    # directions, corrected_df = get_possible_directions("ConnectiesHolland.csv")
    # test_dict = create_connections(corrected_df)
    # test_df = create_trajectories(7, random_connection)
