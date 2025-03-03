import xml.etree.ElementTree as ET
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def price_and_manufacturers_count_corelation_df(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file creates a data frame
    which rows contains:
    - drug id
    - number of drug manufacturers (USA/CANADA + other parts of the world)
    - price (USD/ml)

    WARNING: Only drugs for which we know the USD/ml price are included in the 
    data frame.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespace = {"db": "http://www.drugbank.ca"}

    data = {"Drug-id" : [], "USD/ml" : [], "Manufacturers-count" : []}

    for drug in root.findall("db:drug", namespace):
        for price in drug.find("db:prices", namespace).findall("db:price", namespace):
            if "USD/ml" == f"{price.find('db:cost', namespace).get('currency')}/{price.find('db:unit', namespace).text}":
                cost = price.find('db:cost', namespace).text

                int_brands = 0
                if drug.find("db:international-brands", namespace) is not None:
                    int_brands = len(drug.find("db:international-brands", namespace).findall("db:international-brand", namespace))

                manu = 0
                if drug.find("db:manufacturers", namespace) is not None:
                    manu = len(drug.find("db:manufacturers", namespace).findall("db:manufacturer", namespace))

                data["USD/ml"].append(float(cost))
                data["Manufacturers-count"].append(int(int_brands + manu))
                data["Drug-id"].append(drug.find("db:drugbank-id", namespace).text)

    return pd.DataFrame(data)

def draw_price_and_manufacturers_count_corelation_scatter_plot(xml_file_path : str):
    """
    Given an xml_file_path to DrugBank like xml file draws a scatter plot
    which shows the corelation between the number of manufacturs and drug price.
    
    WARNING: Only drugs for which we know the USD/ml price are included on the plot.
    """

    df = price_and_manufacturers_count_corelation_df(xml_file_path)

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))

    scatter = sns.scatterplot(
        data=df,
        x="Manufacturers-count", 
        y="USD/ml",
        hue="USD/ml",  
        palette="coolwarm",  
        size="USD/ml",
        sizes=(50, 500),
        edgecolor="black",
        alpha=0.85
    )

    # annotate extreme values
    max_price = df.loc[df["USD/ml"].idxmax()]
    max_manu = df.loc[df["Manufacturers-count"].idxmax()]

    plt.annotate(
        max_price["Drug-id"], 
        (max_price["Manufacturers-count"], max_price["USD/ml"]),
        textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, fontweight="bold"
    )

    plt.annotate(
        max_manu["Drug-id"], 
        (max_manu["Manufacturers-count"], max_manu["USD/ml"]),
        textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, fontweight="bold"
    )

    plt.xlabel("Number of manufacturers", fontsize=14, fontweight="bold")
    plt.ylabel("Price (USD/ml)", fontsize=14, fontweight="bold")
    plt.title("Correlation between number of manufacturers and price", fontsize=16, fontweight="bold")

    plt.legend(title="Price (USD/ml)", loc="upper right", fontsize=10, title_fontsize=12)
    plt.savefig("statics/price_manufacturers_number_corelation.png", dpi=300, bbox_inches="tight")

    plt.show()

if __name__ == "__main__":
    draw_price_and_manufacturers_count_corelation_scatter_plot("drugbank_partial.xml")