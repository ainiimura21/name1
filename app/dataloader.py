from typing import Any, Tuple
import pandas as pd
from pandas import DataFrame


def load_data(metadata_path: str, proteins_path: str) -> Tuple[DataFrame, DataFrame]:
    """
    Load metadata and protein data from the provided file paths.

    Parameters:
    - metadata_path: Path to the metadata CSV file.
    - proteins_path: Path to the proteins CSV file.

    Returns:
    - Tuple containing metadata and protein data as pandas DataFrames.
    """
    try:
        metadata = pd.read_csv(metadata_path)
        proteins: DataFrame | Any = pd.read_csv(proteins_path)
    except Exception as e:
        raise ValueError(f"Error loading files: {e}")

    return metadata, proteins


def filter_data(
    proteins: DataFrame, metadata: DataFrame, protein_id: str, id_type: str
) -> DataFrame:
    """
    Filter and merge data for the selected protein ID and its SeqId with the highest mean intensity.

    Parameters:
    - proteins: Proteins data as a DataFrame.
    - metadata: Metadata as a DataFrame.
    - protein_id: The ID of the protein to filter for.
    - id_type: The type of protein ID (e.g., TargetFullName, Target).

    Returns:
    - Filtered and merged DataFrame ready for plotting.
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

    # Group by SeqId to calculate mean intensity and select SeqId with the highest mean
    seqid_groups = (
        filtered_data.groupby("SeqId")
        .agg(
            mean_intensity=("Intensity", "mean"),
            patient_count=("SampleId", "nunique"),
        )
        .reset_index()
    )

    # Drop SeqIds that don't cover all 13 patients
    seqid_groups = seqid_groups[seqid_groups["patient_count"] == 13]
    if seqid_groups.empty:
        seqid_groups = seqid_groups.sort_values(by=["patient_count", "mean_intensity"], ascending=[False, False])

    selected_seqid = seqid_groups.iloc[0]["SeqId"]

    # Filter original data for the selected SeqId
    final_data = filtered_data[filtered_data["SeqId"] == selected_seqid]

    # Merge with metadata on SampleId
    sample_ids = final_data["SampleId"].unique()
    metadata_info = metadata[metadata["SubjectID"].isin(sample_ids)]

    if metadata_info.empty:
        raise ValueError(f"No metadata found for Sample IDs: {sample_ids}.")

    merged_data = pd.merge(final_data, metadata_info, left_on="SampleId", right_on="SubjectID", how="inner")
    return merged_data
