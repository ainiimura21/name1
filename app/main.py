import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dataloader import filter_data, load_data
from Correlation import load_data, filter_data, plot_correlation
from boxplot import plot_boxplot
from volcano import plot_volcano

# Get current file path
BASE_PATH = Path(__file__).parent

# Construct paths
METADATA_PATH = str(BASE_PATH.parent / "Core data/somalogic_metadata.csv")
PROTEINS_PATH = str(BASE_PATH.parent / "Core data/proteins_plot.csv")
VOLCANO_PATH = str(BASE_PATH.parent / "Core data/SSC_all_Healthy_allproteins.csv")

# Set page configuration
st.set_page_config(
    page_title="ScleroBase",  
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="collapsed"  
)

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
            padding: 10px 20px;
            font-size: 26px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100vw;  /* Full width of the viewport */
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999;  /* Ensure navbar stays above other elements */
        }
        .navbar a {
            color: white;
            padding: 30px 30px;
            text-decoration: none;
            font-weight: normal; 
            font-size: 18px; 
        }
        .navbar a:hover {
            background-color: #1B5E20;  /* Darker green background on hover */
            color: white;  /* Keep the text white */
        }
        .brand {
            font-family: 'MuseoModerno', cursive;  /* Updated to MuseoModerno */
            font-size: 42px;  /* Brand name size */
            font-weight: 400;
            color: white;
            padding-left: 60px;
        }
            
        /* Mobile-specific styles */
        @media screen and (max-width: 768px) {
            .navbar {
                flex-direction: column;
                padding: 5px 10px;
            }
            .navbar a {
                font-size: 14px;
                padding: 8px 15px;
                width: 100%;  /* Full width on small screens */
                text-align: center;
            }
            .brand {
                font-size: 24px;
                text-align: center;
                margin-bottom: 10px;
            }
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
  
    if "protein_options" not in st.session_state:
    # Load and cache data
        metadata, proteins, _ = get_data()
        st.session_state["protein_options_map"] = {
            "EntrezGeneID": proteins["EntrezGeneID"].dropna().unique().tolist(),
            "EntrezGeneSymbol": proteins["EntrezGeneSymbol"].dropna().unique().tolist(),
            "TargetFullName": proteins["TargetFullName"].dropna().unique().tolist(),
            "Target": proteins["Target"].dropna().unique().tolist(),
        }
    
    def generate_and_display_plots(button_name, id_type, protein_id, button_key):

        # Button for generating plots
        if st.button(button_name, key=button_key):
            st.session_state["active_button"] = button_key  # Track which button was clicked
            if not protein_id:
                st.error("Please enter a valid Protein ID.")
            else:
                try:
                    # Load data and cache in session state
                    metadata, proteins, volcano = get_data()
                    merged_data = filter_data(proteins, metadata, protein_id, id_type)
                    protein_name = merged_data["TargetFullName"].iloc[0]

                    # Store data in session state
                    st.session_state["plot_data"] = {
                        "merged_data": merged_data,
                        "protein_name": protein_name,
                        "volcano_plot_data": volcano
                    }

                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}.")
                    st.session_state["active_button"] = None

        # Only display plots if the current button is active
        if st.session_state.get("active_button") == button_key:
            try:
                data = st.session_state["plot_data"]
                protein_name = data["protein_name"]
                merged_data = data["merged_data"]
                volcano = data["volcano_plot_data"]

                # Add tabs and display plots
                corr_tab, box_tab, volc_tab = st.tabs(['Correlation Plot', 'Box Plot', 'Volcano Plot'])
                with corr_tab:
                    st.subheader(f"Correlation Plot for {protein_name}")
                    corr_plot = plot_correlation(merged_data, protein_name)
                    st.pyplot(corr_plot)

                with box_tab:
                    st.subheader(f"Box Plot for {protein_name}")
                    box_plot = plot_boxplot(merged_data, protein_name)
                    st.pyplot(box_plot)

                with volc_tab:
                    st.subheader(f"Volcano Plot")
                    st.markdown("Displaying a volcano plot for the provided dataset.")
                    volcano_plot = plot_volcano(volcano)
                    st.pyplot(volcano_plot)

            except Exception as e:
                st.error(f"An error occurred while displaying the plots: {str(e)}")



    #Dropdown box
    col1, col2 = st.columns([2, 2])  # Two equal-width columns (1:1)
    with col1:
        id_type = st.selectbox(
            "Select Protein Reference Type:",
            ["EntrezGeneID", "EntrezGeneSymbol", "TargetFullName", "Target"]
        )
        
        # Update the options based on the selected reference type
        protein_options = st.session_state["protein_options_map"][id_type]

        # Create an autocomplete selectbox for protein ID suggestions
        protein_id = st.selectbox(
            "Enter or select Protein ID:",
            options=[""] + protein_options,  # Add an empty default option for manual input
            index=0,
            help=f"Select or type a valid {id_type} from the dataset."
        )

        generate_and_display_plots("Generate Plots", id_type, protein_id, "generate_plots_button")



    # Initialize session state keys if they don't exist
    if "selected_proteins" not in st.session_state:
        st.session_state["selected_proteins"] = []

    if "show_comparison" not in st.session_state:
        st.session_state["show_comparison"] = False

    # Control variable to check if "Generate Plots" has been clicked
    if "generate_plots_clicked" not in st.session_state:
        st.session_state["generate_plots_clicked"] = False


    with col2:
        selected_protein = st.selectbox(
            "Selected Proteins for Comparison:",
            options=st.session_state.get("selected_proteins", []),
            index=0 if st.session_state.get("selected_proteins") else -1,  # Default to first item or empty
            help="Select a protein to view detailed information."
        )

        # "Compare Proteins" button
        if st.button("Add Protein"):
            if not protein_id:
                st.error("Please enter a valid Protein ID.")
            else:
                # Initialize session state for comparison
                if "show_comparison" not in st.session_state:
                    st.session_state["show_comparison"] = True
                if "selected_proteins" not in st.session_state:
                    st.session_state["selected_proteins"] = []
                
                # Add protein to the comparison list
                if protein_id not in st.session_state["selected_proteins"]:
                    st.session_state["selected_proteins"].append(protein_id)
                    st.success(f"Added {protein_id} to comparison list!")
                else:
                    st.warning(f"{protein_id} is already in the comparison list.")
        
        generate_and_display_plots("Generate Comparison", id_type, selected_protein, "compare_proteins_button")
 

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

    query_params = st.query_params
    page = query_params.get("page", "home") 

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
