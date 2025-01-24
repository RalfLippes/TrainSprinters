from code.other_functions.calculate_score import calculate_score
from code.visualisation.representation import create_map
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

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

    def create_map(self, station_locations):
        #reads the csv file with coordinates
        stations = pd.read_csv(station_locations)

        #dictionary with station coordinates of every station
        coordinates_stations = {}

        # Create a plot figure
        fig, ax = plt.subplots(figsize=(6, 10))
        #plt.style.use("dark_background")

        for index, row in stations.iterrows():

            #safe the name of the station name and its coordinates in a dictionary for easy access
            coordinates_stations[row.iloc[0]]= [row.iloc[1], row.iloc[2]]


            ax.scatter(row.iloc[2], row.iloc[1], marker='o')
            ax.text(row.iloc[2], row.iloc[1] - 0.02, row.iloc[0], fontsize=6, color='white')


        return fig, ax, coordinates_stations

    def create_simulation_data(self):

        #create a list with all the data necessery to plot a simulation
        plotting_data = []

        for trajectory in self.solution:
            plotting_data.append({"x_coords": [], "y_coords": [],
                "index_of_connection_plotted": 0,
                "time_in_current_connection": 0,
            "trajectory": trajectory})


        return plotting_data

    def plot_step(self, plotting_data, stations_data, ax, station_coordinates):

        ax.clear()

        for station, coords in station_coordinates.items():
            ax.scatter(coords[1], coords[0], marker='o', color='red')
            ax.text(coords[1], coords[0] - 0.02, station, fontsize=6, color='blue')


        for trajectory_data in plotting_data:

            #save trajectory object
            trajectory = trajectory_data["trajectory"]

            #make variable for connection_index
            connection_index = trajectory_data["index_of_connection_plotted"]

            connection = trajectory.connection_list[connection_index]

            start_coords = station_coordinates[connection.start_station]
            end_coords = station_coordinates[connection.end_station]
            connection_duration = connection.duration
            time_along_connection = trajectory_data["time_in_current_connection"]

            if connection_index >= len(trajectory.connection_list):
                ax.plot(trajectory_data["x_coords"], trajectory_data["y_coords"],
                        linestyle="--", label=f"Train {self.solution.index(trajectory) + 1}")
                continue

            if time_along_connection < connection.duration:
                t = time_along_connection / connection.duration
                x_step = (1 - t) * start_coords[1] + t * end_coords[1]
                y_step = (1 - t) * start_coords[0] + t * end_coords[0]

                trajectory_data["x_coords"].append(x_step)
                trajectory_data["y_coords"].append(y_step)

                #add to the time counter
                trajectory_data["time_in_current_connection"] += 1

            if trajectory_data["time_in_current_connection"] >= connection_duration:
                trajectory_data["index_of_connection_plotted"] += 1
                trajectory_data["time_in_current_connection"] = 0

            ax.plot(trajectory_data["x_coords"], trajectory_data["y_coords"],
                    linestyle="--", label=f"Train {self.solution.index(trajectory) + 1}")

        plt.legend()
        plt.draw()

        return

    def simulate_solution(self, plotting_data, stations_data, max_duration):

        """
        plots every second of the solution
        """
        plt.ion()
        fig, ax, station_coordinates = self.create_map(stations_data)

        for step in range(max_duration):

            self.plot_step(plotting_data, stations_data, ax, station_coordinates)

            plt.pause(0.01)



        ax.plot(trajectory_data["x_coords"], trajectory_data["y_coords"],
                linestyle="--", label=f"Train {self.solution.index(trajectory) + 1}")


        return plt.show()
