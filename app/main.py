#Interferon regulatory factor 6
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Correlation import load_data, filter_data, plot_correlation
from boxplot import plot_boxplot
from volcano import plot_volcano

# Paths to the data files
METADATA_PATH = "./Core data/somalogic_metadata.csv"
PROTEINS_PATH = "./Core data/proteins_plot.csv"
VOLCANO_PATH = "./Core data/SSC_all_Healthy_allproteins.csv"

# Set page configuration
st.set_page_config(layout="wide")  # Wide layout to avoid the sidebar

# Add custom fonts from Google Fonts
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=MuseoModerno:wght@400&family=Actor&display=swap" rel="stylesheet">
    <style>
        /* Hide the Streamlit default elements */
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;}
        header {visibility: hidden;} 
        .css-1e5imcs, .css-17eq0hr {display: none !important;}

        .navbar {
            background-color: #2E7D32;  /* Green background */
            display: flex;
            justify-content: space-between;
            padding: 0vh 2vw;
            align-items: center;
            width: 100vw;  /* Full width of the viewport */
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999;  /* Ensure navbar stays above other elements */
            height: 12vh;
        }
        .navbar a {
            color: white;
            padding: 30px 30px;
            text-decoration: none;
            font-weight: normal; 
            font-size: 22px; 
            height: 100%;
            border-radius: 20px;
            /* Smooth transition for the colour */
            transition: color 0.3s ease;
        }
        .navbar a:hover {
            background-color: #1B5E20;  /* Darker green background on hover */
            color: orange;  /* Keep the text white */
        }
        .brand {
            font-family: 'MuseoModerno', cursive;  /* Updated to MuseoModerno */
            font-size: 50px;  /* Brand name size */
            font-weight: 400;
            color: white;
            padding-left: 60px;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    """Load and cache metadata and protein data."""
    metadata, proteins = load_data(METADATA_PATH, PROTEINS_PATH)
    volcano = pd.read_csv(VOLCANO_PATH)  # Load the volcano dataset separately
    return metadata, proteins, volcano

def home():
    """Home page with plots and analysis."""
    st.markdown("""
        <h2 style='color: #CC5500;'>MRSS vs Intensity Analysis</h2>
    """, unsafe_allow_html=True)

    # Sidebar for user input
    id_type = st.selectbox(
        "Select Protein Reference Type:",
        ["TargetFullName", "Target", "EntrezGeneID", "EntrezGeneSymbol"]
    )
    protein_id = st.text_input("Enter Protein ID:")

    if st.button("Generate Plots"):
        if not protein_id:
            st.error("Please enter a valid Protein ID.")
        else:
            try:
                metadata, proteins, volcano = get_data()
                filtered_data, metadata_info = filter_data(proteins, metadata, protein_id, id_type)
                protein_name = filtered_data["TargetFullName"].iloc[0]

                # Add tabs and generate plot on each one
                corr_tab, box_tab, volc_tab = st.tabs(['Correlation Plot', 'Box Plot', 'Volcano Plot'])
                with corr_tab:
                    # Generate and display the correlation plot
                    st.subheader(f"Correlation Plot for {protein_name}")
                    corr_plot = plot_correlation(filtered_data, metadata_info, protein_name)
                    st.pyplot(corr_plot)
                with box_tab:
                    # Generate and display the boxplot
                    st.subheader(f"Box Plot for {protein_name}")
                    box_plot = plot_boxplot(filtered_data, metadata_info, protein_name)
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

def research():
    """Research page with publications."""
    st.title("Research and Publications")
    st.markdown("""
    - **2024**: Stimulation of skeletal stem cells in the growth plate promotes linear bone growth.
    - **2023**: Plasticity of epithelial cells during wound healing.
    - **2022**: ARF suppression in pediatric brain tumors.
    """)

def about():
    st.title("About Us")
    st.write("Learn more about the Higgins Lab and our work.")

def data():
    st.title("Data")
    st.write("Access our latest datasets and reports.")

def contact():
    st.title("Contact Us")
    st.write("Feel free to contact us for more information!")

def main():
    """Main function to run the Streamlit app."""
    # Navbar Section
    st.markdown("""
        <div class="navbar">
            <div class="brand">ScleroBase</div>
            <div>
                <a href="?page=home">Home</a>
                <a href="?page=about">About Us</a>
                <a href="?page=research">Research</a>  <!-- Link to Research -->
                <a href="?page=data">Data</a>
                <a href="?page=contact">Contact Us</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Get the selected page from URL query params
    query_params = st.query_params
    page = query_params.get("page", "home")  # Default to "home" if no page is specified

    # Render the selected page
    if page == "home":
        home()
    elif page == "research":
        research()
    elif page == "about":
        about()
    elif page == "data":
        data()
    elif page == "contact":
        contact()

if __name__ == "__main__":
    main()
