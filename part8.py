import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def percentage_presence_of_drugs_in_cell_parts_pie_chart(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a png file with a pie chart representing percentage presence of drugs
    from the database in different cellular locations.
    """
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    namespace = {"db": "http://www.drugbank.ca"}
    cellular_locations_with_count = {}

    for drug in root.findall("db:drug", namespace):
        targets_tag = drug.find("db:targets", namespace)
        if targets_tag is not None:
            for target in targets_tag.findall("db:target", namespace):
                polypeptides = target.findall("db:polypeptide", namespace)
                if len(polypeptides) == 0:
                    # handle missing polypeptides
                    cellular_locations_with_count[None] = cellular_locations_with_count.get(None, 0) + 1
                else:
                    for polypeptide in polypeptides:
                        cellular_location = polypeptide.find("db:cellular-location", namespace).text
                        # count occurrences of each cellular location
                        cellular_locations_with_count[cellular_location] = cellular_locations_with_count.get(cellular_location, 0) + 1

    # labels and sizes from dictionary
    labels = list(cellular_locations_with_count.keys())  
    sizes = list(cellular_locations_with_count.values())  
    
    # calculate percentages
    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]

    colors = plt.cm.Paired.colors 

    # create the pie chart without percentages on the pie itself
    plt.figure(figsize=(10, 10))  
    wedges, texts = plt.pie(
        sizes, startangle=140, shadow=True, 
        colors=colors, textprops={"fontsize": 12, "fontweight": "bold"}
    )

    # add the percentages to the legend
    legend_labels = [f"{label} ({percentage:.1f}%)" for label, percentage in zip(labels, percentages)]
    
    plt.legend(
        wedges, legend_labels, title="Cellular locations", 
        loc="center left", fontsize=12, title_fontsize=14,
        bbox_to_anchor=(1.00, 0.5)  # places the legend to the right of the pie chart
    )

    plt.title("Percentage Presence of Targets in Cellular Locations", fontsize=20, fontweight="bold", pad=0)

    plt.savefig("statics/percentage_targets_cellular_locations.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
   percentage_presence_of_drugs_in_cell_parts_pie_chart("drugbank_partial.xml")