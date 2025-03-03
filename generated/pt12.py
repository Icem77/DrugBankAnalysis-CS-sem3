import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part12 import draw_price_and_manufacturers_count_corelation_scatter_plot

if __name__ == "__main__":
    draw_price_and_manufacturers_count_corelation_scatter_plot("drugbank_partial_and_generated.xml")