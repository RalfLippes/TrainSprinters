import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import ast
import re

def create_map(station_locations):
    """
    this function takes a csv file that includes the y,x coordinates of different
    stations and a dataframe that includes each train with its trajectory. Returns
    a plotted graph of all trajectories showing which cities they pass.
    """

    #reads the csv file with coordinates
    stations = pd.read_csv(station_locations)

    coordinates_stations = {}

    # Create a single plot
    plt.figure(figsize=(6, 10))

    for index, row in stations.iterrows():

        #safe the name of the station name and its coordinates in a dictionary for easy access
        coordinates_stations[row.iloc[0]]= [row.iloc[1], row.iloc[2]]


        plt.scatter(row.iloc[2], row.iloc[1], color='blue', marker='x')
        plt.text(row.iloc[2] - 0.03, row.iloc[1] - 0.01, row.iloc[0], fontsize=6)

    return coordinates_stations

def plot_trajectories(trajectories, station_locations):

    """
    plots the trajectories on a map. return
    """

    station_coordinates = create_map(station_locations)


    #iterate over the different trajectories in our dataset to plot them on the graph
    for index, row in trajectories.iloc[:(len(trajectories)-1)].iterrows():

        #store the x and y coordinates of the trajectories
        x_coordinates = []
        y_coordinates = []

        # remove brackets and split on commas, then turn into list of strings
        cleaned_string = row.iloc[1].strip("[]")
        split_string = cleaned_string.split(",")
        stations_list = [str(item).strip() for item in split_string]

        #save the coordinates of every station passed in a trajectory
        for station in stations_list:

            #Add every x and y coordinate to a list
            y = station_coordinates[station][0]
            x = station_coordinates[station][1]

            x_coordinates.append(x)
            y_coordinates.append(y)

            #plot a line for every trajectory
        plt.plot(x_coordinates, y_coordinates, label = row.iloc[0], linestyle="--")


    plt.title("NS trajectories in North and south Holland", fontsize=14)
    plt.xlabel("Longitude (x)", fontsize=12)
    plt.ylabel("Latitude (y)", fontsize=12)
    plt.legend(loc='best', fontsize=8)

    return plt.show()
