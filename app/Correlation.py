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


def filter_data(proteins, metadata, protein_id, id_type):
    """
    Filter the proteins data for a specific protein ID based on the ID type
    and retrieve corresponding metadata information.
    """
    valid_columns = {
        "TargetFullName": "TargetFullName", #SSC all healthy all proteins
        "Target": "Target", #SSC all healthy all proteins
        "EntrezGeneID": "EntrezGeneID",
        "EntrezGeneSymbol": "EntrezGeneSymbol"
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

    # Debug: Ensure filtered data has SampleId
    if "SampleId" not in filtered_data.columns:
        raise KeyError("Column 'SampleId' not found in filtered proteins data.")
    print(f"Filtered Data for {protein_id}:")
    print(filtered_data.head())

    # Match SampleId in proteins with SubjectID in metadata
    sample_ids = filtered_data["SampleId"].unique()
    metadata_info = metadata[metadata["SubjectID"].isin(sample_ids)]

    if metadata_info.empty:
        raise ValueError(f"No metadata found for Sample IDs: {sample_ids}.")

    # Debug: Print metadata subset
    print("Metadata Info:")
    print(metadata_info.head())

    return filtered_data, metadata_info



def plot_correlation(filtered_data, metadata_info, protein_name):
    """
    Create a scatter plot of MRSS (linear scale) vs Intensity (logarithmic scale)
    with condition-specific colors for points and tags.
    """
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



