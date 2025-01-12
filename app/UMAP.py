import scanpy as sc
from matplotlib.pyplot import rc_context
from matplotlib.colors import LinearSegmentedColormap

def umap_plot(EntrezGeneSymbol='ETHE1'):
    # Paths to the data files
    # single_cell_data_path = "./Core data"

    single_cell_data_path = "/Users/linamraoui/Group_Software_Eng/name1/Core data"

    # Import and read single cell data set
    # single_cell_data = sc.read_h5ad(f'/Users/linamraoui/Group_Software_Eng/name1/Core data/final_combined_simplified.h5ad')

    # List all the split .h5ad files
    chunk_files = ['chunk_1.h5ad', 'chunk_2.h5ad', 'chunk_3.h5ad','chunk_4.h5ad','chunk_5.h5ad','chunk_6.h5ad']  # List all the chunk files

    # Initialize a list to store the AnnData objects
    adata_list = []
    # Load each chunk and append it to the list
    for chunk in chunk_files:
        print("reading chunk i")
        adata_chunk = sc.read(f'{single_cell_data_path}/{chunk}')
        adata_list.append(adata_chunk)

    # Concatenate all the chunks back into a single AnnData object
    single_cell_data = adata_list[0].concatenate(adata_list[1:], join='outer')


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

    return 'done'


umap_plot('ETHE1')


