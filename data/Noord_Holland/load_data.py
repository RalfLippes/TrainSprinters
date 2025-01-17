import pandas as pd
from code.classes.verbinding_class import Connection
from code.classes.station_class import Station

def get_possible_directions(csv_file):
    original_df = pd.read_csv(csv_file)

    # Create an empty DF with twice the rows of the original (both directions)
    corrected_df = pd.DataFrame(index=range(original_df.shape[0] * 2), columns=['station1', 'station2', 'duration'])

    # Fill in the corrected DF with both directions
    row_index = 0
    for _, row in original_df.iterrows():
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

    return possible_directions, corrected_df, original_df

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

def load_station_objects(csv_file):
    """
    reads a csv file and creates Station objects for every station listed
    in the file. Returns a dictionary with the name of the station as the key,
    and the corresponding object as the value.
    """
    stations_dictionary = {}

    # find names of start station, end station and duration of connection
    for index, row in csv_file.iterrows():
        station = row.iloc[0]
        y = row.iloc[1]
        x = row.iloc[2]

        # initialize Connection object with correct data and add to dictionary
        stations_dictionary[station] = Station(x, y, station)

    return stations_dictionary
