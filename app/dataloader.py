
import pandas as pd
import scanpy as sc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

def getEntrezGeneSymbol(input_data_key,input_data_value):
    BASE_PATH = Path(__file__).parent
    file_path = str(BASE_PATH.parent / "Core data/SSC_all_Healthy_allproteins.csv")
    mapping= pd.read_csv(file_path)
    return mapping[mapping[input_data_key]==input_data_value]['EntrezGeneSymbol'].iloc[0]

def load_singlecell_data(single_cell_data_path):
    
    return sc.read(f'{single_cell_data_path}/final_combined_simplified.h5ad')


def load_data(metadata_path, proteins_path):
    """
    Load metadata and protein data from the provided file paths.
    """
    try:
        metadata = pd.read_csv(metadata_path)
        proteins = pd.read_csv(proteins_path)
    except Exception as e:
        raise ValueError(f"Error loading files: {e}")
    return metadata, proteins
