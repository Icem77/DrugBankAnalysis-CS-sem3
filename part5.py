import networkx as nx
import matplotlib.pyplot as plt
import random

import xml.etree.ElementTree as ET
import pandas as pd

from part2 import replace_spaces_with_newline 

def pathways_with_interacting_drugs(xml_file_path : str):
    """"
    Given an xml_file_path to DrugBank like xml file creates
    a dictionary with pathway names as keys and lists of interacting
    drugs as values.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {}

    for drug in root.findall("db:drug", namespace):
        pathways_tag = drug.find("db:pathways", namespace)

        if pathways_tag is not None:
            for pathway_tag in pathways_tag.findall("db:pathway", namespace):
                pathway_name = pathway_tag.find("db:name", namespace)
                drugs_in_pathway = pathway_tag.find("db:drugs", namespace)

                if drugs_in_pathway is not None:
                    for drug in drugs_in_pathway.findall("db:drug", namespace):
                        drug_id = drug.find("db:drugbank-id", namespace).text

                        if (pathway_name.text not in data.keys()):
                            data[pathway_name.text] = []
                        
                        if drug_id not in data[pathway_name.text]:
                            data[pathway_name.text].append(drug_id)

    return data

def pathways_with_interacting_drugs_df(xml_file_path : str):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Pathway-id": [], "Drug-id": []}

    for drug in root.findall("db:drug", namespace):
        main_drug_id = drug.find("db:drugbank-id", namespace).text
        pathways_tag = drug.find("db:pathways", namespace)
        if pathways_tag is not None:
            for pathway_tag in pathways_tag.findall("db:pathway", namespace):
                pathway_id = pathway_tag.find("db:smpdb-id", namespace)

                data["Pathway-id"].append(pathway_id.text)
                data["Drug-id"].append(main_drug_id)

                drugs_in_pathway = pathway_tag.find("db:drugs", namespace)
                if drugs_in_pathway is not None:
                    for drug in drugs_in_pathway.findall("db:drug", namespace):
                        drug_id = drug.find("db:drugbank-id", namespace).text
                        
                        data["Pathway-id"].append(pathway_id.text)
                        data["Drug-id"].append(drug_id)

    return pd.DataFrame(data).drop_duplicates()


def draw_bipartite_pathway_graph(pathway_drug_dict):
    """
    Draws a bipartite graph of pathways and drug interactions with minimal edge crossings.
    Ensures pathways are on one side and drugs on the other for clarity.
    """

    B = nx.Graph()

    # Prepare node sets
    pathways = list(replace_spaces_with_newline(pathway_drug_dict.keys()))
    drugs = set(drug.replace(" ", "\n") for drug_list in pathway_drug_dict.values() for drug in drug_list)

    B.add_nodes_from(pathways, bipartite=0)  # Pathways (left side)
    B.add_nodes_from(drugs, bipartite=1)  # Drugs (right side)

    # assign unique colors to drugs
    drug_colors = {drug: plt.cm.Paired(random.uniform(0.2, 0.8)) for drug in drugs}

    # collect edges and assign colors
    edges = []
    edge_colors = []
    for pathway, drug_list in pathway_drug_dict.items():
        for drug in drug_list:
            pathway_node = pathway.replace(" ", "\n")
            drug_node = drug.replace(" ", "\n")
            B.add_edge(pathway_node, drug_node)
            edges.append((pathway_node, drug_node))
            edge_colors.append(drug_colors[drug_node])

    pos = nx.bipartite_layout(B, pathways)  # ensures separation of two sets

    for node, (x, y) in pos.items():
        if node in pathways:
            pos[node] = (x - 0.3, y)  # shift pathways slightly left
        else:
            pos[node] = (x + 0.3, y)  # shift drugs slightly right

    plt.figure(figsize=(16, 9))
    plt.margins(0.2)  
    plt.axis("off")

    # draw nodes with black borders
    nx.draw_networkx_nodes(B, pos, nodelist=pathways, node_color="lightblue", edgecolors="black", node_size=2200)
    nx.draw_networkx_nodes(B, pos, nodelist=drugs, node_color=[drug_colors[d] for d in drugs], edgecolors="black", node_size=2200)

    # draw edges with colors matching drug nodes
    nx.draw_networkx_edges(B, pos, edgelist=edges, edge_color=edge_colors, width=2)

    # draw labels on white background with black edges
    labels = {node: node for node in B.nodes()}
    nx.draw_networkx_labels(B, pos, labels, font_size=7, font_weight="bold",
                            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

    # adjust x and y limits to prevent cutoff
    x_values, y_values = zip(*pos.values())
    plt.xlim(min(x_values) - 0.2, max(x_values) + 0.2)  # Extend horizontal space
    plt.ylim(min(y_values) - 0.1, max(y_values) + 0.1)  # Extend vertical space

    plt.title("Pathways (left) and Interacting Drugs (right)", fontsize=16, fontweight="bold")

    # additional description below the graph
    description = "An edge exists between a pathway and a drug if the drug interacts with that pathway."
    plt.figtext(0.5, 0.02, description, wrap=True, fontsize=12, ha="center")

    plt.savefig("statics/bipartite_pathways_and_drugs_graph.jpg", format="jpg", dpi=300, bbox_inches="tight", pad_inches=0.2)
    plt.show()

if __name__ == "__main__":
    df = pathways_with_interacting_drugs_df("drugbank_partial.xml")
    print(df)

    draw_bipartite_pathway_graph(pathways_with_interacting_drugs("drugbank_partial.xml"))