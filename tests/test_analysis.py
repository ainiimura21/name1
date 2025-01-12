import pandas as pd
import pytest
from analysis import compute_correlation, differential_expression

def test_compute_correlation():
    """Test correlation computation."""
    data = pd.DataFrame({
        "clinical_score": [1, 2, 3, 4, 5],
        "protein_expression": [2, 4, 6, 8, 10]
    })
    corr = compute_correlation(data, "clinical_score", "protein_expression")
    assert corr > 0.99, "Correlation should be close to 1 for linear data"

def test_differential_expression():
    """Test differential expression analysis."""
    group1 = pd.DataFrame({
        "Protein1": [10, 15, 12],
        "Protein2": [5, 7, 6]
    })
    group2 = pd.DataFrame({
        "Protein1": [20, 25, 22],
        "Protein2": [10, 12, 11]
    })
    proteins = pd.concat([group1, group2], axis=1)
    results = differential_expression(group1, group2, proteins)

    assert isinstance(results, pd.DataFrame), "Results should be a DataFrame"
    assert "logFC" in results.columns, "Results should include logFC column"
    assert "p-value" in results.columns, "Results should include p-value column"
    assert results["logFC"].iloc[0] > 0, "logFC should reflect upregulation"
