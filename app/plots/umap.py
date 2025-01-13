# To run this code from python, download dataset file from google drive (link is in single_cell_data_link.txt in Core data) and move downloaded file to Core data folder

import scanpy as sc
import pandas as pd
from matplotlib.pyplot import rc_context
from matplotlib.colors import LinearSegmentedColormap
from dataloader import load_singlecell_data,getEntrezGeneSymbol

from pathlib import Path

def plot_umap(input_data_key,input_data_value):
    EntrezGeneSymbol = getEntrezGeneSymbol(input_data_key,input_data_value)
    BASE_PATH = Path(__file__).parent
    single_cell_data_path = str(BASE_PATH.parent / "Core data")
    single_cell_data=load_singlecell_data(single_cell_data_path)

    color_vars=['leiden',EntrezGeneSymbol]

    # Define colour map as requested by the client (from grey to blue)
    cmap = LinearSegmentedColormap.from_list("grey_to_blue", ["#d3d3d3", "blue"])

    with rc_context({"figure.figsize": (6, 6)}):
        sc.pl.umap(single_cell_data, color=color_vars, # plot UMAP
        cmap=cmap,
        # /* Reference 1 - taken from https://scanpy.readthedocs.io/en/stable/tutorials/plotting/core.html */
        legend_loc="on data", # Place labels on the data
        frameon=True,
        legend_fontsize=4.5,
        legend_fontoutline=1,)
    # /* end of reference 1 */

    return sc.pl


# umap_plot('EntrezGeneSymbol','THBS1') # EXAMPLE OF USAGE WITH GENESYMBOL
# plot_umap('EntrezGeneID','7057')
