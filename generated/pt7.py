import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part7 import targets_info_data_frame

if __name__ == "__main__":
    df = targets_info_data_frame("drugbank_partial_and_generated.xml")
    print(df)