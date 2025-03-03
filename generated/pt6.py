import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part6 import drug_with_pathways_count_bar_plot, drugs_with_pathways_count

if __name__ == "__main__":
    drug_with_pathways_count_bar_plot(drugs_with_pathways_count("drugbank_partial_and_generated.xml"))