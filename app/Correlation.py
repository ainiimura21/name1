import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dataloader import load_data, filter_data

def plot_correlation(merged_data, protein_name):
    """
    Create a scatter plot of MRSS (linear scale) vs Intensity (logarithmic scale)
    with condition-specific colors for points and tags.
    """
    merged_data = merged_data

    # Extract relevant columns
    mrss = merged_data["mrss"]
    intensity = merged_data["Intensity"]
    condition = merged_data["condition"]

    # Log-transform intensity
    intensity_log = np.log10(intensity)

    # Define custom colors for conditions
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red"
    }

    # Create scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x=mrss, y=intensity_log, hue=condition, s=100, palette=custom_palette, edgecolor="black"
    )

    # Add color-coded annotations for each point
    for i in range(len(merged_data)):
        plt.text(
            mrss.iloc[i],
            intensity_log.iloc[i],
            condition.iloc[i],  # Text is the condition
            fontsize=10,
            ha="center",
            bbox=dict(
                boxstyle="round,pad=0.3",
                edgecolor="black",
                facecolor=custom_palette[condition.iloc[i]],  # Custom color for tag
                alpha=0.7
            ),
        )

    # Set title and labels
    plt.title(f"Correlation Plot for {protein_name}", fontsize=16)
    plt.xlabel("MRSS (Linear Scale)", fontsize=12)
    plt.ylabel("Intensity (Logarithmic Scale)", fontsize=12)
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    plt.legend(title="Condition", loc="best")
    plt.tight_layout()

    return plt



