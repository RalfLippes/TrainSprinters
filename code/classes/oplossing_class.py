from code.other_functions.calculate_score import calculate_score
import pandas as pd

class Solution:
    """
    Initializes a solution which will store trajectory objects. Contains a function
    to add a trajectory to the list of trajectories.
    """
    def __init__(self):
        self.solution = []

    def add_trajectory(self, trajectory):
        self.solution.append(trajectory)

    def calculate_solution_score(self, original_connection_dict, total_connections):
        """Calculates the score of this schedule"""
        connection_set = set()
        duration = 0
        trajectory_amount = len(self.solution)

        for trajectory in self.solution:
            for connection in trajectory.connection_list:
                if connection.start_station + '-' + connection.end_station in original_connection_dict:
                    connection_key = f"{connection.start_station}-{connection.end_station}"
                    connection_set.add(connection_key)
                duration += connection.duration
        connections = len(connection_set)

        return calculate_score(connections, trajectory_amount,
            duration, total_connections)

    def amount_connection(self, original_connection_dict):
        """calculates the amount of connection in a solution"""
        connection_set = set()

        for trajectory in self.solution:
            for connection in trajectory.connection_list:
                if connection.start_station + '-' + connection.end_station in original_connection_dict:
                    connection_key = f"{connection.start_station}-{connection.end_station}"
                    connection_set.add(connection_key)

        return len(connection_set)

    def create_dataframe_from_solution(self, original_connection_dict, total_connections):
        """
        Creates dataframe in correct format from solution object.
        """
        score = self.calculate_solution_score(original_connection_dict, total_connections)
        dataframe = pd.DataFrame(columns = ['train', 'stations'])
        row_index = 0

        for trajectory in self.solution:
            station_list = []
            iteration = 0

            # skip iteration if trajectory is empty
            if len(trajectory.connection_list) == 0:
                continue

            # make list of stations from objects in list
            for iteration, item in enumerate(trajectory.connection_list):

                # append start and end station for first station in trajectory
                if iteration == 0:
                    station_list.append(item.start_station)
                    station_list.append(item.end_station)

                # otherwise add only end station
                else:
                    station_list.append(item.end_station)

                iteration += 1

            # fill in dataframe with correct data
            stations_string = f"[{', '.join(station_list)}]"
            dataframe.loc[row_index, 'stations'] = stations_string
            dataframe.loc[row_index, 'train'] = 'train_' + str(row_index + 1)

            row_index += 1

        dataframe.loc[row_index, 'train'] = 'score'
        dataframe.loc[row_index, 'stations'] = score

        return dataframe
