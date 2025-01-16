import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import ast
import re

def create_map(trajectories, station_locations):
    """
    this function takes a csv file that includes the y,x coordinates of different
    stations and a dataframe that includes each train with its trajectory. Returns
    a plotted graph of all trajectories showing which cities they pass.
    """

    stations = pd.read_csv(station_locations)

    coordinates_stations = {}

    # Create a single plot
    plt.figure(figsize=(6, 10))

    for index, row in stations.iterrows():

        #safe the name of the station name and its coordinates in a dictionary for easy access
        coordinates_stations[row.iloc[0]]= [row.iloc[1], row.iloc[2]]


        plt.scatter(row.iloc[2], row.iloc[1], color='blue', marker='x')
        plt.text(row.iloc[2], row.iloc[1] - 0.02, row.iloc[0], fontsize=8)


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
            y = coordinates_stations[station][0]
            x = coordinates_stations[station][1]

            x_coordinates.append(x)
            y_coordinates.append(y)

            #plot a line for every trajectory
        plt.plot(x_coordinates, y_coordinates, label = row.iloc[0])


    plt.title("NS trajectories in North and south Holland", fontsize=14)
    plt.xlabel("Longitude (x)", fontsize=12)
    plt.ylabel("Latitude (y)", fontsize=12)
    plt.legend(loc='best', fontsize=8)

    return plt.show()
