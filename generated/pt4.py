import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part4 import pathways_df

if __name__ == "__main__":
    df = pathways_df("drugbank_partial_and_generated.xml")
    print(df)

    print(f"Total number of pathways: {df.shape[0]}")