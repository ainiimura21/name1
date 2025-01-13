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

    # Create 4 sub columns
    data_healthy = merged_data[merged_data['condition']== "Healthy"]
    data_VEDOSS =merged_data[merged_data['condition']==  "VEDOSS"]
    data_SSClow = merged_data[merged_data['condition']== "SSC_low"]
    data_SSChigh = merged_data[merged_data['condition']== "SSC_high"]

    # Define custom colors for conditions
    custom_palette = {
        "Healthy": "green",
        "VEDOSS": "violet",
        "SSC_low": "cyan",
        "SSC_high": "red"
    }
    # Extract the intensity values for all 4 categories
    data_healthy = data_healthy["Intensity"]
    data_VEDOSS =data_VEDOSS["Intensity"]
    data_SSClow = data_SSClow["Intensity"]
    data_SSChigh = data_SSChigh["Intensity"]
    data = [data_healthy, data_VEDOSS, data_SSClow, data_SSChigh]
    fig, ax = plt.subplots(figsize =(10, 7))
    bp = ax.boxplot(data, patch_artist=True)
    for median in bp['medians']:
        median.set_color('black')

    # show plot
    plt.show()

    # Set title and labels
    plt.title(f"Box Plot for {protein_name}", fontsize=16)
    plt.xticks([1,2,3,4], ['Healthy', 'VEDOSS', 'SSC_low', 'SSC_high'])
    plt.ylabel("Intensity", fontsize=12)
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    conditions = ["Healthy", "VEDOSS", "SSC_low", "SSC_high"]
    for patch, condition in zip(bp['boxes'], conditions):
        patch.set_facecolor(custom_palette[condition])
    return plt
