import random
import copy
import math
from code.algorithms.annealing_steps import annealing_cost_function
from code.algorithms.baseline import choose_random_connections
from code.other_functions.calculate_score import calculate_score
from code.classes.oplossing_class import Solution

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

def accept_step(old_score, new_score, temperature):
    """
    Takes the cost of the old step and the cost of the new step, as well as the
    current temperature. Decides if the new step will be accepted by using the
    simulated annealing criterion. Returns true or false according to acceptance.
    """
    score_difference = new_score - old_score

    # if new score is lower, accept with a probability
    if score_difference <= 0:
        try:
          exponent = score_difference / temperature
          criterion = math.exp(exponent)
          return random.random() < criterion

        except OverflowError:
        # if exponent is too large it will cause errors
            return False

    # if new solution is better, always accept
    else:
        return True

def simulated_annealing(trajectories, connection_function, connection_object_dict,
    possible_connections_dict, connection_amount, trajectory_amount, temperature,
    cooling_rate, iterations, original_connection_dict):
    """
    Takes a list of trajectory objects. Removes 1 trajectory and makes a new one.
    Calculates score of current and new trajectory and uses acceptance function
    to decide if new step is accepted. Repeats until temperature is 0.
    """
    final_solution = Solution()

    # set current objects to input values
    current_trajectories = trajectories.solution
    current_connections = trajectories.amount_connection(original_connection_dict)
    current_duration = find_duration(current_trajectories)
    current_score = calculate_score(current_connections, trajectory_amount,
        current_duration, total_connections = 28)

    for i in range(iterations):
        # remove random trajectory from list
        new_trajectories = copy.deepcopy(current_trajectories)
        new_trajectories.pop(random.randrange(len(new_trajectories)))

        # create new random trajectory
        trajectory = connection_function(connection_object_dict, possible_connections_dict,
            connection_amount)

        # add trajectory to the schedule
        new_trajectories.append(trajectory)

        # calculate new score
        new_connections = find_connection_amount(new_trajectories, original_connection_dict)
        new_duration = find_duration(new_trajectories)
        new_score = calculate_score(new_connections, trajectory_amount,
            new_duration, total_connections = 28)

        # check if new step is accepted
        if accept_step(current_score, new_score, temperature):
            current_trajectories = new_trajectories
            current_connections = new_connections
            current_score = new_score

        # decrease temperature
        temperature *= cooling_rate

        #print(f"Iteration {i+1}: Score = {current_score}, Temperature = {temperature}")

    for trajectory in current_trajectories:
        final_solution.add_trajectory(trajectory)

    return final_solution
