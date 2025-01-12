import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dataloader import load_data, filter_data

def plot_boxplot(merged_data, protein_name):
    """
    Create a boxplot of the intensity of 4 Scleroderma categories
    """
    merged_data = merged_data
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
    # Extract the intensity values for all 4 catagories
    data_healthy = data_healthy["Intensity"]
    data_VEDOSS =data_VEDOSS["Intensity"]
    data_SSClow = data_SSClow["Intensity"]
    data_SSChigh = data_SSChigh["Intensity"]
    data = [data_healthy, data_VEDOSS, data_SSClow, data_SSChigh]
    fig = plt.figure(figsize =(10, 7))

    ax = fig.add_axes([0, 0, 1, 1])

    # Creating plot
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
