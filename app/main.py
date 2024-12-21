import streamlit as st
from Correlation import load_data, filter_data, plot_correlation
from boxplot import plot_boxplot

# Paths to the data files
METADATA_PATH = "Core data/somalogic_metadata.csv"
PROTEINS_PATH = "Core data/proteins_plot.csv"

@st.cache_data
def get_data():
    metadata, proteins = load_data(METADATA_PATH, PROTEINS_PATH)
    return metadata, proteins

def main():

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
                metadata, proteins = get_data()

                # Filter the data and get corresponding metadata
                filtered_data, metadata_info = filter_data(proteins, metadata, protein_id, id_type)

                # Get the protein name for the title
                protein_name = filtered_data["TargetFullName"].iloc[0]

                # Generate and display the correlation plot
                st.subheader(f"Correlation Plot for {protein_name}")
                corr_plot = plot_correlation(filtered_data, metadata_info, protein_name)
                st.pyplot(corr_plot)

                # Generate and display the boxplot
                st.subheader(f"Box Plot for {protein_name}")
                box_plot = plot_boxplot(filtered_data, metadata_info, protein_name)
                st.pyplot(box_plot)

            except ValueError as e:
                st.error(str(e))
            except KeyError as e:
                st.error(f"Column Error: {e}")

if __name__ == "__main__":
    main()
