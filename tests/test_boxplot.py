import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.plots.boxplot import plot_boxplot

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

@patch("matplotlib.pyplot.show")
@patch("matplotlib.pyplot.subplots")
def test_plot_boxplot(mock_subplots, mock_show, valid_data, protein_name):
    """Test that the plot_boxplot function initializes the plot and creates a boxplot."""
    # Mock figure and axes
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)

    # Call the function
    plot_boxplot(valid_data, protein_name)

    # Verify that plt.subplots is called with correct parameters
    mock_subplots.assert_called_once_with(figsize=(12, 8))

    # Verify that the boxplot method is called on the axes
    mock_ax.boxplot.assert_called_once()

    # Verify that plt.show() is called to display the plot
    mock_show.assert_called_once()

def test_invalid_data_raises_error(invalid_data, protein_name):
    """Test that plot_boxplot raises a ValueError for zero or negative intensity values."""
    with pytest.raises(ValueError, match="contains zero or negative values"):
        plot_boxplot(invalid_data, protein_name)
