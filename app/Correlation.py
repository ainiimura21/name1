import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterSciNotation, NullFormatter


def load_data(metadata_path, proteins_path):
    """
    Load metadata and protein data from the provided file paths.
    """
    metadata = pd.read_csv(metadata_path)
    proteins = pd.read_csv(proteins_path)
    return metadata, proteins


def filter_data(proteins, metadata, protein_id, id_type):
    """
    Filter the proteins data for a specific protein ID based on the ID type
    and retrieve corresponding metadata information.
    """
    valid_columns = {
        "TargetFullName": "TargetFullName",
        "Target": "Target",
        "EntrezGeneID": "EntrezGeneID",
        "EntrezGeneSymbol": "EntrezGeneSymbol",
    }

    if id_type not in valid_columns:
        raise ValueError(f"Invalid ID type. Choose from {list(valid_columns.keys())}.")

    column_name = valid_columns[id_type]

    if column_name not in proteins.columns:
        raise KeyError(f"Column '{column_name}' not found in proteins data.")

    # Filter proteins data for the given protein ID
    filtered_data = proteins[proteins[column_name] == protein_id]
    if filtered_data.empty:
        raise ValueError(f"No data found for {id_type} = {protein_id}.")

    # Group by SeqID and calculate mean intensity for each
    seqid_groups = (
        filtered_data.groupby("SeqId")
        .agg(
            mean_intensity=("Intensity", "mean"),
            patient_count=("SampleId", "nunique"),
        )
        .reset_index()
    )

    # Drop SeqIDs that don't cover all 13 patients
    seqid_groups = seqid_groups[seqid_groups["patient_count"] == 13]

    # If no SeqIDs cover all 13 patients, proceed with the ones that cover the most
    if seqid_groups.empty:
        max_patients = filtered_data["SampleId"].nunique()
        seqid_groups = (
            filtered_data.groupby("SeqId")
            .agg(
                mean_intensity=("Intensity", "mean"),
                patient_count=("SampleId", "nunique"),
            )
            .reset_index()
        )
        seqid_groups = seqid_groups[seqid_groups["patient_count"] == max_patients]

    # Select the SeqID with the highest mean intensity
    selected_seqid = seqid_groups.sort_values(
        by=["mean_intensity", "SeqId"], ascending=[False, True]
    ).iloc[0]["SeqId"]

    # Filter the original data for the selected SeqID
    final_data = filtered_data[filtered_data["SeqId"] == selected_seqid]

    # Match SampleId in proteins with SubjectID in metadata
    sample_ids = final_data["SampleId"].unique()
    metadata_info = metadata[metadata["SubjectID"].isin(sample_ids)]

    if metadata_info.empty:
        raise ValueError(f"No metadata found for Sample IDs: {sample_ids}.")

    return final_data, metadata_info

def plot_correlation(filtered_data, metadata_info, protein_name):
    """
    Create a scatter plot of MRSS (linear scale) vs Intensity (logarithmic scale)
    with condition-specific colors for points and traditional logarithmic value markers.

    Parameters:
    - filtered_data (pd.DataFrame): DataFrame containing filtered protein intensity data.
    - metadata_info (pd.DataFrame): DataFrame containing corresponding metadata.
    - protein_name (str): Name of the protein for the plot title.

    Returns:
    - plt.Figure: The Matplotlib figure object containing the plot.
    """
    # Merge filtered_data with metadata_info on SampleId
    merged_data = pd.merge(
        filtered_data,
        metadata_info,
        left_on="SampleId",
        right_on="SubjectID",
        how="inner"
    )

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