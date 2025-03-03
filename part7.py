import xml.etree.ElementTree as ET
import pandas as pd

def targets_info_data_frame(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a targets info data frame which rows consists of:
    - target drug-bank id 
    - source (data base)
    - source id (id in source data base)
    - polypeptide name
    - gene name
    - GenAtlas id
    - number of chromosome
    - cellular location
    """
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Drug-id" : [], "Drugbank-id": [], "Source": [], "Source-id": [], 
        "Polypeptide-name": [], "Gene-name": [], "GenAtlasID": [], 
        "Num-of-chromosome": [], "Cellular-location": []}

    for drug in root.findall("db:drug", namespace):
        main_drug_id = drug.find("db:drugbank-id", namespace).text
        targets_tag = drug.find("db:targets", namespace)
        if targets_tag is not None:
            for target in targets_tag.findall("db:target", namespace):
                drug_bank_id = target.find("db:id", namespace).text
                polypeptides = target.findall("db:polypeptide", namespace)
                for polypeptide in polypeptides:
                    source = polypeptide.get("source")
                    polypeptide_name = polypeptide.find("db:name", namespace).text
                    gene_name = polypeptide.find("db:gene-name", namespace).text
                    cellular_location = polypeptide.find("db:cellular-location", namespace).text
                    num_of_chromosome = polypeptide.find("db:chromosome-location", namespace).text
                    gen_atlas_id = None
                    source_id = polypeptide.get("id")    
                    external_tag = polypeptide.find("db:external-identifiers", namespace)
                    for external_id in external_tag.findall("db:external-identifier", namespace):
                        resource = external_id.find("db:resource", namespace).text
                        resource_id = external_id.find("db:identifier", namespace).text

                        if (resource == "GenAtlas"):
                            gen_atlas_id = resource_id
                        if (resource == source):
                            source_id = resource_id
                    
                    data["Drug-id"].append(main_drug_id)
                    data["Drugbank-id"].append(drug_bank_id)
                    data["Source"].append(source)
                    data["Source-id"].append(source_id)
                    data["Polypeptide-name"].append(polypeptide_name)
                    data["Gene-name"].append(gene_name)
                    data["GenAtlasID"].append(gen_atlas_id)
                    data["Num-of-chromosome"].append(num_of_chromosome)
                    data["Cellular-location"].append(cellular_location)

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = targets_info_data_frame("drugbank_partial.xml")
    print(df)