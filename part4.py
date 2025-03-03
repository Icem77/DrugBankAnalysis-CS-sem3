import xml.etree.ElementTree as ET
import pandas as pd

def pathways_df(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a pathways info data frame which rows consists of:
    - pathway id
    - name
    - category
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Pathway-id": [], "Pathway-name": [], "Pathways-category": [],}

    for drug in root.findall("db:drug", namespace):
        pathways_tag = drug.find("db:pathways", namespace)
        if pathways_tag is not None:
            for pathway_tag in pathways_tag.findall("db:pathway", namespace):
                pathway_id = pathway_tag.find("db:smpdb-id", namespace)
                # add pathway to data frame if it's not already there
                if (pathway_id.text not in data["Pathway-id"]):
                    pathway_name = pathway_tag.find("db:name", namespace)
                    pathway_category = pathway_tag.find("db:category", namespace)
                    
                    data["Pathway-id"].append(pathway_id.text)
                    data["Pathway-name"].append(pathway_name.text)
                    data["Pathways-category"].append(pathway_category.text)

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = pathways_df("drugbank_partial.xml")
    print(df)

    print(f"Total number of pathways: {df.shape[0]}")
                