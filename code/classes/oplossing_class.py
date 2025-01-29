from code.algorithms.calculate_score import calculate_score
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
        #stores trajectory objects in a list
        self.solution = []

    def add_trajectory(self, trajectory):
        """adds a trajectory to the solution"""
        self.solution.append(trajectory)

    def calculate_solution_score(self, original_connection_dict, total_connections):
        """Calculates the score of this schedule"""
        connection_set = set()
        duration = 0

        #checks how many trajectories the solution has
        trajectory_amount = len(self.solution)

        #checks which connection are driven in solution and checks the total duration
        for trajectory in self.solution:
            for connection in trajectory.connection_list:
                if connection.start_station + '-' + connection.end_station in original_connection_dict:
                    connection_key = f"{connection.start_station}-{connection.end_station}"
                    connection_set.add(connection_key)
                duration += connection.duration
        connections = len(connection_set)

        #calculates score with the amount of connections driven, the trajectories and the duration of the solution
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

    def find_duration(self):
        total_duration = 0
        for trajectory in self.solution:
            for connection in trajectory.connection_list:
                total_duration += connection.duration

        return total_duration

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

            # adds the stations of trajectory to a row
            stations_string = f"[{', '.join(station_list)}]"
            dataframe.loc[row_index, 'stations'] = stations_string
            dataframe.loc[row_index, 'train'] = 'train_' + str(row_index + 1)
            row_index += 1

        #in the final row it adds the score of the solution
        dataframe.loc[row_index, 'train'] = 'score'
        dataframe.loc[row_index, 'stations'] = score

        return dataframe

    def create_map(self, station_locations):
        """
        creates a with all stations plotted on it
        """

        # Creates a map to add the stations and traj. to
        self.fig, self.ax = plt.subplots(figsize=(6, 10))

        #plot all stations on the map
        for key, value in station_locations.items():
            self.ax.scatter(value.x, value.y, marker='o', color='red')
            self.ax.text(value.x, value.y - 0.02, value.name, fontsize=6)

        return

    def create_simulation_data(self):

        """
        makes a list that contains a dictionary for every trajectory
        that holds information about the x and y coords that need to be plotted
        the index of the connection that is being plotted and the time in current
        connection
        """

        #create a list with all the data necessery to plot a simulation
        plotting_data = []

        #creates a dictionary for every trajectory
        for trajectory in self.solution:

            #adds a place to store data for plotting
            plotting_data.append({"x_coords": [], "y_coords": [],
                "index_of_connection_plotted": 0,
                "time_in_current_connection": 0,
            "trajectory": trajectory})

        return plotting_data

    def plot_step(self, plotting_data, stations_data):

        #empty plot
        self.ax.clear()

        #plots stations on the map
        for key, value in stations_data.items():
            self.ax.scatter(value.x, value.y, marker='o', color = 'blue')
            self.ax.text(value.x, value.y - 0.02, value.name, fontsize=6)

        #
        for trajectory_data in plotting_data:

            #save trajectory object
            trajectory = trajectory_data["trajectory"]

            connection_index = trajectory_data["index_of_connection_plotted"]

            #check if trajectory is finished it does not add coords
            if connection_index >= len(trajectory.connection_list):
                self.ax.plot(trajectory_data["x_coords"], trajectory_data["y_coords"],
                        linestyle="--", label=f"Train {self.solution.index(trajectory) + 1}")
                continue

            #check which connection we are plotting
            connection = trajectory.connection_list[connection_index]

            #check what the start and end coords are of current connection to indicate step direction
            start_coords = [stations_data[connection.start_station].x , stations_data[connection.start_station].y]
            end_coords = [stations_data[connection.end_station].x , stations_data[connection.end_station].y]

            #save the connections duration and how far we are along the connection
            connection_duration = connection.duration
            time_along_connection = trajectory_data["time_in_current_connection"]

            #check if the connection is not finished
            if time_along_connection < connection.duration:

                #add a step to the simulation
                t = time_along_connection / connection.duration
                x_step = (1 - t) * start_coords[0] + t * end_coords[0]
                y_step = (1 - t) * start_coords[1] + t * end_coords[1]

                trajectory_data["x_coords"].append(x_step)
                trajectory_data["y_coords"].append(y_step)

                #add to the time counter
                trajectory_data["time_in_current_connection"] += 1

            #check if the connection is finished
            if trajectory_data["time_in_current_connection"] >= connection_duration:
                trajectory_data["index_of_connection_plotted"] += 1
                trajectory_data["time_in_current_connection"] = 0

            #plot coordinates with the next step
            self.ax.plot(trajectory_data["x_coords"], trajectory_data["y_coords"],
                    linestyle="--", label=f"Train {self.solution.index(trajectory) + 1}")

        plt.legend()
        plt.draw()

        return

    def simulate_solution(self, stations_data, max_duration):

        """
        plots a step that represents a minute of real time in the simulation
        """

        #creates a map for the solution
        self.create_map(stations_data)

        #creates an empty list where we are going to add the plotting data
        plotting_data = self.create_simulation_data()

        #loop over the amount of steps
        for step in range(max_duration):
            self.plot_step(plotting_data, stations_data)
            plt.pause(0.01)

        plt.show()

        return
