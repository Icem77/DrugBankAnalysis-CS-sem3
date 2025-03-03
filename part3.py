import xml.etree.ElementTree as ET
import pandas as pd

def drug_and_products_df(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a drug and products connection data frame  which rows consists of:
    - drug id
    - product name
    - manufacturer
    - NDC id
    - dosage form
    - application
    - dose
    - country (registering product)
    - agency (registering product)
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"ID": [], "Product-name": [], "Manufacturer": [], 
            "NDC-id": [], "Dosage-form": [], "Application": [], 
            "Dose": [], "Country": [], "Agency" : [],}

    # iterate through drugs
    for drug in root.findall("db:drug", namespace):
        drug_id = drug.find("db:drugbank-id", namespace)

        products_tag = drug.find("db:products", namespace)
        if products_tag is not None:
            # iterate through products which contain drug
            for product_tag in products_tag.findall("db:product", namespace):
                product_name = product_tag.find("db:name", namespace)
                product_manufacturer = product_tag.find("db:labeller", namespace)
                product_ndc_id = product_tag.find("db:ndc-id", namespace)
                product_dosage_form = product_tag.find("db:dosage-form", namespace)
                product_route = product_tag.find("db:route", namespace)
                product_strength = product_tag.find("db:strength", namespace)
                product_country = product_tag.find("db:country", namespace)
                product_source = product_tag.find("db:source", namespace)

                data["ID"].append(drug_id.text) if drug_id is not None else data["ID"].append(None)
                data["Product-name"].append(product_name.text) if product_name is not None else data["ProductName"].append(None)
                data["Manufacturer"].append(product_manufacturer.text) if product_manufacturer is not None else data["Manufacturer"].append(None)
                data["NDC-id"].append(product_ndc_id.text) if product_ndc_id is not None else data["NDC-id"].append(None)
                data["Dosage-form"].append(product_dosage_form.text) if product_dosage_form is not None else data["Dosage-form"].append(None)
                data["Application"].append(product_route.text) if product_route is not None else data["Application"].append(None)
                data["Dose"].append(product_strength.text) if product_strength is not None else data["Dose"].append(None)
                data["Country"].append(product_country.text) if product_country is not None else data["Country"].append(None)
                data["Agency"].append(product_source.text) if product_source is not None else data["Agency"].append(None)

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = drug_and_products_df("drugbank_partial.xml")
    print(df)