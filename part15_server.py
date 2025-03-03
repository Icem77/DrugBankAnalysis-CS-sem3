from fastapi import FastAPI
import xml.etree.ElementTree as ET
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class DrugRequest(BaseModel):
    drug_id: str

# Parsowanie XML i utworzenie ramki danych **tylko raz**
def load_data(xml_file_path):
    """
    Gathers info about the number of pathways that all the drugs
    interact with to effectively answer requests to server.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Drug-id" : [], "Pathways-count" : []}

    for drug in root.findall("db:drug", namespace):
        drug_id = drug.find("db:drugbank-id", namespace).text
        pathways_tag = drug.find("db:pathways", namespace)


        data["Drug-id"].append(drug_id)
        if pathways_tag is None:
            data["Pathways-count"].append(0)
        else:
            data["Pathways-count"].append(len(pathways_tag.findall("db:pathway", namespace)))

    return pd.DataFrame(data)

df_drug_pathways = load_data("drugbank_partial.xml")

@app.post("/get_number_of_pathways")
def get_drug_pathways(request: DrugRequest):
    """
    Handles requests for pathway interaction count of a drug
    under /get_number_of_pathways endpoint.
    """

    result = df_drug_pathways[df_drug_pathways["Drug-id"] == request.drug_id]

    if result.empty:
        return {"drug_id": request.drug_id, "pathway_count": -1, 
                "message" : "ID not found in DrugBank"}
    else:
        return {"drug_id": request.drug_id, "pathways_count": int(result["Pathways-count"].values[0]),
                "message" : "Success"}
