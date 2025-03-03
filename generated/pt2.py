import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part2 import draw_synonyms_graph, drug_synonyms_df

if __name__  == "__main__":
    df = drug_synonyms_df("drugbank_partial_and_generated.xml")
    print(df)

    draw_synonyms_graph("777", "drugbank_partial_and_generated.xml")
