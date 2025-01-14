import pytest
import pandas as pd
from unittest.mock import patch, mock
from plots.boxplot import plot_boxplot
import matplotlib.pyplot as plt

# Fixture for valid test data
@pytest.fixture
def valid_data():
    """Fixture to provide valid intensity values for all conditions."""
    return pd.DataFrame({
        "SampleId": [1, 2, 3, 4],
        "condition": ["Healthy", "VEDOSS", "SSC_low", "SSC_high"],
        "Intensity": [10, 20, 15, 25]
    })

# Fixture for invalid test data
@pytest.fixture
def invalid_data():
    """Fixture to provide invalid intensity values (zero or negative)."""
    return pd.DataFrame({
        "SampleId": [1, 2, 3, 4],
        "condition": ["Healthy", "VEDOSS", "SSC_low", "SSC_high"],
        "Intensity": [-10, 0, 15, 25]
    })

@pytest.fixture
def protein_name():
    """Fixture for test protein name."""
    return "Test Protein"

@mock.patch("matplotlib.pyplot.subplots")
def test_plot_boxplot(mock_subplots, valid_data, invalid_data, protein_name):
    """Test that the plot_boxplot function initializes the plot and creates a boxplot."""

    # Call the function with valid data
    plot_boxplot(valid_data, protein_name)
    mock_subplots.assert_called_once()

    # Test that the function raises ValueError for invalid data
    with pytest.raises(ValueError, match="contains zero or negative values"):
        plot_boxplot(invalid_data, protein_name)


def test_plot_contents(valid_data, protein_name):
    """Test the contents of the plot using valid data."""

    plot_boxplot(valid_data, protein_name)

    ax = plt.gca() 
    assert ax.get_title() == f"Box Plot for {protein_name}"
    assert ax.get_ylabel() == "Intensity (Logarithmic Scale)"
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Healthy", "VEDOSS", "SSC_low", "SSC_high"]

    plt.close()
