import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dataloader import load_data, filter_data
from Correlation import plot_correlation
from boxplot import plot_boxplot
from volcano import plot_volcano

# Paths to the data files
METADATA_PATH = "./Core data/somalogic_metadata.csv"
PROTEINS_PATH = "./Core data/proteins_plot.csv"
VOLCANO_PATH = "./Core data/SSC_all_Healthy_allproteins.csv"

@st.cache_data
def get_data():
    """Load and cache metadata and protein data."""
    metadata, proteins = load_data(METADATA_PATH, PROTEINS_PATH)  # Load only the first two datasets
    volcano = pd.read_csv(VOLCANO_PATH)  # Load the volcano dataset separately
    return metadata, proteins, volcano

def main():
    """Main function to run the Streamlit app."""
    # Header Section
    st.markdown("""
    <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            margin-left: -40%;
            margin-right: -40%;
        }
        .subtitle {
            font-size: 30px;
            font-weight: normal;
            text-align: center;
            color: grey;
            margin-bottom: 10%;
        }
    </style>
    <div class="title">
        Monitoring Progression of Scleroderma
    </div>
    <div class="subtitle">
        Higgins Lab Imperial College
    </div>
    """, unsafe_allow_html=True)

    # Section Title
    st.markdown("""
        <h2 style='color: #CC5500;'>
            MRSS vs Intensity Analysis
        </h2>
    """, unsafe_allow_html=True)

    # Sidebar for user input
    id_type = st.selectbox(
        "Select Protein Reference Type:",
        ["TargetFullName", "Target", "EntrezGeneID", "EntrezGeneSymbol"]
    )
    protein_id = st.text_input("Enter Protein ID:")

    # Button to trigger plot generation
    if st.button("Generate Plots"):
        if not protein_id:
            st.error("Please enter a valid Protein ID.")
        else:
            try:
                # Load the data
                metadata, proteins, volcano = get_data()

                # Filter the data and get corresponding metadata
                merged_data = filter_data(proteins, metadata, protein_id, id_type)

                # Get the protein name for the title
                protein_name = merged_data["TargetFullName"].iloc[0]

                # Add tabs and generate plot on each one
                corr_tab, box_tab, volc_tab = st.tabs(['Correlation Plot', 'Box Plot', 'Volcano Plot'])
                with corr_tab:
                    # Generate and display the correlation plot
                    st.subheader(f"Correlation Plot for {protein_name}")
                    corr_plot = plot_correlation(merged_data, protein_name)
                    st.pyplot(corr_plot)
                with box_tab:
                    # Generate and display the boxplot
                    st.subheader(f"Box Plot for {protein_name}")
                    box_plot = plot_boxplot(merged_data, protein_name)
                    st.pyplot(box_plot)
                with volc_tab:
                    # Volcano Plot Section
                    st.subheader(f"Volcano Plot")
                    st.markdown("Displaying a volcano plot for the provided dataset.")
                    volcano_plot = plot_volcano(volcano)  # Pass full volcano data
                    st.pyplot(volcano_plot)
            except ValueError as e:
                st.error(f"Value Error: {str(e)}. Please check the input values or dataset.")
            except KeyError as e:
                st.error(f"Key Error: Missing column in the data - {e}. Please verify the dataset structure.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}.")

if __name__ == "__main__":
    main()
