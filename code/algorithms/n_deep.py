import random
import pandas as pd
import copy
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.algorithms.calculate_score import calculate_score
from code.classes.oplossing_class import Solution
import random

def calculate_new_score(new_connections_made, current_time):
    """
    Calculates the score based on new connections and time.
    """
    return calculate_score(new_connections_made, 1, current_time)

def get_valid_next_connections(current_station, available_connections, possible_connections, current_time, time_limit=120):
    """
    Retrieves all valid next connections from the current station.
    """
    # find valid connections
    next_stations = possible_connections.get(current_station, [])
    valid_connections = []
    for next_station in next_stations:
        connection_key = f"{current_station}-{next_station}"
        connection = available_connections.get(connection_key)

        if connection is not None and current_time + connection.duration <= time_limit:
            valid_connections.append((connection_key, connection, next_station))
    return valid_connections

def explore_paths(current_station, available_connections, used_connections, needed_connections,
                  possible_connections, current_time, steps_left, steps_without_new_connection=0, max_no_new_steps=8):
    """
    Explores possible routes up to a certain depth. Returns the best score and path.
    Terminates if no new connections are made within a specified number of steps.
    """
    # If steps run out or there are no available connections
    if steps_left == 0 or not available_connections:
        new_connections_made = len(needed_connections) - len(available_connections)
        return calculate_new_score(new_connections_made, current_time), []

    # Terminate if too many steps have passed without new connections
    if steps_without_new_connection >= max_no_new_steps:
        return float('-inf'), []

    path_scores = {}
    valid_connections = get_valid_next_connections(
        current_station, available_connections, possible_connections, current_time)

    for connection_key, connection, next_station in valid_connections:
        # Check if this connection makes a new connection
        is_new_connection = connection_key in needed_connections

        updated_used_connections = used_connections.copy()
        updated_used_connections.add(connection_key)

        updated_available_connections = copy.deepcopy(available_connections)
        updated_available_connections.pop(connection_key)

        # Increment steps_without_new_connection if no new connection is made
        new_steps_without_new_connection = steps_without_new_connection + (0 if is_new_connection else 1)

        # Explore further paths
        future_score, future_path = explore_paths(
            next_station, updated_available_connections, updated_used_connections, needed_connections,
            possible_connections, current_time + connection.duration, steps_left - 1, new_steps_without_new_connection, max_no_new_steps)

        # Add bonus for new connections
        if is_new_connection:
            future_score += 300  # Bonus for new connections

        # Add the new connection in the front of the tuple and set the score
        path_scores[(connection,) + tuple(future_path)] = future_score

    if not path_scores:
        return float('-inf'), []

    best_path = max(path_scores, key=path_scores.get)
    best_score = path_scores[best_path]

    return best_score, list(best_path)

def initialize_route(needed_connections):
    """
    Initializes the route with a random connection from the needed connections.
    """
    first_connection = random.choice(list(needed_connections.values()))
    route = [first_connection]
    total_time = first_connection.duration
    current_station = first_connection.end_station
    used_connections = {f"{first_connection.start_station}-{first_connection.end_station}"}
    needed_connections.pop(f"{first_connection.start_station}-{first_connection.end_station}")

    return route, total_time, current_station, used_connections

def n_deep_algorithm(connection_data, possible_connections, needed_connections, depth):
    """
    Creates a route by looking several steps ahead to decide the best path.
    Uses the `Trajectory` class to store connections and updates the `needed_connections`.
    """
    traject = Trajectory()  # Initialize a new trajectory to store the connections
    total_time = 0
    remaining_needed_connections = copy.deepcopy(needed_connections)  # Make a deep copy of needed connections
    used_connections = set()  # Set to track used connections
    current_station = None

    while len(remaining_needed_connections) > 0:
        if not traject.connection_list:
            route, total_time, current_station, used_connections = initialize_route(remaining_needed_connections)
            traject.connection_list = route

        else:
            # Explore paths to decide the next connection
            _, best_path = explore_paths(
                current_station, connection_data, used_connections, remaining_needed_connections,
                possible_connections, total_time, depth)

            if not best_path:
                break

            # add info
            next_connection = best_path[0]
            traject.add_connection(next_connection)
            total_time += next_connection.duration
            current_station = next_connection.end_station
            used_connections.add(f"{next_connection.start_station}{next_connection.end_station}")

            # remove the connection if it is present in the needed connections
            remaining_needed_connections.pop(f"{next_connection.start_station}-{next_connection.end_station}", None)

            if total_time > 120:
                break

    return traject, remaining_needed_connections

def create_deep_trajectories(trajectory_amount, connection_algorithm,
    full_connection_dict, original_connection_dict, needed_connections_dict,
    possible_directions, depth, total_connections):
    """
    Creates a given number of trajectories using the specified algorithm.
    Returns a Solution object containing the trajectories.
    """
    final_solution = Solution()
    needed_connections = copy.deepcopy(needed_connections_dict)

    # Create the required number of trajectories
    for i in range(trajectory_amount):
        current_trajectory, needed_connections = n_deep_algorithm(
            full_connection_dict, possible_directions, needed_connections, depth
        )
        final_solution.add_trajectory(current_trajectory)


    return final_solution
