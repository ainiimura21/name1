import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib.pyplot as plt
from app.boxplot import plot_boxplot


class TestPlotBoxplot(unittest.TestCase):
    def setUp(self):
        # Test filtered dataset
        self.filtered_data = pd.DataFrame({
            "SampleId": [1, 2, 3, 4],
            "condition": ["Healthy", "VEDOSS", "SSC_low", "SSC_high"],
            "Intensity": [10, 20, 15, 25]
        })
        # Test metadata dataset
        self.metadata_info = pd.DataFrame({
            "SubjectID": [1, 2, 3, 4],
            "OtherInfo": ["Info1", "Info2", "Info3", "Info4"]
        })

        self.protein_name = "Test Protein"

    @patch("matplotlib.pyplot.show")  # Mock plt.show to prevent rendering
    def test_plot_boxplot(self, mock_show):
        # Run the function
        result = plot_boxplot(self.filtered_data, self.metadata_info, self.protein_name)

        # Validate that plt.show() was called once
        mock_show.assert_called_once()

        self.assertIsInstance(result, MagicMock)

    @patch("matplotlib.pyplot.Figure.add_axes")  # Mock plt.Figure.add_axes
    def test_custom_palette_assignment(self, mock_add_axes):
        # Run the function
        plot_boxplot(self.filtered_data, self.metadata_info, self.protein_name)

        # Validate that add_axes was called
        mock_add_axes.assert_called_once_with([0, 0, 1, 1])

    def test_data_merge(self):
        # Check if merged data is correct
        merged_data = pd.merge(
            self.filtered_data,
            self.metadata_info,
            left_on="SampleId",
            right_on="SubjectID",
            how="inner"
        )
        self.assertEqual(len(merged_data), 4)  # Ensure all rows are merged
        self.assertIn("OtherInfo", merged_data.columns)  # Check for expected column


if __name__ == "__main__":
    unittest.main()
