import xml.etree.ElementTree as ET
import pandas as pd

def drug_info_df(xml_file_path : str) -> pd.DataFrame:
    """
    Given a xml file with DrugBank like structure creates a drug info data frame.
    Data Frame consists of:
    - drug id
    - name
    - type 
    - description
    - state
    - indications
    - mechanism of action
    - food interactions
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"ID": [], "Name": [], "Type": [], 
            "Description": [], "State": [], "Indication": [], 
            "Mechanism-of-action": [], "Food-interactions": []}

    for drug in root.findall("db:drug", namespace):
        # gether appropriete tags
        drug_id = drug.find("db:drugbank-id", namespace)
        drug_name = drug.find("db:name", namespace)
        drug_type = drug.attrib["type"]
        drug_description = drug.find("db:description", namespace)
        drug_state = drug.find("db:state", namespace)
        drug_indication = drug.find("db:indication", namespace)
        drug_mechanism_of_action = drug.find("db:mechanism-of-action", namespace)
        
        # update data frame based on gathered tags
        data["ID"].append(drug_id.text) if drug_id is not None else data["ID"].append(None)
        data["Name"].append(drug_name.text) if drug_name is not None else data["Name"].append(None)
        data["Type"].append(drug_type)
        data["Description"].append(drug_description.text) if drug_description is not None else data["Description"].append(None)
        data["State"].append(drug_state.text) if drug_state is not None else data["State"].append(None)
        data["Indication"].append(drug_indication.text) if drug_indication is not None else data["Indication"].append(None)
        data["Mechanism-of-action"].append(drug_mechanism_of_action.text) if drug_mechanism_of_action is not None else data["Mechanism-of-action"].append(None)
        
        # build string with food-interactions
        food_interactions = ""
        food_interaction_tag = drug.find("db:food-interactions", namespace)
        if food_interaction_tag is not None:
            for food_interaction in food_interaction_tag.findall("db:food-interaction", namespace):
                food_interactions += " " + food_interaction.text
        food_interactions = food_interactions.lstrip(" ")

        # add food interaction string to data frame
        data["Food-interactions"].append(food_interactions)


    return pd.DataFrame(data)

if __name__ == "__main__":
    df = drug_info_df("drugbank_partial.xml")
    print(df)