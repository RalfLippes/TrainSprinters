import random
import copy
import math
from code.algorithms.baseline import choose_random_connections
from code.algorithms.calculate_score import calculate_score
from code.classes.oplossing_class import Solution
import matplotlib.pyplot as plt


def find_connection_amount(trajectories, original_connection_dict):
    """
    Finds the number of unique needed connections in the schedule of trajectories.
    """
    original_connections = set()
    for trajectory in trajectories:
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

def hill_climber(trajectories, connection_function, connection_object_dict,
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


    iterations = list(range(1, len(scores) + 1))

    # create a plot of scores vs iteration
    plt.plot(iterations, scores, linestyle='-', color='b', label='High Scores')
    plt.title('High Scores vs Iterations')
    plt.xlabel('Iteration Number')
    plt.ylabel('High Score')
    plt.xlim(0, len(scores))

    plt.show()



    for trajectory in current_trajectories:
        final_solution.add_trajectory(trajectory)

    return final_solution
