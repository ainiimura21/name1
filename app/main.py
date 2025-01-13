import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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
            display: flex;
            justify-content: space-between;
            padding: 0vh 2vw;
            align-items: center;
            width: 100vw;  /* Full width of the viewport */
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999;  /* Ensure navbar stays above other elements */
            height: 9vh;
        }

        .brand_container{
            display: flex;
            flex-direction: column;
            padding-left: 30px;
            height: 100%;
        } 

        .brand {
            font-family: 'MuseoModerno', cursive;  /* Updated to MuseoModerno */
            font-size: 35px;  /* Brand name size */
            font-weight: 400;
            color: white;
            padding: 4px 10px 23px 10px;
        }

        .p_brand {
            font-size: 15px;
            color: white;
            text-align: center;
            margin-top: -43px;
        }
            
        .navbar a {
            color: white;
            padding: 20px 30px 20px 30px;
            text-decoration: none;
            font-weight: normal; 
            font-size: 20px; 
            height: 100%;
            border-radius: 20px;
            /* Smooth transition for the colour */
            transition: color 0.3s ease;
        }

        .navbar a:hover {
            background-color: #1B5E20;  /* Darker green background on hover */
            color: orange;  /* Keep the text white */
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

    # Load data
    metadata, proteins, volcano = get_data()

    # Create two columns with custom width proportions
    col1, col2 = st.columns([3, 4])  # col1 will take up 2/5 of the space, col2 will take up 3/5

    with col1:
        st.markdown("""
        <style>
                    
            .init_info {
                font-size: 45px;  
            }
                    
            .init_p {
                font-size: 18px;
                padding-right: 3vw;
            }
                    
            .green-box {
                margin-top: 40px;
                background-color: #e0f7e9;  /* Light green background */
                border-radius: 20px;      /* Rounded corners */
                padding: 15px;           /* Inner padding */
                border: 1px solid #a5d6a7; /* Light green border */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Optional shadow */
                width: 80%;
            }
                    
            .contact {
                padding-top: 60px;
                padding-right: 40px;
                font-style: italic;
                font-size: 15px;
            }
                    
        </style>

        <div class="init_info"> 
            <h>Welcome to ScleroBase...</h>
            <div class="init_p">A Web-App for searching and comparing protein expression levels for individuals with scleraderma - and it's easy!</div>
        </div>
        <div class="green-box">
            <ul>
                <li style="font-size: 18px; padding: 10px;"><b style="font-size:20px">Explore All proteins</b>: Search our database or simply look to the right at our volcano plot.</li>
                <br>
                <li style="font-size: 18px; padding: 10px;"><b style="font-size:20px">Search for specific protein</b>: Enter a protein, and check out the graphs.</li>
                <br>
                <li style="font-size: 18px; padding: 10px;"><b style="font-size:20px">Compare protein expression levels</b>: Compare graphs side by side.</li>
            </ul>
        </div>
        <div class="contact">The Higgins Lab collects it's own data, and the graphs are derived thereof. If you feel like adding your very own data, please contact kb822@ic.ac.uk</div>
        """, unsafe_allow_html=True)

    # Right Column: Volcano Plot
    with col2:
        
        plot_volcano(volcano)  # Generate the plot


    st.markdown("""
        <h2 style='margin-top: -20px;'></h2>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h2 style='color: green;'>Protein Search</h2>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style='color: black; font-size: 18px; line-height: 1.5; font-style: italic'>
            Search for a protein using one of four reference types below, 
            and click on <b>Generate Plots</b> to see results. 
            If you are interested in the protein, select <b>Add Protein</b> 
            on the right-hand side. Then, at any time, you can 
            generate comparison plots of this protein by pressing <b>Plot Comparison</b> 
            when viewing other proteins.
        </p>
        """,
        unsafe_allow_html=True,
    )


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
                    filtered_data, metadata_info = filter_data(proteins, metadata, protein_id, id_type)
                    protein_name = filtered_data["TargetFullName"].iloc[0]

                    # Store data in session state
                    st.session_state["plot_data"] = {
                        "filtered_data": filtered_data,
                        "metadata_info": metadata_info,
                        "protein_name": protein_name,
                    }

                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}.")
                    st.session_state["active_button"] = None

        # Only display plots if the current button is active
        if st.session_state.get("active_button") == button_key:
            try:
                data = st.session_state["plot_data"]
                protein_name = data["protein_name"]
                filtered_data = data["filtered_data"]
                metadata_info = data["metadata_info"]
                
                # Add tabs and display plots
                corr_tab, box_tab= st.tabs(['Correlation Plot', 'Box Plot'])
                with corr_tab:
                    # st.subheader(f"Correlation Plot for {protein_name}")
                    corr_plot = plot_correlation(filtered_data, metadata_info, protein_name)
                    st.pyplot(corr_plot)

                with box_tab:
                    # st.subheader(f"Box Plot for {protein_name}")
                    box_plot = plot_boxplot(filtered_data, metadata_info, protein_name)
                    st.pyplot(box_plot)

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
        
        # Add padding above the graph
        st.markdown("<div style='padding-top: 27px;'></div>", unsafe_allow_html=True)
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

def research():
    """Research page with publications."""
    st.title("Research and Publications")
    st.markdown("""
    Specific papers...
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
            <div class="brand_container">
                <div class="brand">ScleroBase</div>
                <div class="p_brand">Higgins Lab Presents</div>
            </div>
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
