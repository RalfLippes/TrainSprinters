import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_temp_cool_scores(scores_dataframe, title):
    heatmap_data = scores_dataframe.groupby(['Temperature', 'Cooling Rate'])['Score'].mean().unstack()

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot = True, cmap = 'viridis', fmt = ".2f")
    plt.title(title)
    plt.xlabel('Cooling Rate')
    plt.ylabel('Temperature')
    plt.savefig("data/output/cooling_rates_and_temperatures.png")
