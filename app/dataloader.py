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


    return merged_data
