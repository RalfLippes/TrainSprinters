import pandas as pd


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
