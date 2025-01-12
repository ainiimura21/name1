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
            "OtherColumn": ["A", "B", "C", "D"]
        })

        self.protein_name = "Test Protein"

    @patch("matplotlib.pyplot.show")
    def test_plot_boxplot(self, mock_show):
        # Run the function
        result = plot_boxplot(self.filtered_data, self.metadata_info, self.protein_name)

        # Validate that plt.show() was called once
        mock_show.assert_called_once()

        # Validate that the function returns matplotlib.pyplot
        self.assertIs(result, plt)

    @patch("matplotlib.pyplot.subplots")  # Mock plt.subplots
    def test_custom_palette_assignment(self, mock_subplots):
        # Mock the return value of plt.subplots
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Run the function
        plot_boxplot(self.filtered_data, self.metadata_info, self.protein_name)

        # Validate that plt.subplots was called
        mock_subplots.assert_called_once_with(figsize=(10, 7))

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
