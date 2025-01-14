import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_boxplot(filtered_data, metadata_info, protein_name):
    # Merge filtered_data with metadata_info on SampleId
    merged_data = pd.merge(
        filtered_data,
        metadata_info,
        left_on="SampleId",
        right_on="SubjectID",
        how="inner"
    )

    # Debug: Print merged data
    print("Merged Data:")
    print(merged_data.head())

    # Create sub datasets for each condition
    conditions = ["Healthy", "VEDOSS", "SSC_low", "SSC_high"]
    data = [merged_data[merged_data['condition'] == condition]["Intensity"] for condition in conditions]

    # Check if any condition is missing data
    for condition, condition_data in zip(conditions, data):
        if condition_data.empty:
            print(f"Warning: No data for {condition}. This condition will be skipped.")

    # Define custom colours for conditions
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red"
    }

    # Create the boxplot
    fig, ax = plt.subplots(figsize=(10, 7))
    bp = ax.boxplot(data, patch_artist=True)

    # Set colours for boxes based on conditions
    for patch, condition in zip(bp['boxes'], conditions):
        patch.set_facecolor(custom_palette[condition])

    # Set the title and labels before calling show
    plt.title(f"Box Plot for {protein_name}", fontsize=16)
    plt.xticks([1, 2, 3, 4], conditions)
    plt.ylabel("Intensity", fontsize=12)
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Set black colour for the medians
    for median in bp['medians']:
        median.set_color('black')

    # Show the plot
    plt.show()

    return plt
