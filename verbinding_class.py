import pandas as pd
import random
from csv_possibility_reader import get_possible_directions

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
    Initializes a trajectory with a given number of connections. The way the
    connections are chosen is dictated by the connection function that should be
    given to this class.
    """
    def __init__(self, number_of_connections, connection_function):
        self.number_of_connections = number_of_connections
        self.connection_function = connection_function

    def choose_connections(self):
        """
        Makes a list of n random connections, starting by choosing a first station
        dictated by the connection function. The repeats finding a random possible
        connection number_of_connections amount of times. Returns list of stations
        that the trajectory passes and the total duration of the trajectory.
        """
        stations = []
        duration = 0

        # create given number of connection objects
        for i in range(self.number_of_connections):

            if len(stations) == 0:
                # Start with a random connection and append its first station to the list
                connection_object = self.connection_function()
                start_station = connection_object.start_station
                stations.append(start_station)

                # Extract a random possible station to travel to and append to the list
                possible_stations = possible_connections[start_station]
                chosen_station = random.choice(possible_stations)
                stations.append(chosen_station)

            else:
                departure_station = stations[-1]
                possible_stations = possible_connections[departure_station]
                chosen_station = random.choice(possible_stations)
                connection_object = test_dict[departure_station + "-" + chosen_station]

                # if duration time goes over 120: don't add connection and return list
                if duration + connection_object.duration > 120:
                    return stations, duration
                else:
                    duration += connection_object.duration

                stations.append(chosen_station)

        return stations, duration

def create_trajectories(trajectory_amount, connection_function):
    """
    Creates a given number of trajectories. Uses a specified method to select
    connections for the trajectories. Returns a dataframe with each train and its
    trajectory, as well as the total score of this itinerary.
    """
    # create empty dataframe to store data in
    dataframe = pd.DataFrame(index = range(trajectory_amount + 1), columns = ['train', 'stations'])
    total_duration = 0
    connections_set = set()

    # create right amount of trajectories
    for i in range(trajectory_amount):
        current_trajectory = Trajectory(random.randint(1, 14), random_connection)

        # store connections and train number in dataframe
        current_connections, current_duration = current_trajectory.choose_connections()
        dataframe.loc[i, 'stations'] = current_connections
        dataframe.loc[i, 'train'] = 'train_' + str(i + 1)

        # add duration of each connection to the total
        for connection in range(len(current_connections) - 1):
            connection_name = current_connections[connection] + '-' + current_connections[connection + 1]
            total_duration += test_dict[connection_name].duration

            # make set of start and end station and add to set of total connections
            connection_name = set((current_connections[connection], current_connections[connection + 1]))

        # put all the unique connections into the set of connections
        connections_set = connections_set.union(set(connection_name))

    # find the number of connections that were ridden, calculate score and add to df
    connection_number = len(connections_set)
    score = calculate_score(connection_number, trajectory_amount, total_duration)
    dataframe.iloc[-1, dataframe.columns.get_loc('train')] = 'score'
    dataframe.iloc[-1, dataframe.columns.get_loc('stations')] = score

    return dataframe

def calculate_score(connections, trajectory_amount, duration, total_connections = 28):
    """
    Calculates the quality of the itinerary. Outputs a score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)

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

def random_connection():
    connection = random.choice(list(test_dict.keys()))
    return test_dict[connection]

possible_connections, corrected_df = get_possible_directions("ConnectiesHolland.csv")
test_dict = create_connections(corrected_df)

test_df = create_trajectories(7, random_connection)

print(test_df)
