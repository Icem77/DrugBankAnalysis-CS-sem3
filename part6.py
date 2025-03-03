import xml.etree.ElementTree as ET
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import math
from matplotlib.backends.backend_pdf import PdfPages

def drugs_with_pathways_count(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a dictionary with drug id's as keys and interacted pathways count
    as values.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {}

    for drug in root.findall("db:drug", namespace):
        drug_name = drug.find("db:drugbank-id", namespace)
        pathways_tag = drug.find("db:pathways", namespace)

        data[drug_name.text] = 0 if pathways_tag is None else len(pathways_tag.findall("db:pathway", namespace))
    
    return data

def drug_with_pathways_count_bar_plot(data):
    """
    Given a dictionary provided by drugs_with_pathways_count() function,
    creates a bar plot of drug names (X-axis) and the number of interacted pathways (Y-axis).
    
    If there are more than 25 drugs, it creates separate plots and saves them all in a single PDF file.
    
    WARNING: Drugs that have 0 interacting pathways are not displayed.
    """

    filtered_data = data
    """
    filtered_data = {k: v for k, v in data.items() if v > 0}
    """

    # sort drugs alphabetically
    sorted_data = dict(sorted(filtered_data.items()))

    # extract keys and values
    medicines = list(sorted_data.keys())
    pathway_counts = list(sorted_data.values())

    # define chunk size (number of drugs per plot)
    chunk_size = 25  
    num_chunks = math.ceil(len(medicines) / chunk_size)

    # create a multi-page PDF file
    pdf_filename = "statics/drug_pathways_count_chart.pdf"
    with PdfPages(pdf_filename) as pdf:
        for i in range(num_chunks):
            # get the subset of drugs for this plot
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            sub_medicines = medicines[start_idx:end_idx]
            sub_counts = pathway_counts[start_idx:end_idx]

            sns.set_style("whitegrid")
            plt.figure(figsize=(12, 6))

            plt.bar(sub_medicines, sub_counts, color=sns.color_palette("pastel"))

            plt.xlabel("Drug Name", fontsize=14, fontweight="bold")
            plt.ylabel("Number of Interacted Pathways", fontsize=14, fontweight="bold")
            plt.title(f"Drugs with Pathway Interaction Count (Part {i+1})", fontsize=16, fontweight="bold", pad=20)

            # rotate x-axis labels for better readability
            plt.xticks(rotation=45, fontsize=10, ha="right")

            # adjust y-axis to show integer values
            plt.yticks(range(0, max(sub_counts) + 2), fontsize=12)

            # remove chart borders
            sns.despine()

            pdf.savefig(bbox_inches="tight", dpi=300)
            plt.close()

if __name__ == "__main__":
    data = drug_with_pathways_count_bar_plot(drugs_with_pathways_count("drugbank_partial.xml"))