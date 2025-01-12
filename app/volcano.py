import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text

def plot_volcano(data):
    # Ensure required columns exist
    required_columns = ["logFC", "P.Value", "Target"]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data is missing required columns: {required_columns}")

    # Calculate -log10(p-value)
    if (data['P.Value'] <= 0).any():
        raise ValueError("P.Value contains non-positive values, which cannot be logged.")
    data['-log10_pvalue'] = -np.log10(data['P.Value'])

    # Define thresholds
    fold_change_threshold = 0.6  # Adjust as needed
    pvalue_threshold = 0.05  # Adjust as needed

    # Categorise points
    data['Colour'] = 'grey'  # Default for non-significant points
    data.loc[(data['logFC'] > fold_change_threshold) & (data['P.Value'] < pvalue_threshold), 'Colour'] = 'red'
    data.loc[(data['logFC'] < -fold_change_threshold) & (data['P.Value'] < pvalue_threshold), 'Colour'] = 'green'
    data.loc[(data['logFC'] > fold_change_threshold) & (data['P.Value'] > pvalue_threshold), 'Colour'] = 'orange'
    data.loc[(data['logFC'] < -fold_change_threshold) & (data['P.Value'] > pvalue_threshold), 'Colour'] = 'orange'

    # Create the plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=data,
        x='logFC',
        y='-log10_pvalue',
        hue='Colour',
        palette={'red': 'red', 'green': 'green', 'grey': 'grey', 'orange': 'orange'},  # Added orange here
        legend=False,
        s=50  # Adjust point size
    )


    # Add threshold lines
    plt.axvline(x=-fold_change_threshold, linestyle='--', color='black', linewidth=0.8)
    plt.axvline(x=fold_change_threshold, linestyle='--', color='black', linewidth=0.8)
    plt.axhline(y=-np.log10(pvalue_threshold), linestyle='--', color='black', linewidth=0.8)

    # Label the plot
    plt.title("SSc High vs Healthy Proteins", fontsize=16, style='italic')
    plt.xlabel("Log₂ Fold Change", fontsize=14)
    plt.ylabel("-Log₁₀ P", fontsize=14)

    # Annotate significant points
    significant_points = data[data['Colour'].isin(['red', 'green'])]
    texts = []
    for _, row in significant_points.iterrows():
        texts.append(
            plt.text(
                row['logFC'],
                row['-log10_pvalue'],
                row['Target'],
                fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.7),
                ha='center'
            )
        )

    # Adjust labels to avoid overlap
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black', lw=0.5))

    # Final adjustments
    plt.tight_layout()
    return plt
