import xml.etree.ElementTree as ET
import pandas as pd

def interacting_drug_pairs_df(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a data frames which rows consist of:
    - drug id 
    - drug id of interacting drug
    - description of interaction
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Drug-id" : [], "Interacting-drug-id" : [], 
            "Interaction-description" : []}

    for drug in root.findall("db:drug", namespace):
        drug_id = drug.find("db:drugbank-id", namespace)
        interactions_tag = drug.find("db:drug-interactions", namespace)

        if interactions_tag is not None:
            for interaction in interactions_tag.findall("db:drug-interaction", namespace):
                interacting_drug_id = interaction.find("db:drugbank-id", namespace)
                description = interaction.find("db:description", namespace)

                data["Drug-id"].append(drug_id.text)
                data["Interacting-drug-id"].append(interacting_drug_id.text)
                if description is None: 
                    description = ""
                data["Interaction-description"].append(description.text)

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = interacting_drug_pairs_df("drugbank_partial.xml")
    print(df)
