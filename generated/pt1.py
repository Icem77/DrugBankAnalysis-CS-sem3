import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part1 import drug_info_df

if __name__  == "__main__":
    df = drug_info_df("drugbank_partial_and_generated.xml")
    print(df)

