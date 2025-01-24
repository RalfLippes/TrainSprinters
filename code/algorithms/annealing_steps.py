# import pandas as pd
import math
import random
import copy
from code.classes.traject_class import Trajectory
from code.classes.oplossing_class import Solution
# from code.other_functions.calculate_score import calculate_score
"""
Algorithm that tries to minimize the distance between the current station and
the station where a connection begins that has not been ridden yet using
a sort of simulated annealing algorithm.
"""

def annealing_cost_function(station_dictionary, current_station, step_station,
    destination, full_connection_dict, penalty_weight, total_duration, max_duration):
    """
    Calculates the cost of riding a connection. Checks the distance, and penalizes
    for the duration of the connection.
    Cost function is euclidean distance + penalty weight * 1 if connection has
    already been ridden and    distance + penalty weight * 0 if connection is still
    needed. Returns the cost.
    """
    # check if total duration goes over max duration
    if total_duration + full_connection_dict[current_station + '-' + step_station].duration > max_duration:
        return math.inf

    # get both station objects
    station_1 = station_dictionary[step_station]
    station_2 = station_dictionary[destination]

    # calculate euclidean distance
    euclidean_distance = math.sqrt((station_2.x - station_1.x) ** 2 + (station_2.y - station_1.y) ** 2)

    duration = full_connection_dict[current_station + '-' + step_station].duration

    # calculate outcome of cost function
    cost = euclidean_distance + penalty_weight * duration

    return cost

def accept_solution(old_cost, new_cost, temperature):
    """
    Takes the cost of the old step and the cost of the new step, as well as the
    current temperature. Decides if the new step will be accepted by using the
    simulated annealing criterion. Returns true or false according to acceptance.
    """
    cost_difference = new_cost - old_cost

    # if new solution is better, always accept
    if cost_difference < 0:
        return True

    # if the new solution is worse, accept with a probability
    else:
        # Calculate the acceptance criterion
        criterion = math.exp(-cost_difference / temperature)

        # accept only if criterion is larger than random number between 0-1
        return random.random() < criterion

def find_nearest_connection(station_dictionary, current_station, needed_connections_dict):
    """
    Finds the nearest connection in needed_connections_dict hat has not been ridden.
    Uses current station to calculate distances. Returns the closest 'new' connection
    as an object.
    """
    x1, y1 = current_station.x, current_station.y
    closest_distance = math.inf
    closest_connection = None

    # check which needed connection is closest to current station
    for connection in needed_connections_dict:
        x2 = station_dictionary[needed_connections_dict[connection].start_station].x
        y2 = station_dictionary[needed_connections_dict[connection].start_station].y
        euclidean_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # check if better than current best, then save distance and connection object
        if euclidean_distance < closest_distance:
            closest_distance = euclidean_distance
            closest_connection = needed_connections_dict[connection]

    return closest_connection

def trim_trajectory(trajectory, needed_connections_dict):
    """
    Trims the trajectory list by removing all connections after the last one
    that exists in needed_connections_dict.
    Takes a trajectory list of connection objects and a dictionary with
    'station1-station2' as keys and connection objects as values. Returns list of
    trimmed connection objects.
    """
    last_valid_index = -1
    # iterate backwards through the trajectory to find the last valid connection
    for index in range(len(trajectory.connection_list) - 1, -1, -1):
        connection = trajectory.connection_list[index]
        key = f"{connection.start_station}-{connection.end_station}"

        if key in needed_connections_dict:
            # keep track of the last valid index
            last_valid_index = index
            break

    if last_valid_index != -1:
        trajectory.keep_connections(last_valid_index)

    return trajectory

