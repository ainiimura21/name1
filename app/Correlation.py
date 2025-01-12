import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter
from dataloader import load_data, filter_data

def plot_correlation(merged_data, protein_name):
    """
    Create a scatter plot of MRSS (linear scale) vs Intensity (logarithmic scale)
    with condition-specific colors for points and traditional logarithmic value markers.

    Parameters:
    - filtered_data (pd.DataFrame): DataFrame containing filtered protein intensity data merged with the corresponding
    metadata.
    - protein_name (str): Name of the protein for the plot title.

    Returns:
    - plt.Figure: The Matplotlib figure object containing the plot.
    """
    merged_data = merged_data
    # Extract relevant columns
    mrss = merged_data["mrss"]
    intensity = merged_data["Intensity"]
    condition = merged_data["condition"]

    # Data Validation: Ensure all Intensities are positive
    if (intensity <= 0).any():
        num_invalid = (intensity <= 0).sum()
        raise ValueError(f"Intensity contains {num_invalid} non-positive values. "
                         "Logarithmic scale requires all values to be positive.")

    # Define custom colors for conditions
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red"
    }

    # Initialize the plot
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
        ax=ax
    )

    # Set the y-axis to logarithmic scale
    ax.set_yscale("log")

    # Configure adaptive limits for y-axis
    y_min = intensity.min() * 0.8
    y_max = intensity.max() * 1.2
    ax.set_ylim(bottom=y_min, top=y_max)

    # Configure log ticks and formatter for y-axis (fixing log10 display issues)
    ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=None, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):g}" if x >= 1 else f"{x:.1g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())  # Hide minor tick labels

    # Add color-coded annotations for each point
    for i in range(len(merged_data)):
        plt.text(
            mrss.iloc[i],
            intensity.iloc[i],
            condition.iloc[i],  # Text is the condition
            fontsize=9,
            ha="center",
            va="center",
            color="black",
            bbox=dict(
                boxstyle="round,pad=0.2",
                edgecolor="black",
                facecolor=custom_palette.get(condition.iloc[i], "gray"),
                alpha=0.7
            )
        )

    # Set title and labels with appropriate font sizes
    plt.title(f"Correlation Plot for {protein_name}", fontsize=16, fontweight='bold')
    plt.xlabel("MRSS (Linear Scale)", fontsize=14)
    plt.ylabel("Intensity (Logarithmic Scale)", fontsize=14)

    # Customize grid for better readability
    plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust legend
    plt.legend(title="Condition", fontsize=12, title_fontsize=13, loc="best")

    # Optimize layout
    plt.tight_layout()

    # Display the plot
    plt.show()

    return plt