import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

def plot_boxplot(merged_data, metadata_info, protein_name):
    """
    Create a boxplot of the intensity of 4 Scleroderma categories with a logarithmic scale.
    """
    # Filter data by conditions
    conditions = ["Healthy", "VEDOSS", "SSC_low", "SSC_high"]
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red"
    }

    # Extract intensity values for each condition
    data = [merged_data[merged_data['condition'] == condition]["Intensity"] for condition in conditions]

    # Ensure no zeros or negatives for logarithmic scale
    for i, condition_data in enumerate(data):
        if (condition_data <= 0).any():
            raise ValueError(f"Condition '{conditions[i]}' contains zero or negative values, which are invalid for a logarithmic scale.")

    # Create the boxplot
    fig, ax = plt.subplots(figsize=(12, 8))
    bp = ax.boxplot(data, patch_artist=True)

    # Set colors for the boxes
    for patch, condition in zip(bp['boxes'], conditions):
        patch.set_facecolor(custom_palette[condition])

    # Set median line colors
    for median in bp['medians']:
        median.set_color('black')

    # Set logarithmic y-axis
    ax.set_yscale("log")
    y_min = min([d.min() for d in data]) * 0.8
    y_max = max([d.max() for d in data]) * 1.2
    ax.set_ylim(bottom=y_min, top=y_max)

    # Configure ticks and formatters
    ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=None, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):g}" if x >= 1 else f"{x:.1g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())


    ax.set_title(f"Box Plot for {protein_name}", fontsize=16)
    ax.set_xticks(range(1, 5))
    ax.set_xticklabels(conditions)
    ax.set_ylabel("Intensity (Logarithmic Scale)", fontsize=12)
    ax.grid(visible=True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Plot graph
    plt.show()

    return plt