def initialize_trajectory(station_dictionary, needed_connections_dict, max_connections):
    """Initializes the trajectory with a random starting connection."""
    trajectory = Trajectory()
    new_needed_connections_dict = copy.deepcopy(needed_connections_dict)
    total_duration = 0
    temperature = max_connections

    # return if no connections are needed
    if not new_needed_connections_dict:
        return trajectory, new_needed_connections_dict, total_duration, None, temperature

    # choose first connection at random (from connections that are still needed)
    first_connection = new_needed_connections_dict[random.choice(list(new_needed_connections_dict))]

    # add information to variables
    trajectory.add_connection(first_connection)
    total_duration += first_connection.duration
    current_station = station_dictionary[first_connection.end_station]

    # remove connection from needed connections
    new_needed_connections_dict.pop(first_connection.start_station + '-' + first_connection.end_station)

    return trajectory, new_needed_connections_dict, total_duration, current_station, temperature

def attempt_direct_connection(station_dictionary, current_station, nearest_connection, total_duration,
    new_needed_connections_dict, trajectory, full_connection_dict, temperature):
    """Attempts to connect directly to the nearest connection's start station."""
    # check if station is start point of nearest connection
    if current_station.name == nearest_connection.start_station:
        if total_duration + nearest_connection.duration <= 120:
            # if riding connection is possible, add info to variables
            total_duration += nearest_connection.duration
            new_needed_connections_dict.pop(current_station.name + '-' +
                nearest_connection.end_station)
            current_station = station_dictionary[nearest_connection.end_station]
            current_connection = nearest_connection
            if (not trajectory.connection_list or
                trajectory.connection_list[-1].end_station != nearest_connection.end_station):
                trajectory.add_connection(nearest_connection)

            return (trajectory, new_needed_connections_dict, total_duration,
                temperature - 1, current_station, True)

        # if it goes over time, trajectory is done
        else:
            trajectory = trim_trajectory(trajectory, new_needed_connections_dict)
            return (trajectory, new_needed_connections_dict, total_duration, temperature,
                None, True)

    # check if connection to start of nearest connection is possible
    connection_key = current_station.name + '-' + nearest_connection.start_station
    if connection_key in full_connection_dict:
        # check if this connection can be ridden
        if total_duration + full_connection_dict[connection_key].duration <= 120:
            # if so, add info
            total_duration += full_connection_dict[connection_key].duration
            if connection_key in new_needed_connections_dict:
                 new_needed_connections_dict.pop(connection_key)
            current_station = station_dictionary[nearest_connection.start_station]
            current_connection = full_connection_dict[connection_key]
            trajectory.add_connection(current_connection)
            return (trajectory, new_needed_connections_dict, total_duration,
                temperature - 1, current_station, True)

        # if it goes over time, trajectory is done
        else:
            trajectory = trim_trajectory(trajectory, new_needed_connections_dict)
            return (trajectory, new_needed_connections_dict, total_duration, temperature,
                None, True)

    return (trajectory, new_needed_connections_dict, total_duration, temperature,
        current_station, False)

def find_best_annealing_move(current_station, nearest_connection, total_duration,
    new_needed_connections_dict, trajectory, full_connection_dict, temperature,
    station_dictionary, penalty_weight, max_duration):
    """Does a random move and checks if that move will be executed."""
    possible_connections = [key.split('-')[1]
        for key in full_connection_dict if key.split('-')[0] == current_station.name]
    accepted_any = False

    # randomize order of possible connections
    random_connections = copy.copy(possible_connections)
    random.shuffle(random_connections)

    # check every connection possible
    for random_station in random_connections:
        if random_station == current_station.name:
            continue

        # skip connections that are not possible
        connection_key = current_station.name + '-' + random_station
        if connection_key not in full_connection_dict:
            continue

        # check current and step cost
        current_connection = trajectory.connection_list[-1]
        current_cost = annealing_cost_function(station_dictionary,
            current_connection.start_station, current_station.name,
            nearest_connection.start_station, full_connection_dict,
            penalty_weight, total_duration, max_duration)
        station_cost = annealing_cost_function(station_dictionary,
            current_station.name, random_station,
            nearest_connection.start_station, full_connection_dict,
            penalty_weight, total_duration, max_duration)

        # decide if the new step will be accepted
        if temperature == 0:
            acceptance = False
        else:
            acceptance = accept_solution(current_cost, station_cost, temperature)

        # check next station if it is not accepted
        if not acceptance:
            continue

        # if accepted, check if step can be made
        accepted_any = True
        connection_to_add = full_connection_dict[connection_key]
        if total_duration + connection_to_add.duration <= 120:
            # add connection info to variables
            total_duration += connection_to_add.duration
            if connection_key in new_needed_connections_dict:
                new_needed_connections_dict.pop(connection_key)
            current_station = station_dictionary[random_station]
            current_connection = connection_to_add
            trajectory.add_connection(connection_to_add)
            temperature -= 1

            break

    return (trajectory, new_needed_connections_dict, total_duration, temperature,
        current_station, accepted_any)

