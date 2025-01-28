import random
import copy
import math
from code.algorithms.baseline import choose_random_connections
from code.algorithms.annealing_steps import create_annealing_steps_trajectory
from code.algorithms.calculate_score import calculate_score
from code.classes.oplossing_class import Solution
import matplotlib.pyplot as plt

def find_connection_amount(trajectories, original_connection_dict):
    """
    Finds the number of unique needed connections in the schedule of trajectories.
    """
    original_connections = set()
    for trajectory in trajectories:
        #print(trajectory)
        for connection in trajectory.connection_list:
            if connection.start_station + '-' + connection.end_station in original_connection_dict:
                connection_key = f"{connection.start_station}-{connection.end_station}"
                original_connections.add(connection_key)

    return len(original_connections)

def find_duration(trajectories):
    """Finds the total duration of all trajectories in a schedule"""
    total_duration = 0
    for trajectory in trajectories:
        for connection in trajectory.connection_list:
            total_duration += connection.duration

    return total_duration

def get_needed_connections(trajectories, original_connection_dict):
    """
    Finds the needed connections and return dictionary with needed connections.
    """
    new_connection_dict = copy.deepcopy(original_connection_dict)
    for trajectory in trajectories:
        for connection in trajectory.connection_list:
            connection_name = f"{connection.start_station} - {connection.end_station}"
            if connection_name in new_connection_dict:
                new_connection_dict.pop(connection_name)

    return new_connection_dict

def create_hill_climber_trajectory(station_dictionary, needed_connections_dict,
    possible_connections_dict, full_connection_dict, max_duration, max_connections,
    creating_algorithm):
    """
    Creates a new trajectory with either the baseline or the annealing_steps
    algorithm. Returns trajectory object.
    """
    if creating_algorithm == 'baseline':
        trajectory = choose_random_connections(full_connection_dict, possible_connections_dict,
            max_connections, max_duration)

    else:
        trajectory, temp = create_annealing_steps_trajectory(station_dictionary,
            needed_connections_dict, possible_connections_dict, full_connection_dict,
            max_duration, max_connections)

    return trajectory

def hill_climber(trajectories, connection_function, connection_object_dict,
    possible_connections_dict, connection_amount, trajectory_amount, iterations,
    original_connection_dict, max_duration, total_connections,
    creating_algorithm, station_dictionary):
    """
    Takes a list of trajectory objects. Removes 1 trajectory and makes a new one.
    Calculates score of current and new trajectory.
    """
    final_solution = Solution()

    scores = []

    # set current objects to input values
    current_trajectories = trajectories.solution
    current_connections = trajectories.amount_connection(original_connection_dict)
    current_duration = find_duration(current_trajectories)
    current_score = calculate_score(current_connections, trajectory_amount,
        current_duration, total_connections)

    for i in range(iterations):
        # remove random trajectory from list
        new_trajectories = copy.deepcopy(current_trajectories)
        new_trajectories.pop(random.randrange(len(new_trajectories)))

        # find the needed connections
        needed_connections = get_needed_connections(new_trajectories, original_connection_dict)

        # create new random trajectory
        trajectory = create_hill_climber_trajectory(station_dictionary, needed_connections,
            possible_connections_dict, connection_object_dict, max_duration, connection_amount,
            creating_algorithm)

        # add trajectory to the schedule
        new_trajectories.append(trajectory)

        # calculate new score
        new_connections = find_connection_amount(new_trajectories, original_connection_dict)
        new_duration = find_duration(new_trajectories)
        new_score = calculate_score(new_connections, trajectory_amount,
            new_duration, total_connections)

        if new_score > current_score:
            current_trajectories = new_trajectories
            current_connections = new_connections
            current_score = new_score

        scores.append(current_score)

    for trajectory in current_trajectories:
        final_solution.add_trajectory(trajectory)

    return final_solution

def find_best_iterations(trajectories, connection_function, connection_object_dict,
    possible_connections_dict, connection_amount, trajectory_amount, iterations,
    original_connection_dict, max_duration, total_connections):
    """
    Takes a list of trajectory objects. Removes 1 trajectory and makes a new one.
    Calculates score of current and new trajectory.
    """
    final_solution = Solution()

    scores = []

    # set current objects to input values
    current_trajectories = trajectories.solution
    current_connections = trajectories.amount_connection(original_connection_dict)
    current_duration = find_duration(current_trajectories)
    current_score = calculate_score(current_connections, trajectory_amount,
        current_duration, total_connections)

    for i in range(iterations):
        # remove random trajectory from list
        new_trajectories = copy.deepcopy(current_trajectories)
        new_trajectories.pop(random.randrange(len(new_trajectories)))

        # create new random trajectory
        trajectory = connection_function(connection_object_dict, possible_connections_dict,
            connection_amount, max_duration)

        # add trajectory to the schedule
        new_trajectories.append(trajectory)

        # calculate new score
        new_connections = find_connection_amount(new_trajectories, original_connection_dict)
        new_duration = find_duration(new_trajectories)
        new_score = calculate_score(new_connections, trajectory_amount,
            new_duration, total_connections)

        if new_score > current_score:
            current_trajectories = new_trajectories
            current_connections = new_connections
            current_score = new_score

        scores.append(current_score)

    return scores
