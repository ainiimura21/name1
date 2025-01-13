import scanpy as sc
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc_context
from dataloader import load_singlecell_data,getEntrezGeneSymbol

def plot_violin(input_data_key,input_data_value):
    EntrezGeneSymbol = getEntrezGeneSymbol(input_data_key,input_data_value)
    BASE_PATH = Path(__file__).parent
    single_cell_data_path = str(BASE_PATH.parent / "Core data")
    single_cell_data=load_singlecell_data(single_cell_data_path)

    with rc_context({"figure.figsize": (5, 10)}):
        sc.pl.violin(single_cell_data, [EntrezGeneSymbol], groupby="leiden",rotation=90)
    # plt.subplots_adjust(top=0.02)
    plt.xticks(fontsize=5)
    plt.show()
    return plt

# violin_plot('EntrezGeneSymbol','THBS1') # EXAMPLE OF USAGE WITH GENESYMBOL