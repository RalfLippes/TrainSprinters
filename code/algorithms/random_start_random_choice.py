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

def generate_trajectory(connection_object_dict, possible_connections_dict, needed_connections_dict):
    """
    generates a random trajectory by preferring to choose from the connections that
    have not been chosen yet (provided in needed_connections). Takes a dictionary
    with connections that haven't been ridden yet, a dictionary with all possible
    connections and a dictionary with all possible target station from each possible
    starting station. Returns list of connection objects (trajectory) and the updated
    needed connections dictionary.
    """
    objects = []
    duration = 0
    new_needed_connections_dict = copy.deepcopy(needed_connections_dict)

    # make random amount of connections between 1 and 24
    if len(new_needed_connections_dict) > 0:
        for i in range(random.randint(1, 24)):
            # if there is no objects yet, we need a random starting point
            if len(objects) <= 0:
                # Start with a random needed connection and append to list
                connection_object = random.choice(list(new_needed_connections_dict.values()))
                start_station = connection_object.start_station
                objects.append(connection_object)
                duration += connection_object.duration

            # if we have >0 objects, go on from the end station of the previous connection
            else:
                length_before = len(objects)
                departure_station = objects[-1].end_station

                # check possible stations (connections) and append to list if it is still needed
                possible_stations = possible_connections_dict[departure_station]
                for station in possible_stations:
                    if departure_station + '-' + station in new_needed_connections_dict:
                        connection_object = connection_object_dict[departure_station + "-" + station]
                        #TODO: make sure to try other stations instead of returning
                        # if duration time goes over 120: don't add connection and return list
                        if duration + connection_object.duration > 120:
                            return objects, new_needed_connections_dict

                        # add object, count duration and remove connection from needed connections
                        objects.append(needed_connections_dict[departure_station + '-' + station])
                        duration += connection_object.duration
                        new_needed_connections_dict.pop(departure_station + '-' + station)
                        break

                # store length after and check if previous loop has added any connections
                length_after = len(objects)
                if length_after == length_before:
                    # choose random possible connection
                    chosen_station = random.choice(possible_stations)
                    connection_object = connection_object_dict[departure_station + "-" + chosen_station]

                    # if duration time goes over 120: don't add connection and return list
                    if duration + connection_object.duration > 120:
                        return objects, new_needed_connections_dict

                    duration += connection_object.duration
                    objects.append(connection_object)

    return objects, new_needed_connections_dict

def create_better_trajectories(trajectory_amount, connection_algorithm, full_connection_dict, original_connection_dict, needed_connections_dict, arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None, arg10 = None):
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
    needed_connections = needed_connections_dict

    # remove arguments that are none
    arg_list = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    arg_list = [item for item in arg_list if item is not None]

    # create right amount of trajectories
    for i in range(trajectory_amount):
        station_list = []
        current_trajectory = Trajectory()

        # find connections according to the given connection algorithm
        current_connections, needed_connections = connection_algorithm(*arg_list, needed_connections)

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
