import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part10 import interacting_drug_pairs_df

if __name__ == "__main__":
    df = interacting_drug_pairs_df("drugbank_partial_and_generated.xml")
    print(df)