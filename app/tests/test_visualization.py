import pandas as pd
from plots import volcano_plot

def test_volcano_plot():
    """Test generating a volcano plot."""
    results_df = pd.DataFrame({
        "Protein": ["Protein1", "Protein2"],
        "logFC": [2.5, -1.2],
        "p-value": [0.001, 0.05]
    })
    fig = volcano_plot(results_df)
    assert fig, "Volcano plot should return a Plotly figure object"
    assert "Protein1" in fig.data[0].text, "Hover text should include Protein1"
    assert "Protein2" in fig.data[0].text, "Hover text should include Protein2"
