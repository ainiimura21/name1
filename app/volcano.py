import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

def plot_volcano(data):
    # Ensure required columns exist
    required_columns = ["logFC", "P.Value", "Target"]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data is missing required columns: {required_columns}")

    # Calculate -log10(p-value)
    if (data['P.Value'] <= 0).any():
        raise ValueError("P.Value contains non-positive values, which cannot be logged.")
    data['-log10_pvalue'] = -np.log10(data['P.Value'])

        # Create a compact layout for sliders with padding
    padding1, col1, padding2, col2, padding3, col3, padding4 = st.columns([1, 4, 1, 4, 1, 4, 1])  # Adjust proportions as needed

    with col1:
        fold_change_threshold = st.slider(
            "Fold Change (Log₂)", min_value=0.1, max_value=2.0, value=0.6, step=0.1, key="fold_change"
        )
    with col2:
        point_opacity = st.slider(
            "Transparency", min_value=0.1, max_value=1.0, value=0.8, step=0.1, key="opacity"
        )
    with col3:
        point_size = st.slider(
            "Point Size", min_value=5, max_value=20, value=10, step=1, key="size"
        )


    # Categorise points based on updated thresholds
    data['Colour'] = 'grey'  # Default for non-significant points
    data.loc[(data['logFC'] > fold_change_threshold) & (data['P.Value'] < 0.05), 'Colour'] = 'red'
    data.loc[(data['logFC'] < -fold_change_threshold) & (data['P.Value'] < 0.05), 'Colour'] = 'green'
    data.loc[(data['logFC'] > fold_change_threshold) & (data['P.Value'] > 0.05), 'Colour'] = 'orange'
    data.loc[(data['logFC'] < -fold_change_threshold) & (data['P.Value'] > 0.05), 'Colour'] = 'orange'

    # Create an interactive plot using Plotly
    fig = px.scatter(
        data_frame=data,
        x='logFC',
        y='-log10_pvalue',
        color='Colour',
        color_discrete_map={'red': 'red', 'green': 'green', 'grey': 'grey', 'orange': 'orange'},
        hover_name='Target',  # Protein name will be shown when hovering
        labels={"logFC": "Log₂ Fold Change", "-log10_pvalue": "-Log₁₀ P", "Colour": "Significance"},
        title="SSc High vs Healthy Proteins",
        opacity=point_opacity,  # Use the slider value for opacity
    )

    # Adjust the marker size based on the slider
    fig.update_traces(marker=dict(size=point_size))

    # Add threshold lines (vertical and horizontal)
    fig.add_vline(x=-fold_change_threshold, line_dash="dash", line_color="black")
    fig.add_vline(x=fold_change_threshold, line_dash="dash", line_color="black")
    fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="black")

    # Add the number of samples annotation
    num_samples = len(data)
    fig.add_annotation(
        text=f"Number of samples: {num_samples}",
        xref="paper",
        yref="paper",
        x=0.95,  # Bottom-right corner
        y=0.05,  # Bottom-right corner
        showarrow=False,
        font=dict(size=12, color="black"),
        align="right"
    )

    # Update layout to improve appearance
    fig.update_layout(
        xaxis_title="Log₂ Fold Change",
        yaxis_title="-Log₁₀ P",
        title=dict(
            text="SSc High vs Healthy Proteins",
            font=dict(size=16, family='Arial', style='italic')
        ),
        title_x=0.05,  # Center the title
        title_y=0.9,
        plot_bgcolor="white",
        hovermode="closest",
        height=700,  # Make the graph taller
        margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins for symmetry
        xaxis=dict(range=[-max(abs(data['logFC'])) - 0.2, max(abs(data['logFC'])) + 0.2])  # Symmetrical X-axis range
    )

    # Display the interactive Plotly chart within your Streamlit app
    st.plotly_chart(fig)
