import pytest
import pandas as pd
from pandas.errors import ParserError
from unittest.mock import patch, mock_open
from app.dataloader import load_data

# Fixture for valid test data
@pytest.fixture
def valid_metadata_file():
    """Fixture to provide valid metadata CSV content."""
    return """SubjectID,OtherInfo
1,Info1
2,Info2
3,Info3
"""

@pytest.fixture
def valid_proteins_file():
    """Fixture to provide valid proteins CSV content."""
    return (
        "SampleId,TargetFullName,Target,EntrezGeneID,EntrezGeneSymbol"
        "1,Protein A,A,101,GA"
        "2,Protein B,B,102,GB"
        "3,Protein C,C,103,GC"
    )

@pytest.fixture
def invalid_file_content():
    """Fixture for invalid file content (non-CSV)."""
    return "Invalid Content"

def test_load_data_valid_files(valid_metadata_file, valid_proteins_file):
    """Test that load_data loads valid CSV files correctly."""
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.side_effect = [
            pd.DataFrame({"SubjectID": [1, 2, 3], "OtherInfo": ["Info1", "Info2", "Info3"]}),
            pd.DataFrame({
                "SampleId": [1, 2, 3],
                "TargetFullName": ["Protein A", "Protein B", "Protein C"],
                "Target": ["A", "B", "C"],
                "EntrezGeneID": [101, 102, 103],
                "EntrezGeneSymbol": ["GA", "GB", "GC"]
            }),
        ]

        metadata, proteins = load_data("metadata.csv", "proteins.csv")

        assert not metadata.empty
        assert not proteins.empty
        assert list(metadata.columns) == ["SubjectID", "OtherInfo"]
        assert list(proteins.columns) == ["SampleId", "TargetFullName", "Target", "EntrezGeneID", "EntrezGeneSymbol"]

def test_load_data_invalid_file_path():
    """Test that load_data raises ValueError for invalid file paths."""
    with pytest.raises(ValueError, match="Error loading files"):
        load_data("invalid_metadata.csv", "invalid_proteins.csv")

def test_load_data_invalid_file_content():
    """Test that load_data raises ValueError for invalid file content."""
    with patch("pandas.read_csv", side_effect=ParserError("Error parsing file")):
        with pytest.raises(ValueError, match="Error loading files"):
            load_data("metadata.csv", "proteins.csv")

def test_load_data_empty_files():
    """Test that load_data handles empty files correctly."""
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.side_effect = [pd.DataFrame(), pd.DataFrame()]

        metadata, proteins = load_data("metadata.csv", "proteins.csv")

        assert metadata.empty
        assert proteins.empty
