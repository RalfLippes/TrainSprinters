import random
import copy
import pandas as pd
from code.classes.traject_class import Trajectory
from code.classes.oplossing_class import Solution
from code.classes.verbinding_class import Connection
from code.algorithms.calculate_score import calculate_score

def choose_random_connections(connection_object_dict, possible_connections_dict,
    max_connections, max_duration):
    """
    Takes a dictionary with strings as keys in the form 'Startstation-Endstation'
    and values of connection objects. Makes a trajectory of n random connections,
    starting by choosing a random first station. Then repeats finding a random
    possible connection for 1 - max_connections times or until the time limit
    (120 minutes) would be reached. Returns the trajectory object.
    """
    trajectory = Trajectory()
    duration = 0

    # create given number of connection objects
    for i in range(random.randint(1, max_connections + 1)):

        if len(trajectory.connection_list) == 0:
            # start with a random connection and append its first station to the list
            connection_object = random.choice(list(connection_object_dict.values()))
            start_station = connection_object.start_station
            trajectory.add_connection(connection_object)
            duration += connection_object.duration

        # if not the first, start from previous station
        else:
            departure_station = trajectory.connection_list[-1].end_station

            # check possible stations and choose random connection
            possible_stations = possible_connections_dict[departure_station]
            chosen_station = random.choice(possible_stations)
            connection_object = connection_object_dict[departure_station + "-" + chosen_station]

            # create a copy of the possible station list before looping
            temp_possible_stations = copy.deepcopy(possible_stations)

            # if duration time goes over 120 enter a loop where we try other connections
            while duration + connection_object.duration > max_duration:

                # remove the station we already tried
                temp_possible_stations.remove(chosen_station)

                # return the objects if the list is empty after removing
                if len(list(temp_possible_stations)) == 0:
                    return trajectory

                # if not, choose a random station
                else:
                    chosen_station = random.choice(temp_possible_stations)
                    connection_object = connection_object_dict[departure_station + "-" + chosen_station]

            # add duration and connection
            duration += connection_object.duration
            trajectory.add_connection(connection_object)

    return trajectory

def create_trajectories(trajectory_amount, full_connection_dict, possible_directions,
    max_connections, max_duration):
    """
    Creates a solution using the random algorithm.
    """
    # create solution object
    solution = Solution()

    # create right amount of trajectories
    for i in range(trajectory_amount):
        current_trajectory = choose_random_connections(full_connection_dict,
            possible_directions, max_connections, max_duration)

        solution.add_trajectory(current_trajectory)

    return solution
