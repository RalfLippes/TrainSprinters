import random
import copy
import pandas as pd

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

def choose_random_connections(connection_object_dict, possible_connections_dict, connection_amount):
    """
    Takes a dictionary with strings as keys in the form 'Startstation-Endstation'
    and values of connection objects. Makes a list of n random connections,
    starting by choosing a random first station. Then repeats finding a random
    possible connection until the time limit (120 minutes) would be reached.
    Returns list of stations that the trajectory passes and the total duration
    of the trajectory.
    """
    objects = []
    duration = 0

    # create given number of connection objects
    for i in range(connection_amount):

        if len(objects) == 0:
            # Start with a random connection and append its first station to the list
            connection_object = random.choice(list(connection_object_dict.values()))
            start_station = connection_object.start_station
            objects.append(connection_object)
            duration += connection_object.duration

        else:
            departure_station = objects[-1].end_station
            possible_stations = possible_connections_dict[departure_station]
            chosen_station = random.choice(possible_stations)
            connection_object = connection_object_dict[departure_station + "-" + chosen_station]

            # Create a copy of the possible station list before looping
            temp_possible_stations = copy.deepcopy(possible_stations)

            # if duration time goes over 120 enter a loop where we try other connections 
            while duration + connection_object.duration > 120:

                # Remove the station we already tried
                temp_possible_stations.remove(chosen_station)

                # Return the objects if the list is empty after removing
                if len(list(temp_possible_stations)) == 0:
                    return objects

                else:
                    chosen_station = random.choice(temp_possible_stations)
                    connection_object = connection_object_dict[departure_station + "-" + chosen_station]


            duration += connection_object.duration

            objects.append(connection_object)

    return objects

def create_trajectories(trajectory_amount, connection_algorithm, full_connection_dict, original_connection_dict, arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None, arg10 = None):
    """
    Creates a given number of trajectories. Uses a specified method to select
    connections for the trajectories. Make sure to provide the arguments needed
    for the connection function. Returns a dataframe with each train and its
    trajectory, as well as the total score of this itinerary.
    """
    # create empty dataframe to store data in
    dataframe = pd.DataFrame(index = range(trajectory_amount + 1), columns = ['train', 'stations'])
    total_duration = 0
    connections_set = set()

    # remove arguments that are none
    arg_list = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    arg_list = [item for item in arg_list if item is not None]

    # create right amount of trajectories
    for i in range(trajectory_amount):
        station_list = []
        current_trajectory = Trajectory()

        # find connections according to the given connection algorithm
        current_connections = connection_algorithm(*arg_list)

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
            connections_set = connections_set.union({(item.start_station + item.end_station)})

            iteration += 1

        # fill in dataframe with correct data
        stations_string = f"[{', '.join(station_list)}]"
        dataframe.loc[i, 'stations'] = stations_string
        dataframe.loc[i, 'train'] = 'train_' + str(i + 1)

    # make a set of tuples with (start_station, end_station) for original connections
    original_set = set()
    for item in original_connection_dict:
        original_set = original_set.union({(original_connection_dict[item].start_station + original_connection_dict[item].end_station)})

    # find all connections of the trajectories that are valid and count them
    set_connections = set.intersection(connections_set, original_set)
    connection_number = len(set_connections)

    # calculate itinerary score and put into dataframe
    score = calculate_score(connection_number, trajectory_amount, total_duration)
    dataframe.iloc[-1, dataframe.columns.get_loc('train')] = 'score'
    dataframe.iloc[-1, dataframe.columns.get_loc('stations')] = score

    return dataframe, connection_number
