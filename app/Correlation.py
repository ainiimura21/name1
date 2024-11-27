import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(metadata_path, proteins_path):
    """
    Load metadata and protein data from the provided file paths.
    """
    metadata = pd.read_csv(metadata_path)
    proteins = pd.read_csv(proteins_path)
    return metadata, proteins


def filter_data(proteins, protein_id, id_type):
    """
    Filter the proteins data for a specific protein ID based on the ID type.
    """
    valid_columns = {
        "TargetFullName": "TargetFullName",
        "Target": "Target",
        "EntrezGeneID": "EntrezGeneID",
        "EntrezGeneSymbol": "EntrezGeneSymbol"
    }

    if id_type not in valid_columns:
        raise ValueError(f"Invalid ID type. Choose from {list(valid_columns.keys())}.")

    column_name = valid_columns[id_type]

    if column_name not in proteins.columns:
        raise KeyError(f"Column '{column_name}' not found in proteins data.")

    filtered_data = proteins[proteins[column_name] == protein_id]

    if filtered_data.empty:
        raise ValueError(f"No data found for {id_type} = {protein_id}.")

    return filtered_data


def plot_correlation(filtered_data, protein_name):
    """
    Create a scatter plot of MRSS (linear scale) vs Intensity (logarithmic scale)
    with color-coded SampleGroup and point annotations.
    """
    # Extract relevant columns
    mrss = filtered_data["mrss"]
    intensity = filtered_data["Intensity"]
    sample_group = filtered_data["SampleGroup"]

    # Log-transform intensity
    intensity_log = np.log10(intensity)

    # Create scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=mrss, y=intensity_log, hue=sample_group, s=100, palette="Set2")

    # Add annotations for each point
    for i in range(len(filtered_data)):
        plt.text(
            mrss.iloc[i],
            intensity_log.iloc[i],
            sample_group.iloc[i],
            fontsize=10,
            ha="center",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", alpha=0.3),
        )

    # Set title and labels
    plt.title(f"Correlation Plot for {protein_name}", fontsize=16)
    plt.xlabel("MRSS (Linear Scale)", fontsize=12)
    plt.ylabel("Intensity (Logarithmic Scale)", fontsize=12)
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    plt.legend(title="Sample Group", loc="best")
    plt.tight_layout()

    return plt
