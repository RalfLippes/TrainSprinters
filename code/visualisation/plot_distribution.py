import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import random
from ..algorithms.baseline import create_trajectories
from code.classes.oplossing_class import Solution

def plot_distribution(data, bins_amount, title, xlabel, plot_name):
    plt.figure(figsize=(8, 6))
    sns.histplot(data, kde=True, bins=bins_amount, color='skyblue', label='Histogram with KDE', kde_kws={'bw_adjust': 1.5})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig(plot_name)
    plt.show()


def prepare_data_baseline(all_connections_number, iterations, full_connection_dict, original_connection_dict,
    possible_directions, choose_random_connections, max_connections, max_duration, min_trains, max_trains):
    # get statistics from random samples of solutions
    results = []
    total_score = []
    total_connections = []

    loop_range = range(min_trains, max_trains + 1)

    for i in loop_range:
        score = []
        connections = []
        duration = []
        highest_score = 0

        fully_connected_iterations = 0
        for j in range(iterations):
            solution = Solution()
            for number in range(i):
                solution.add_trajectory(choose_random_connections(full_connection_dict,
                    possible_directions, max_connections, max_duration))

            connection_number = solution.amount_connection(original_connection_dict)
            current_df = solution.create_dataframe_from_solution(original_connection_dict,
                all_connections_number)

            score.append(current_df['stations'].iloc[-1])
            total_score.append(current_df['stations'].iloc[-1])

            connections.append(connection_number)
            total_connections.append(connection_number)

            if connection_number == all_connections_number:
                fully_connected_iterations += 1

            if current_df['stations'].iloc[-1] > highest_score:
                highest_score = current_df['stations'].iloc[-1]


        print(f"average score for {i} trajectories is {sum(score) / iterations}")
        print(f"highest score = {highest_score}")


        results.append({
            'Trajectories': i,
            'Average Score': np.mean(score),
            'Median Score': np.median(score),
            'Std Dev Score': np.std(score),
            'Highest Score': highest_score,
            'Average Connections': np.mean(connections),
            'Median Connections': np.median(connections),
            'Std Dev Connections': np.std(connections),
            'Fully Connected Iteration': fully_connected_iterations
        })

    df = pd.DataFrame(results)

    average_row = df.mean(numeric_only=True)
    average_row = pd.DataFrame(average_row).T

    # Add a label for the average row
    average_row['Trajectories'] = 'Average'

    # Append the average row to the DataFrame
    df = pd.concat([df, average_row], ignore_index=True)

    return total_score, total_connections, df
