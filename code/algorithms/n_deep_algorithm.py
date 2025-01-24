import random
import pandas as pd
import copy
from code.classes.traject_class import Trajectory
from code.classes.verbinding_class import Connection
from code.other_functions.calculate_score import calculate_score
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

def n_deep_algorithm(connection_data, possible_connections, needed_connections, depth=3):
    """
    Creates a route by looking several steps ahead to decide the best path.
    """
    route = []
    total_time = 0
    remaining_needed_connections = copy.deepcopy(needed_connections)
    used_connections = set()
    current_station = None

    while len(remaining_needed_connections) > 0:
        if not route:
            # Initialize the route with a random needed connection
            route, total_time, current_station, used_connections = initialize_route(remaining_needed_connections)

        else:
            # Explore paths to decide the next connection
            _, best_path = explore_paths(
                current_station, remaining_needed_connections, used_connections,
                needed_connections, possible_connections, total_time, depth)

            if not best_path:
                break

            next_connection = best_path[0]
            route.append(next_connection)
            total_time += next_connection.duration
            current_station = next_connection.end_station
            used_connections.add(f"{next_connection.start_station}-{next_connection.end_station}")
            remaining_needed_connections.pop(f"{next_connection.start_station}-{next_connection.end_station}")

            if total_time > 120:
                break

    return route, remaining_needed_connections

def create_deep_trajectories(trajectory_amount, connection_algorithm,
    full_connection_dict, original_connection_dict, needed_connections_dict,
    arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None,
    arg7 = None, arg8 = None, arg9 = None, arg10 = None):
    """
    Creates a given number of trajectories. Uses a specified method to select
    connections for the trajectories. Make sure to provide the arguments needed
    for the connection function. Returns a dataframe with each train and its
    trajectory, as well as the total score of this itinerary.
    """
    # create empty dataframe to store data in
    dataframe = pd.DataFrame(index = range(trajectory_amount + 1), columns =
        ['train', 'stations'])
    total_duration = 0
    connections_set = set()
    needed_connections = needed_connections_dict

    # remove arguments that are none
    arg_list = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    arg_list = [item for item in arg_list if item is not None]

    # create right amount of trajectories
    for i in range(trajectory_amount):
        station_list = []
        current_trajectory = Trajectory()

        # find connections according to the given connection algorithm
        if len(needed_connections) > 0:
            current_connections, needed_connections = connection_algorithm(
                full_connection_dict,
                arg2,
                needed_connections,
                arg4
            )

        iteration = 0

        # make list of stations from objects in list
        for item in list(current_connections):

            # append start and end station for first station in trajectory
            if iteration == 0:
                station_list.append(item.start_station)
                station_list.append(item.end_station)

            # otherwise add only end station
            else:
                station_list.append(item.end_station)

            # add duration of connection to total
            total_duration += item.duration

            # add start and end station as a tuple to the set of connections
            connections_set = connections_set.union({(item.start_station +
                item.end_station)})

            iteration += 1

        # fill in dataframe with correct data
        stations_string = f"[{', '.join(station_list)}]"
        dataframe.loc[i, 'stations'] = stations_string
        dataframe.loc[i, 'train'] = 'train_' + str(i + 1)

    # make a set of tuples with (start_station, end_station) for original connections
    original_set = set()
    for item in original_connection_dict:
        original_set = original_set.union({(original_connection_dict[item].start_station +
            original_connection_dict[item].end_station)})

    # find all connections of the trajectories that are valid and count them
    set_connections = set.intersection(connections_set, original_set)
    connection_number = len(set_connections)

    # calculate itinerary score and put into dataframe
    score = calculate_score(connection_number, trajectory_amount, total_duration)
    dataframe.iloc[-1, dataframe.columns.get_loc('train')] = 'score'
    dataframe.iloc[-1, dataframe.columns.get_loc('stations')] = score

    return dataframe, connection_number
