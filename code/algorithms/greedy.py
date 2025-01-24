import random
import pandas as pd
import copy
from code.classes.verbinding_class import Connection
from code.classes.traject_class import Trajectory
from code.classes.oplossing_class import Solution
from code.other_functions.calculate_score import calculate_score

def generate_trajectory(full_connection_dict, possible_directions,
    needed_connections_dict):
    """
    generates a random trajectory by preferring to choose from the connections that
    have not been chosen yet (provided in needed_connections). Takes a dictionary
    with connections that haven't been ridden yet, a dictionary with all possible
    connections and a dictionary with all possible target station from each possible
    starting station. Returns list of connection objects (trajectory) and the updated
    needed connections dictionary.
    """
    trajectory = Trajectory()
    duration = 0
    new_needed_connections_dict = copy.deepcopy(needed_connections_dict)
    complete = False

    while not complete:
        # if there are no connections yet, choose a random one that is available
        if len(trajectory.connection_list) <= 0:
            # check if all connections have been ridden, stop if they are
            if len(new_needed_connections_dict) == 0:
                complete = True
                break

            # create random connection and store values
            connection_object = random.choice(list(new_needed_connections_dict.values()))
            start_station = connection_object.start_station
            trajectory.add_connection(connection_object)
            duration += connection_object.duration
            new_needed_connections_dict.pop(start_station + '-' +
                connection_object.end_station)

        # if we have >0 objects, go on from the end station of the previous connection
        else:
            length_before = len(trajectory.connection_list)
            departure_station = trajectory.connection_list[-1].end_station

            # randomize connections and append if it is still needed
            possible_stations = possible_directions[departure_station]
            random.shuffle(possible_stations)
            for station in possible_stations:
                if departure_station + '-' + station in new_needed_connections_dict:
                    connection_object = new_needed_connections_dict[departure_station
                        + "-" + station]

                    # if duration time goes over 120: don't add connection and go to next one
                    if duration + connection_object.duration > 120:
                        continue

                    # add object, count duration and remove connection from needed connections
                    trajectory.add_connection(connection_object)
                    duration += connection_object.duration
                    new_needed_connections_dict.pop(departure_station + '-' + station)
                    break

            # check if previous loop has added any connections
            length_after = len(trajectory.connection_list)
            if length_after == length_before:
                # go through random order of possible connections
                random.shuffle(possible_stations)
                for station in possible_stations:
                    chosen_station = station
                    connection_object = full_connection_dict[departure_station + "-" +
                    chosen_station]

                    # if duration time goes over 120: go to next connection
                    if duration + connection_object.duration > 120:
                        continue

                    # if valid, count duration and add connection object to list
                    duration += connection_object.duration
                    trajectory.add_connection(connection_object)

                complete = True

    return trajectory, new_needed_connections_dict

def create_better_trajectories(trajectory_amount, full_connection_dict,
    original_connection_dict, needed_connections_dict, possible_directions):
    """
    Creates a given number of trajectories. Uses greedy algorithm to select
    connections for the trajectories. Returns a solution object.
    """
    # create a solution object
    solution = Solution()
    needed_connections = copy.deepcopy(needed_connections_dict)

    # create right amount of trajectories
    for i in range(trajectory_amount):

        # find connections according to the given connection algorithm
        if len(needed_connections) > 0:
            current_connections, needed_connections = generate_trajectory(
                full_connection_dict, possible_directions, needed_connections_dict)

        solution.add_trajectory(current_connections)

    return solution
