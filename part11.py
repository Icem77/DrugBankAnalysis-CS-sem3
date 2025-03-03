import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

def gene_interacting_drugs_with_distinct_products(xml_file_path : str, gene_name : str):
    """
    Given an xml_file_path to DrugBank like xml file creates and a gene name
    creates a dictionary with drug names that interact with gene as keys
    and lists of products which consist those drugs as values.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    products_of_drugs_interacting_with_gene = {}

    for drug in root.findall("db:drug", namespace):
        proteins = []

        for target in drug.find("db:targets", namespace).findall("db:target", namespace): 
            proteins.append(target) 
        for transporter in drug.find("db:transporters", namespace).findall("db:transporter", namespace):
            proteins.append(transporter) 
        for carrier in drug.find("db:carriers", namespace).findall("db:carriers", namespace):
            proteins.append(carrier)
        for enzyme in drug.find("db:enzymes", namespace).findall("db:enzyme", namespace):
            proteins.append(enzyme)

        for protein_tag in proteins:           
            for polypeptide in protein_tag.findall("db:polypeptide", namespace):
                if polypeptide.find("db:gene-name", namespace).text == gene_name:
                    drug_name = drug.find("db:name", namespace)
                    products_of_drugs_interacting_with_gene[drug_name.text] = []
                    products_tag = drug.find("db:products", namespace)
                    if products_tag is not None:
                        for product_tag in products_tag.findall("db:product", namespace):
                            products_of_drugs_interacting_with_gene[drug_name.text].append(
                                product_tag.find("db:name", namespace).text)
                    
                    products_of_drugs_interacting_with_gene[drug_name.text] = list(dict.fromkeys(products_of_drugs_interacting_with_gene[drug_name.text]))

    return products_of_drugs_interacting_with_gene

def draw_gene_drug_product_star_graph(xml_file_path : str, gene_name : str):
    """
    Given an xml_file_path to DrugBank like xml file and gene name creates
    a png file with a drawing of nested star graphs.
    Center node is gene name, the next layer of nodes are drugs interacting with it
    and the last one are products which consist those drugs.
    """

    drugs_and_products = gene_interacting_drugs_with_distinct_products(xml_file_path, gene_name)
    
    G = nx.Graph()

    for drug in drugs_and_products.keys():
        G.add_edge(gene_name, drug)
        
        for product in drugs_and_products[drug]:
            G.add_edge(drug, product)
    
    sub_outer_nodes = [val for key in drugs_and_products.keys() for val in drugs_and_products[key]]
    outer_nodes = list(drugs_and_products.keys()) + sub_outer_nodes
    central_nodes = [gene_name] + outer_nodes

    pos = nx.spring_layout(G)  # layout for better separation

    # colors for each layer
    central_color = "skyblue"
    outer_color = "orange"
    sub_outer_color = "lightgreen"

    plt.figure(figsize=(16, 9))
    
    # draw nodes with different colors
    nx.draw_networkx_nodes(G, pos, nodelist=central_nodes, node_size=700, node_color=central_color)
    nx.draw_networkx_nodes(G, pos, nodelist=outer_nodes, node_size=500, node_color=outer_color)
    nx.draw_networkx_nodes(G, pos, nodelist=sub_outer_nodes, node_size=300, node_color=sub_outer_color)
    
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color="gray")
    
    nx.draw_networkx_labels(G, pos, font_size=6, font_color="black", font_weight="bold")
    
    plt.title("Gene (blue) with interacting drugs (orange)\n and products which contains them (green)", 
              fontweight="bold", pad=0, fontsize=15)
    plt.axis("off")
    plt.savefig("statics/gene_drug_product.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    draw_gene_drug_product_star_graph("drugbank_partial.xml", "C1QC")


