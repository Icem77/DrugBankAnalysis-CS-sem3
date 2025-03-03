import xml.etree.ElementTree as ET
import random

def simulate_drugbank(xml_file_path : str, generated_size : int, new_name : str):
    """
    Given an xml_file_path to DrugBank xml file creates an DrugBank like xml file 
    with given name which apart from the drugs from original file contains
    given amount of randomly generated drugs.
    Id's of those drugs are continous numbers starting from 0. Other columns  are
    randomly selected from those in original drugs.
    """
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    tags = {"types" : []}

    for drug in root.findall("db:drug", namespace):
        tags["types"].append(drug.attrib["type"])
        for element in drug:
            tag_name = element.tag.split("}")[1]
            if tag_name not in tags.keys():
                tags[tag_name] = []
            
            tags[tag_name].append(element)

    tags.pop("drugbank-id")

    NAMESPACE = "http://www.drugbank.ca"
    ET.register_namespace("", NAMESPACE)  # ensures namespace in the output

    new_root = ET.Element(f"{{{NAMESPACE}}}drugbank")

    for i in range(generated_size):
        new_drug = ET.Element(f"{{{NAMESPACE}}}drug")
        new_drug.set("type", random.choice(tags["types"]))

        id = ET.Element(f"{{{NAMESPACE}}}drugbank-id")
        id.set("primary", "true")
        id.text = str(i)
        new_drug.append(id)

        for tag, value in tags.items():
            if tag != "types":
                new_drug.append(random.choice(value))

        new_root.append(new_drug)

    for drug in root.findall("db:drug", namespace):
        new_root.append(drug)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(new_name, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    simulate_drugbank("drugbank_partial.xml", 1000, "generated/drugbank_partial_and_generated.xml")
