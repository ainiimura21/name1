import streamlit as st
from Correlation import load_data, filter_data, plot_correlation

# Paths to the data files
METADATA_PATH = "Core Data/somalogic_metadata.csv"
PROTEINS_PATH = "Core Data/proteins_plot.csv"

@st.cache_data
def get_data():
    metadata, proteins = load_data(METADATA_PATH, PROTEINS_PATH)
    return metadata, proteins


def main():
    st.title("MRSS vs Intensity Correlation")

    # Load the data
    metadata, proteins = get_data()

    # Sidebar for user input
    st.sidebar.header("Protein Selection")
    id_type = st.sidebar.selectbox(
        "Select Protein Reference Type:",
        ["TargetFullName", "Target", "EntrezGeneID", "EntrezGeneSymbol"]
    )
    protein_id = st.sidebar.text_input("Enter Protein ID:")

    # Button to trigger plot generation
    if st.sidebar.button("Plot Correlation"):
        if not protein_id:
            st.error("Please enter a valid Protein ID.")
        else:
            try:
                # Filter the data and get corresponding metadata
                filtered_data, metadata_info = filter_data(proteins, metadata, protein_id, id_type)

                # Get the protein name for the title
                protein_name = filtered_data["TargetFullName"].iloc[0]

                # Generate and display the plot
                plt = plot_correlation(filtered_data, metadata_info, protein_name)
                st.pyplot(plt)
            except ValueError as e:
                st.error(str(e))
            except KeyError as e:
                st.error(f"Column Error: {e}")


if __name__ == "__main__":
    main()
