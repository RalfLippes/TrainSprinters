import random
import pandas as pd
import copy

class Connection:
    """
    Contains all the aspects of a connection, including start station, end station
    and the duration of riding the connection.
    """
    def __init__(self, start_station, end_station, duration):
        self.start_station = start_station
        self.end_station = end_station
        self.duration = duration

class Trajectory:
    """
    Initializes a trajectory which will store connection objects. Contains a function
    to add a connection to the list of connections.
    """
    def __init__(self):
        self.connection_list = []

    def add_connection(self, connection_object):
        """Manually add a connection object to the connection list"""
        self.connection_list.append(connection_object)

def calculate_score(connections, trajectory_amount, duration, total_connections = 28):
    """
    Calculates the quality of the itinerary. Outputs a score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)


import random
import copy

def n_deep_algorithm(connection_data, possible_connections, needed_connections, depth=3):
    """
    Creates a route by looking several steps ahead to decide the best path.
    The goal is to maximize the score by finding new connections and keeping the travel time short.
    Already-used connections do not add to the score.
    """

    def explore_paths(current_station, available_connections, used_connections, current_time, steps_left):
        """
        This helper function explores possible routes up to a certain depth.
        It returns the best score and the path that achieves it.
        """
        # If no more steps are allowed or there are no connections left, calculate the score
        if steps_left == 0 or not available_connections:
            new_connections_made = len(needed_connections) - len(available_connections)
            score = calculate_score(new_connections_made, 1, current_time)
            return score, []

        # Store all possible paths and their scores
        path_scores = {}
        next_stations = possible_connections.get(current_station, [])

        # Try every station that can be reached from the current one
        for next_station in next_stations:
            # Identify the connection between the current and next station
            connection_key = f"{current_station}-{next_station}"
            connection = available_connections.get(connection_key)

            if connection is None:
                continue  # Skip if the connection doesn't exist

            # Skip connections that would exceed the time limit
            if current_time + connection.duration > 120:
                continue

            # Mark this connection as used
            updated_used_connections = used_connections.copy()
            updated_used_connections.add(connection_key)

            # Remove this connection from the available ones
            updated_available_connections = copy.deepcopy(available_connections)
            updated_available_connections.pop(connection_key)

            # Recursively explore the next steps
            future_score, future_path = explore_paths(
                next_station, updated_available_connections, updated_used_connections,
                current_time + connection.duration, steps_left - 1
            )

            # Add bonus points for making a new connection
            is_new_connection = connection_key in needed_connections
            if is_new_connection:
                future_score += 300

            # Save the score and path
            path_scores[(connection, *future_path)] = future_score

        # If no valid paths are found, return a fallback score
        if not path_scores:
            return float('-inf'), []

        # Find the path with the highest score
        best_path = max(path_scores, key=path_scores.get)
        best_score = path_scores[best_path]

        return best_score, list(best_path)

    # Initialize the route-building process
    route = []
    total_time = 0
    remaining_needed_connections = copy.deepcopy(needed_connections)
    used_connections = set()
    current_station = None

    # Keep building the route until all needed connections are covered
    while len(remaining_needed_connections) > 0:
        if not route:
            # Start with a random needed connection
            first_connection = random.choice(list(remaining_needed_connections.values()))
            route.append(first_connection)
            total_time += first_connection.duration
            current_station = first_connection.end_station
            used_connections.add(f"{first_connection.start_station}-{first_connection.end_station}")
            remaining_needed_connections.pop(f"{first_connection.start_station}-{first_connection.end_station}")
        else:
            # Look ahead by `depth` steps to decide the next connection
            _, best_path = explore_paths(
                current_station, remaining_needed_connections, used_connections, total_time, depth)

            # Stop if no valid path is found
            if not best_path:
                break

            # Add the best connection to the route
            next_connection = best_path[0]
            route.append(next_connection)
            total_time += next_connection.duration
            current_station = next_connection.end_station
            used_connections.add(f"{next_connection.start_station}-{next_connection.end_station}")
            remaining_needed_connections.pop(f"{next_connection.start_station}-{next_connection.end_station}")

            # Stop if the time limit is exceeded
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
