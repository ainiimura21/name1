import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Updated Volcano Plot Function
def plot_volcano(data):
    # Ensure required columns exist
    required_columns = ["logFC", "P.Value", "Target"]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data is missing required columns: {required_columns}")

    # Calculate -log10(p-value)
    data['-log10_pvalue'] = -np.log10(data['P.Value'])

    # Define thresholds
    fold_change_threshold = 0.6  # Adjust as needed
    pvalue_threshold = 0.05  # Adjust as needed
    data['Significant'] = (np.abs(data['logFC']) > fold_change_threshold) & (data['P.Value'] < pvalue_threshold)

    # Create the volcano plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        data=data,
        x='logFC',
        y='-log10_pvalue',
        # hue='Significant',
        palette={True: 'red', False: 'grey'},
        legend=False
    )

    # Add vertical and horizontal threshold lines
    plt.axvline(x=-fold_change_threshold, linestyle='--', color='blue', linewidth=1)
    plt.axvline(x=fold_change_threshold, linestyle='--', color='blue', linewidth=1)
    plt.axhline(y=-np.log10(pvalue_threshold), linestyle='--', color='green', linewidth=1)

    # Label the plot
    plt.title("Volcano Plot", fontsize=16)
    plt.xlabel("Log2 Fold Change", fontsize=14)
    plt.ylabel("-Log10 P-value", fontsize=14)

    # Annotate significant points with protein names
    significant_points = data[data['Significant']]
    for _, row in significant_points.iterrows():
        plt.text(row['logFC'], row['-log10_pvalue'], row['Target'], fontsize=9)

    plt.tight_layout()
    return plt
