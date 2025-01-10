import random
import pandas as pd

####################################### REMOVE THIS WHEN DONE
#######################################
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

def get_possible_directions(csv_file):
    df = pd.read_csv(csv_file)

    # Create an empty DF with twice the rows of the original (both directions)
    corrected_df = pd.DataFrame(index=range(df.shape[0] * 2), columns=['station1', 'station2', 'duration'])

    # Fill in the corrected DF with both directions
    row_index = 0
    for _, row in df.iterrows():
        station_1 = row['station1']
        station_2 = row['station2']
        duration = row['distance']

        # Original direction
        corrected_df.loc[row_index] = {'station1': station_1, 'station2': station_2, 'duration': duration}
        row_index += 1

        # Reverse direction
        corrected_df.loc[row_index] = {'station1': station_2, 'station2': station_1, 'duration': duration}
        row_index += 1

    # Get all unique departure stations
    possible_departure_stations = corrected_df['station1'].unique()

    possible_directions = {}
    for station in possible_departure_stations:
        # Initialize the key (station)
        possible_directions[station] = []

        # Initialize the value (list of possible directions)
        connected_stations = corrected_df[corrected_df['station1'] == station]['station2'].tolist()
        possible_directions[station] = connected_stations

    return possible_directions, corrected_df

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

def calculate_score(connections, trajectory_amount, duration, total_connections = 28):
    """
    Calculates the quality of the itinerary. Outputs a score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)

possible_connections, corrected_df = get_possible_directions("ConnectiesHolland.csv")
test_dict = create_connections(corrected_df)

original_df = pd.read_csv("ConnectiesHolland.csv")
original_dict = create_connections(original_df)

#######################################
#######################################
def choose_random_connections(connection_object_dict, possible_connections_dict):
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
    while duration <= 120:

        if len(objects) == 0:
            # Start with a random connection and append its first station to the list
            connection_object = random.choice(list(connection_object_dict.values()))
            start_station = connection_object.start_station
            objects.append(connection_object)

            # Extract a random possible station to travel to and append to the list
            possible_stations = possible_connections_dict[start_station]
            chosen_station = random.choice(possible_stations)

        else:
            departure_station = objects[-1].end_station
            possible_stations = possible_connections[departure_station]
            chosen_station = random.choice(possible_stations)
            connection_object = connection_object_dict[departure_station + "-" + chosen_station]

            # if duration time goes over 120: don't add connection and return list
            if duration + connection_object.duration > 120:
                return objects
            else:
                duration += connection_object.duration

            objects.append(connection_object)

    return objects

test_objects = choose_random_connections(test_dict, possible_connections)

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
        for item in current_connections:
            # append start and end station for first station in trajectory
            if iteration == 0:
                station_list.append(item.start_station)
                station_list.append(item.end_station)

            # otherwise add only end station
            else:
                station_list.append(item.end_station)

            # add duration of connection to total
            total_duration += item.duration

            iteration += 1

        print(station_list)
        # fill in dataframe with correct data
        dataframe.loc[i, 'stations'] = station_list
        dataframe.loc[i, 'train'] = 'train_' + str(i + 1)

        connections_set = connections_set.union(set(current_connections))
    print(f"total duration: {total_duration}")
    # find the number of connections that were ridden, calculate score and add to df
    original_connections = set(original_connection_dict.values())
    connections_set = original_connections.intersection(connections_set)
    connection_number = len(connections_set)
    score = calculate_score(connection_number, trajectory_amount, total_duration)
    dataframe.iloc[-1, dataframe.columns.get_loc('train')] = 'score'
    dataframe.iloc[-1, dataframe.columns.get_loc('stations')] = score

    return dataframe

dataframe = create_trajectories(3, choose_random_connections, test_dict, original_dict, test_dict, possible_connections)
print(dataframe)
