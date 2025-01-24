from code.other_functions.load_data import get_possible_directions
from code.other_functions.create_connection_dict import create_connections
from code.algorithms.n_deep_algorithm import n_deep_algorithm, create_deep_trajectories
#
# from code.algorithms.annealing_steps import load_station_location_data, annealing_cost_function, find_nearest_connection, create_annealing_steps_trajectory, create_dataframe_annealing
# from code.other_functions.load_data import get_possible_directions
# from code.other_functions.create_connection_dict import create_connections


import copy

def run_n_deep_algorithm(iterations, depth, loading_popup=False):
    # Load data and prepare variables
    possible_directions, corrected_df, original_df = get_possible_directions("data/Noord_Holland/ConnectiesHolland.csv")
    full_connection_dict = create_connections(corrected_df)
    original_connection_dict = create_connections(original_df)

    avg_scores = {}
    highest_scores = {}
    best_dataframe = []

    for i in range(4, 8):
        total_score = 0  # Initialize total score for the current trajectory amount
        highest_score = float('-inf')  # Initialize the highest score for this trajectory amount

        for j in range(iterations):
            needed_connections_dict = copy.deepcopy(original_connection_dict)
            possible_connections_dict = possible_directions


            dataframe, connections_made = create_deep_trajectories(
                trajectory_amount=i,
                connection_algorithm=n_deep_algorithm,
                full_connection_dict=full_connection_dict,
                original_connection_dict=original_connection_dict,
                needed_connections_dict=needed_connections_dict,
                arg1=full_connection_dict,
                arg2=possible_connections_dict,
                arg3=needed_connections_dict,
                arg4=depth)

            score = dataframe.loc[dataframe.index[-1], 'stations']
            total_score += score

            # Update highest score if the current score is higher
            if score > highest_score:
                highest_score = score
                best_dataframe = dataframe

            if loading_popup == True:
                if j % (iterations/10) == 0 and j > 0:
                    print(f"Traject {i}: {j} iteration completed...")

        # Calculate the average score for the current trajectory amount
        avg_scores[i] = total_score / iterations
        highest_scores[i] = highest_score  # Store the highest score for the current trajectory amount


        print(f"Average score for {i} trajectories: {avg_scores[i]}")
        print(f"Highest score for {i} trajectories: {highest_scores[i]}")
    print(best_dataframe)

    best_dataframe.to_csv("output2.csv", index=False)

    return avg_scores, highest_scores, best_dataframe
