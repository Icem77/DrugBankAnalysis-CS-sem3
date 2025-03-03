import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

def drug_synonyms_df(xml_file_path):
    """
    Given an xml file path with DrugBank like structure creates pandas dataframe
    which rows consist of:
    - drug id
    - list of drug synonyms
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"ID": [], "Synonyms": []}

    # iterate through all drugss
    for drug in root.findall("db:drug", namespace):    
        data["ID"].append(drug.find("db:drugbank-id", namespace).text)

        drug_synonyms_tag = drug.find("db:synonyms", namespace)

        # construct the list of synonyms
        synonyms = []
        if drug_synonyms_tag is not None:
            for synonym in drug_synonyms_tag.findall("db:synonym", namespace):
                synonyms.append(synonym.text)

        data["Synonyms"].append(synonyms)

    return pd.DataFrame(data)

def replace_spaces_with_newline(strings_list):
    """
    Given a list of strings, returns a list which elements
    are strings from original list with spaces replaced with newlines.
    """
    return [s.replace(" ", "\n") for s in strings_list]

def finds_synonyms_for_id(db_id, xml_file_path):
    """
    Given drugbank-id of drug and a path to DrugBank like xml file
    returns a main name of a drug and a list of it's synonyms.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    for drug in root.findall("db:drug", namespace):
        drug_id = drug.find("db:drugbank-id", namespace)
        if drug_id is not None and drug_id.text == db_id:
            drug_name = drug.find("db:name", namespace).text
            drug_synonyms_tag = drug.find("db:synonyms", namespace)

            synonyms = []
            if drug_synonyms_tag is not None:
                for synonym in drug_synonyms_tag.findall("db:synonym", namespace):
                    synonyms.append(synonym.text)

            return drug_name, synonyms

    return None, None

def draw_synonyms_graph(db_id, xml_file_path):
    """
    Given a xml file with DrugBank like structure creates a png file with
    star graph drawing. The center node is the main name of a drug and the outer
    nodes are its synonyms.
    """
    center_node, peripheral_nodes = finds_synonyms_for_id(db_id, xml_file_path)
    if center_node is not None:
        center_node_name_for_title = center_node
        center_node = center_node.replace(" ", "\n")
        peripheral_nodes = replace_spaces_with_newline(peripheral_nodes)
        G = nx.star_graph(len(peripheral_nodes))
        
        mapping = {0: center_node}  # center node is always '0' in nx.star_graph()
        for i, node in enumerate(peripheral_nodes, start=1):
            mapping[i] = node  # map other nodes
        
        G = nx.relabel_nodes(G, mapping)

        # use shell layout with center node in the middle
        pos = nx.shell_layout(G, nlist=[[center_node], peripheral_nodes])

        plt.figure(figsize=(12, 12))
        nx.draw(
            G, pos, with_labels=True, node_color='lightgreen', node_size=8000, font_size=9, font_weight="bold", 
            edge_color="black", linewidths=2, edgecolors='black', font_color='black',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
        )

        plt.title(f"'{center_node_name_for_title}' and its synonyms", fontsize=24, fontweight="bold")

        plt.savefig(f"statics/{db_id}_synonyms_graph.png", format="png", dpi=300, bbox_inches='tight')

        print(f"Star graph saved as {db_id}_synonyms_graph.png")
    else:
        print("ID not found in the database.")

if __name__ == "__main__":
    df = drug_synonyms_df("drugbank_partial.xml")
    print(df)

    draw_synonyms_graph("DB00036", "drugbank_partial.xml")
