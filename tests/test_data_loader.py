import pytest
import pandas as pd
from pandas.errors import ParserError
from app.dataloader import load_data, filter_data, getEntrezGeneSymbol, load_singlecell_data
from io import StringIO

"""Unit test for the dataloader.py file. Four functions are tested:
 filter_data()
 getEntrezGeneSymbol()
 load_singlecell_data()
 load_data()
 """
@pytest.fixture
def valid_metadata_df():
    return pd.DataFrame({
        "SubjectID": [1, 2, 3],
        "Condition": ["Healthy", "VEDOSS", "Healthy"],
        "Info": [1, 2, 3]
    })
@pytest.fixture
def valid_proteins_df():
    return pd.DataFrame({
        "SampleId": [1, 2, 3, 4],
        "TargetFullName": ["ProteinA", "ProteinB", "ProteinC", "ProteinD"],
        "EntrezGeneID": [101, 102, 103, 104],
        "EntrezGeneSymbol": ["GeneA", "GeneB", "GeneC", "GeneD"]
    })


def test_load_data():
    """
    Test the load_data function for valid and invalid data.
    """
    # Valid input
    valid_metadata_df = StringIO("""SubjectID,Condition,Info
1,Healthy,1
2,VEDOSS,2
3,Healthy,3
""")
    valid_proteins_df = StringIO("""SampleId,TargetFullName,EntrezGeneID,EntrezGeneSymbol
1,ProteinA,101,GeneA
2,ProteinB,102,GeneB
3,ProteinC,103,GeneC
4,ProteinD,104,GeneD
""")

    # Test valid input
    metadata, protein = load_data(valid_metadata_df, valid_proteins_df)
    assert isinstance(metadata, pd.DataFrame), "Metadata should be a DataFrame."
    assert isinstance(protein, pd.DataFrame), "Proteins should be a DataFrame."
    assert len(metadata) == 3, "Metadata should have 3 rows."
    assert len(protein) == 4, "Proteins should have 4 rows."

    # Test invalid file paths
    with pytest.raises(ValueError, match="Error loading files"):
        load_data("non_existent_metadata.csv", "non_existent_proteins.csv")

def test_filter_data(valid_proteins_df, valid_metadata_df):
    """
    Filter the proteins data for a specific protein ID based on the ID type
    and retrieve corresponding metadata information.
    """
    invalid_id = "invalid_id"
    invalid_protein = "invalid_protein"
    valid_id = "TargetFullName"
    valid_protein = "ProteinB"

    # Test invalid inputs
    with pytest.raises(ValueError, match=f"No data found for {valid_id} = {invalid_protein}"):
        filter_data(valid_proteins_df, valid_metadata_df, invalid_protein, valid_id)
    with pytest.raises(ValueError, match=f"Invalid ID type"):
        filter_data(valid_proteins_df, valid_metadata_df, valid_protein, invalid_id)

    # Test valid inputs
    merged_df = filter_data(valid_proteins_df, valid_metadata_df, valid_protein, valid_id)
    assert not merged_df.empty, "Result is not empty"
    assert len(merged_df) == 1, "Result should have exactly 1 row"
    assert len(merged_df.columns) == 7, "Result should have exactly 7 columns"