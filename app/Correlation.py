import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter
from dataloader import load_data, filter_data


def plot_correlation(merged_data: pd.DataFrame, protein_name: str):
    """
    Generate a scatter plot of MRSS vs Intensity with hover-over features.

    Parameters:
    - merged_data: Preprocessed data for plotting.
    - protein_name: Name of the protein for the plot title.

    Returns:
    - The Matplotlib figure object containing the plot.
    """
    # Extract relevant columns
    mrss = merged_data["mrss"]
    intensity = merged_data["Intensity"]
    condition = merged_data["condition"]

    # Ensure all intensities are positive for logarithmic scale
    if (intensity <= 0).any():
        raise ValueError("All intensity values must be positive for a logarithmic scale.")

    # Define custom colours for conditions
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red",
    }

    # Initialize plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Create scatter plot
    sns.scatterplot(
        x=mrss,
        y=intensity,
        hue=condition,
        s=100,
        palette=custom_palette,
        edgecolor="black",
        ax=ax,
    )

    # Set the y-axis to logarithmic scale
    ax.set_yscale("log")

    # Configure adaptive limits for y-axis
    y_min = intensity.min() * 0.8
    y_max = intensity.max() * 1.2
    ax.set_ylim(bottom=y_min, top=y_max)

    # Configure log ticks and formatter for y-axis
    ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=None, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):g}" if x >= 1 else f"{x:.1g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())  # Hide minor tick labels

    # Add hover-over annotations
    for i in range(len(merged_data)):
        plt.text(
            mrss.iloc[i],
            intensity.iloc[i],
            condition.iloc[i],
            fontsize=9,
            ha="center",
            va="center",
            color="black",
            bbox=dict(
                boxstyle="round,pad=0.2",
                edgecolor="black",
                facecolor=custom_palette.get(condition.iloc[i], "gray"),
                alpha=0.7,
            ),
        )

    # Title and labels
    plt.title(f"Correlation Plot for {protein_name}", fontsize=16, fontweight="bold")
    plt.xlabel("MRSS (Linear Scale)", fontsize=14)
    plt.ylabel("Intensity (Logarithmic Scale)", fontsize=14)
    plt.grid(which="both", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.show()

    return plt
