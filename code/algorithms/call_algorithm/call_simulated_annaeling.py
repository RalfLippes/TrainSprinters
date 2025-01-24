from code.algorithms.annealing_steps import load_station_location_data, annealing_cost_function, find_nearest_connection, create_annealing_steps_trajectory, create_dataframe_annealing
from code.other_functions.load_data import get_possible_directions
from code.other_functions.create_connection_dict import create_connections
import copy

def run_simulated_annaeling(penalty_weight, max_duration, max_connections, trajectory_amount,
    iterations, original_connection_dict, station_locations, possible_directions,
    full_connection_dict):
    best_dataframe = None
    highest_score = 0
    total_highest_score = 0
    total_best_dataframe = None

    for a in range(iterations):
        new_needed_connections_dict = copy.deepcopy(original_connection_dict)
        trajectory_list = []
        # create certain amount of trajectories
        for i in range(trajectory_amount):
            trajectories_test, new_needed_connections_dict = create_simulated_annealing_trajectory(station_locations,
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
