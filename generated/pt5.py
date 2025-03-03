import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part5 import pathways_with_interacting_drugs_df

if __name__ == "__main__":
    df = pathways_with_interacting_drugs_df("drugbank_partial_and_generated.xml")
    print(df)
    