def move_towards_nearest_connection(station_dictionary, current_station, nearest_connection,
    total_duration, new_needed_connections_dict, trajectory, full_connection_dict,
    max_duration, temperature, penalty_weight):
    """Tries to move toward the nearest connection."""
    at_destination = False
    max_attempts = 1000
    attempts = 0

    # keep trying while we're not at the destination
    while not at_destination:
        attempts += 1
        if attempts > max_attempts:
            temperature = 0
            break

        # check if we can make a direct connection to nearest connection
        (trajectory, new_needed_connections_dict, total_duration, temperature,
        new_current_station, at_destination) = attempt_direct_connection(
            station_dictionary, current_station, nearest_connection,
            total_duration, new_needed_connections_dict, trajectory,
            full_connection_dict, temperature)

        # check if new_current_station is None, return if it is
        if new_current_station is None:
            return (trajectory, new_needed_connections_dict, total_duration,
                temperature, new_current_station, True)

        current_station = new_current_station

        # if we reached the destination, return values
        if at_destination:
            break

        # if not, do annealing on random possible steps we can take
        (trajectory, new_needed_connections_dict, total_duration, temperature,
        current_station, accepted_any) = find_best_annealing_move(current_station,
            nearest_connection, total_duration, new_needed_connections_dict,
            trajectory, full_connection_dict, temperature, station_dictionary,
            penalty_weight, max_duration)

        # if nothing is accepted, trajectory is done
        if not accepted_any:
            temperature = 0
            break

    return (trajectory, new_needed_connections_dict, total_duration, temperature,
        current_station, False)

def create_annealing_steps_trajectory(station_dictionary, needed_connections_dict,
    possible_connections_dict, full_connection_dict, penalty_weight, max_duration,
    max_connections):
    """
    Creates a trajectory using the 'annealing steps' algorithm.
    """
    # initialize the trajectory
    (trajectory, new_needed_connections_dict, total_duration, current_station,
    temperature) = initialize_trajectory(station_dictionary, needed_connections_dict,
        max_connections)

    # keep looping while temp is above 0 and there are connections needed
    while temperature != 0 and len(new_needed_connections_dict) > 0:
        nearest_connection = find_nearest_connection(station_dictionary,
            current_station, new_needed_connections_dict)

        (trajectory, new_needed_connections_dict, total_duration, temperature,
        current_station, time_limit_exceeded) = move_towards_nearest_connection(
            station_dictionary, current_station, nearest_connection, total_duration,
            new_needed_connections_dict, trajectory, full_connection_dict,
            max_duration, temperature, penalty_weight)

        if time_limit_exceeded:
              break

    # remove stations after last needed station (since those aren't necessary)
    trajectory = trim_trajectory(trajectory, needed_connections_dict)
    return trajectory, new_needed_connections_dict

def create_solution_annealing(station_locations, original_connection_dict,
    possible_directions, full_connection_dict, penalty_weight,
    max_duration, max_connections, trajectory_amount):
    """
    Runs annealing steps for a certain amount of iterations to create a solution.
    Returns this solution object.
    """
    # create solution object to store trajectories
    solution = Solution()
    needed_connections_dict = copy.deepcopy(original_connection_dict)

    # create right amount of trajectories
    for trajectory in range(trajectory_amount):
        current_trajectory, needed_connections_dict = create_annealing_steps_trajectory(
            station_locations, needed_connections_dict, possible_directions,
            full_connection_dict, penalty_weight, max_duration, max_connections)

        # add trajectory to solution
        solution.add_trajectory(current_trajectory)

    return solution
