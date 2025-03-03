import xml.etree.ElementTree as ET
import pandas as pd

import matplotlib.pyplot as plt

def group_sizes_df(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates
    a data frames which rows consist of:
    - group name
    - number of drugs in the group
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Approved" : 0, "Withdrawned" : 0, "Vet-approved" : 0,
            "Experimental/investigational" : 0}

    for drug in root.findall("db:drug", namespace):
        groups_tag = drug.find("db:groups", namespace)

        if groups_tag is not None:
            for group in groups_tag.findall("db:group", namespace):
                match (group.text):
                    case "approved":
                        data["Approved"] = data["Approved"] + 1
                    case "vet_approved":
                        data["Vet-approved"] = data["Vet-approved"] + 1
                    case "withdrawn":
                        data["Withdrawned"] = data["Withdrawned"] + 1
                    case "investigational" | "experimental":
                        data["Experimental/investigational"] = data["Experimental/investigational"] + 1
                    case _:
                        pass

    return pd.DataFrame(list(data.items()), columns=["Group", "Count"])

def count_approved_and_not_withdrawn(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml counts the number of drugs 
    that were not withdrawned after approval.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    count = 0

    for drug in root.findall("db:drug", namespace):
        groups_tag = drug.find("db:groups", namespace)

        withdrawn = False
        approved = False

        if groups_tag is not None:
            for group in groups_tag.findall("db:group", namespace):
                match (group.text):
                    case "approved":
                        approved = True
                    case "withdrawn":
                        withdrawn = True
                    case _:
                        pass
            
            if approved and not withdrawn: 
                count += 1

    return count

def percentage_of_withdrawned_after_approval_pie_chart(df, approved_and_not_withdrawn):
    """
    Provided with results of group_sizes_df() and count_approved_and_not_withdrawn()
    functions draws a pie chart showing the scale of withdrawals of drugs after approval
    """
    
    labels = ["Approved & not withdrawned", "Withdrawned after approval"]
    sizes = [approved_and_not_withdrawn, 
             df[df["Group"] == "Approved"]["Count"].values[0] - approved_and_not_withdrawn]
    colors = ["#4CAF50", "#FF5733"]  # custom colors
    explode = (0, 0.1)  # explode first slice

    plt.figure(figsize=(9, 9))
    wedges, texts, autotexts = plt.pie(
    sizes, autopct="%1.1f%%", colors=colors, 
    explode=explode, startangle=140, shadow=True
    )

    plt.legend(wedges, labels, title="Drug Categories", loc="lower right", fontsize=9, title_fontsize=12)

    plt.title("Withdrawal of drugs after approval", fontsize=20, fontweight="bold", pad=0)
    plt.savefig("statics/withdrawal_of_approved_drugs.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    frame = group_sizes_df("drugbank_partial.xml")
    approved_and_not_withdrawn = count_approved_and_not_withdrawn("drugbank_partial.xml")

    print(frame)
    print()
    print(f"Approved and not withdrawned: {approved_and_not_withdrawn}")

    percentage_of_withdrawned_after_approval_pie_chart(
        frame,
        approved_and_not_withdrawn
    )

