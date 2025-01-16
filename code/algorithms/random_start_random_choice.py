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



def n_deep_algorithm(connection_object_dict, possible_connections_dict,
                     needed_connections_dict, depth=3):
    """
    Generates a trajectory by looking n connections into the future to select the best path.
    Evaluates paths based on the highest score, prioritizing the number of new connections
    and minimizing the duration of the route.
    """
    def evaluate_future_paths(current_station, remaining_connections, current_duration, depth_left):
        """
        Recursively evaluates the score of future paths up to the given depth.
        Returns the best score and corresponding path.
        """
        if depth_left == 0 or len(remaining_connections) == 0:
            # Base case: calculate score for current state
            connections_made = len(needed_connections_dict) - len(remaining_connections)
            score = calculate_score(connections_made, 1, current_duration)
            return score, []

        best_score = float('-inf')
        best_path = []

        possible_stations = possible_connections_dict.get(current_station, [])
        for station in possible_stations:
            connection_key = f"{current_station}-{station}"
            if connection_key in remaining_connections:
                connection = remaining_connections[connection_key]
                if current_duration + connection.duration > 120:
                    continue  # Skip if adding this connection exceeds time limit

                # Recursively evaluate future paths
                new_remaining_connections = copy.deepcopy(remaining_connections)
                new_remaining_connections.pop(connection_key)
                future_score, future_path = evaluate_future_paths(
                    connection.end_station, new_remaining_connections,
                    current_duration + connection.duration, depth_left - 1
                )

                # Update best score and path if this option is better
                if future_score > best_score:
                    best_score = future_score
                    best_path = [connection] + future_path

        return best_score, best_path

    # Initialize variables
    objects = []
    duration = 0
    new_needed_connections_dict = copy.deepcopy(needed_connections_dict)
    current_station = None

    # Generate trajectory by looking `depth` steps into the future
    while len(new_needed_connections_dict) > 0:
        if len(objects) == 0:
            # Start with a random needed connection
            connection = random.choice(list(new_needed_connections_dict.values()))
            objects.append(connection)
            duration += connection.duration
            current_station = connection.end_station
            new_needed_connections_dict.pop(f"{connection.start_station}-{connection.end_station}")
        else:
            # Look `depth` steps ahead to choose the best path
            _, best_path = evaluate_future_paths(
                current_station, new_needed_connections_dict, duration, depth
            )

            if len(best_path) == 0:
                break  # No valid path found

            # Add the first connection from the best path to the trajectory
            next_connection = best_path[0]
            objects.append(next_connection)
            duration += next_connection.duration
            current_station = next_connection.end_station
            new_needed_connections_dict.pop(f"{next_connection.start_station}-{next_connection.end_station}")

            # Stop if adding this connection exceeds time limit
            if duration > 120:
                break

    return objects, new_needed_connections_dict

def create_better_trajectories(trajectory_amount, connection_algorithm,
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
            current_connections, needed_connections = connection_algorithm(*arg_list,
                needed_connections)

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



dataframe, connections_made = create_better_trajectories(
    trajectory_amount=5,
    connection_algorithm=n_deep_algorithm,
    full_connection_dict=full_connection_dict,
    original_connection_dict=original_connection_dict,
    needed_connections_dict=needed_connections_dict,
    arg1=full_connection_dict,
    arg2=possible_connections_dict,
    arg3=needed_connections_dict,
    arg4=3  # Depth for n_deep_algorithm
)

print(dataframe)
