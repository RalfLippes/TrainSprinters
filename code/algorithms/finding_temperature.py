from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.annealing_steps import create_annealing_steps_trajectory
from code.algorithms.baseline import choose_random_connections
from code.classes.oplossing_class import Solution
import copy
import random
import pandas as pd

def find_best_temp_and_cooling(full_connection_dict, possible_directions,
    original_connection_dict, station_dictionary, max_duration, max_connections, min_trains,
    max_trains, total_connections, iterations, penalty_weight, temperature_values,
    cooling_rate_values):
    """
    Experiment function to try and find the best combination of temperature and
    cooling rate for the simulated annealing function. Runs the simulated annealing
    algorithm with different values of temperature and cooling rate and returns
    various a dataframe with the average score per combination of temperature and
    cooling rate.
    """
    solution_list = []
    combinations_dictionary = {}

    # create 50 solutions to test these on
    for i in range(50):
        solution = Solution()
        needed_connections_dict = copy.deepcopy(original_connection_dict)
        for a in range(random.randint(min_trains, max_trains)):
            current_trajectory, needed_connections_dict = create_annealing_steps_trajectory(
                station_locations, needed_connections_dict, possible_directions,
                full_connection_dict, penalty_weight, max_duration, max_connections)
            solution.add_trajectory(current_trajectory)
        solution_list.append(solution)

    # try every combination of temperature and cooling rate
    for temperature in temperature_values:
        print(f"current temperature: {temperature}")
        for cooling_rate in cooling_rate_values:
            print(f"current cooling rate: {cooling_rate}")
            combinations_dictionary[str(temperature) + '-' + str(cooling_rate)] = []
            # use current temperature and cooling rate to improve all 50 solutions
            for x in solution_list:
                # create trajectories according to how many are in original solution
                current_solution = simulated_annealing(x, choose_random_connections,
                    full_connection_dict, possible_directions, max_connections,
                    len(x.solution), temperature, cooling_rate, iterations,
                    original_connection_dict, max_duration)

                # add score to dictionary with scores
                combinations_dictionary[str(temperature) + '-' + str(cooling_rate)].append(
                    current_solution.calculate_solution_score(original_connection_dict,
                        total_connections))

    # flatten dictionary into a dataframe
    rows = []
    for key, scores in combinations_dictionary.items():
        # split keys into temperature and cooling rate
        temp, cooling = map(float, key.split('-'))
        for score in scores:
            rows.append({'Temperature': temp, 'Cooling Rate': cooling, 'Score': score})

    # create DataFrame
    df = pd.DataFrame(rows)

    return df
