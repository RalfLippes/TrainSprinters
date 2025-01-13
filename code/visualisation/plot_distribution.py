import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(data, bins_amount, title, xlabel):
    plt.figure(figsize=(8, 6))
    sns.histplot(data, kde=True, bins=bins_amount, color='skyblue', label='Histogram with KDE')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()
