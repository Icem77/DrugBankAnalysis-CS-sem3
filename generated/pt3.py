import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part3 import drug_and_products_df

if __name__ == "__main__":
    df = drug_and_products_df("drugbank_partial_and_generated.xml")
    print(df)