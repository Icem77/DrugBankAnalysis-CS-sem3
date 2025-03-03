import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part11 import draw_gene_drug_product_star_graph

if __name__ == "__main__":
    draw_gene_drug_product_star_graph("drugbank_partial_and_generated.xml", "CACNA1B")