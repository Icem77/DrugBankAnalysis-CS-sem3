import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part8 import percentage_presence_of_drugs_in_cell_parts_pie_chart

if __name__ == "__main__":
   percentage_presence_of_drugs_in_cell_parts_pie_chart("drugbank_partial_and_generated.xml")