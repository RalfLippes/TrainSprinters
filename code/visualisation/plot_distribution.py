import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from ..algorithms.baseline import create_trajectories

def plot_distribution(data, bins_amount, title, xlabel):
    plt.figure(figsize=(8, 6))
    sns.histplot(data, kde=True, bins=bins_amount, color='skyblue', label='Histogram with KDE', kde_kws={'bw_adjust': 1.5})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

def prepare_data_baseline(iterations, full_connection_dict, original_connection_dict, possible_directions, choose_random_connections):
    # get statistics from random samples of solutions
    results = []
    total_score = []
    total_connections = []

    for i in range(4,8):
        score = []
        connections = []
        duration = []
        highest_score = 0

        fully_connected_iterations = 0
        for j in range(iterations):
            current_df, connection_number = create_trajectories(
                i, choose_random_connections, full_connection_dict,
                original_connection_dict, full_connection_dict, possible_directions)


            score.append(current_df['stations'].iloc[-1])
            total_score.append(current_df['stations'].iloc[-1])

            connections.append(connection_number)
            total_connections.append(connection_number)

            if connection_number == 28:
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

    # Add a label for the average row
    average_row['Trajectories'] = 'Average'

    # Append the average row to the DataFrame
    df = pd.concat([df, pd.DataFrame([average_row])])

    # Display the DataFrame
    print(df)

    return total_score, total_connections, df
