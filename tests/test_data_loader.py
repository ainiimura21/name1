import pandas as pd
from app.data_loader import load_metadata, load_proteins, preprocess_data

def test_load_metadata():
    """Test loading metadata."""
    metadata = load_metadata()
    assert isinstance(metadata, pd.DataFrame), "Metadata should be a DataFrame"
    assert metadata.shape[0] > 0, "Metadata should have rows"

def test_load_proteins():
    """Test loading proteins."""
    proteins = load_proteins()
    assert isinstance(proteins, pd.DataFrame), "Proteins should be a DataFrame"
    assert proteins.shape[0] > 0, "Proteins should have rows"

def test_preprocess_data():
    """Test merging metadata and proteins."""
    metadata = load_metadata()
    proteins = load_proteins()
    merged = preprocess_data(metadata, proteins)
    assert isinstance(merged, pd.DataFrame), "Merged data should be a DataFrame"
    assert "Row.names" in merged.columns, "Merged DataFrame should include Row.names"
    assert "SubjectID" in merged.columns, "Merged DataFrame should include SubjectID"
