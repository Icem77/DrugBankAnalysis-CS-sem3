# DrugBankAnalysis-CS-sem3

This project involves analyzing a subset of the DrugBank database—a public, free resource containing detailed information about drugs and therapeutic substances. For this project we will work with a trimmed version provided as `drugbank_partial.xml`, which includes data for 100 drugs.

The goal of this project is to extract, analyze, and visually present various aspects of the drug data. In addition, we will extend the analysis by generating a larger test dataset and building a RESTful service for interactive queries.

## Project Overview 💊\n

The project consists of several tasks that cover data extraction, data transformation, visualization and simulation. The main areas include:

- **Data Extraction and DataFrames:** 💊\n
  Create structured dataframes to capture essential information for each drug, including unique identifiers, names, types, descriptions, dosage forms, indications, mechanisms of action, and interactions (with food, pathways, proteins, etc.).

- **Graphical Visualization:** 💊\n
  Generate graphs such as synonym graphs using NetworkX, bipartite graphs showing drug-pathway interactions, histograms, and pie charts. The visualizations should be clear, attractive, and informative.

- **Simulated Data Generation:** 💊\n
  Develop a simulator that creates a test database of 20,000 drugs by generating consecutive DrugBank IDs for 19,900 new entries and populating other fields with values sampled from the original 100 drugs.

- **Web Service:** 💊\n
  Implement a RESTful service (using FastAPI and Uvicorn) that, for example, accepts a drug ID via a POST request and returns specific analytical results, as demonstrated in one of the tasks.

## Detailed Tasks 💊\n

1. **Drug Data DataFrame:** 💊\n
   Build a dataframe that for each drug contains:
   - Unique DrugBank ID
   - Drug name
   - Drug type
   - Description
   - Dosage form
   - Indications
   - Mechanism of action
   - Interactions with food  

2. **Synonyms and Graphs:** 💊\n
   Create a dataframe for searching DrugBank IDs for all synonyms under which each drug is known. Write a function that, for a given DrugBank ID, builds and displays a synonym graph using NetworkX. Ensure the graph is readable.  

3. **Pharmaceutical Products DataFrame:** 💊\n
   Create a dataframe detailing pharmaceutical products that contain a given drug (active ingredient). The dataframe should include:
   - Drug ID
   - Product name
   - Manufacturer
   - National Drug Code (NDC)
   - Dosage form
   - Application method
   - Dosage information
   - Country and registering agency  

4. **Pathways DataFrame:** 💊\n
   Build a dataframe that captures information on all pathways (e.g., signaling, metabolic, etc.) that any drug interacts with. Also, provide the total count of these pathways.  

5. **Drug-Pathway Interactions:** 💊\n
   For each signaling/metabolic pathway, list the drugs that interact with it. Present the results both as a dataframe and using a custom graphical representation (e.g., a bipartite graph where one node set represents pathways and the other drugs).  

6. **Pathway Histogram:** 💊\n
   For every drug, determine the number of pathways it interacts with. Visualize the distribution using a histogram with properly labeled axes.  

7. **Protein (Target) DataFrame:** 💊\n
   Create a dataframe containing information about proteins (targets) with which drugs interact. Include at least:
   - Target's DrugBank ID
   - Source (e.g., Swiss-Prot)
   - External database identifier
   - Peptide name
   - Gene name encoding the peptide
   - GenAtlas ID
   - Chromosome number
   - Subcellular location  

8. **Target Location Pie Chart:** 💊\n
   Generate a pie chart displaying the percentage distribution of targets across different cellular compartments.  

9. **Drug Approval Status:** 💊\n
   Construct a dataframe summarizing how many drugs are approved, withdrawn, experimental/investigational, and approved for animal use. Visualize this information in a pie chart. Also, provide the count of approved drugs that have not been withdrawn.  

10. **Drug Interactions DataFrame:** 💊\n
    Create a dataframe that captures information about potential interactions between a given drug and other drugs.  

11. **Custom Graphical Presentation:** 💊\n
    Develop graphical presentation that links specific gene(s) with:
    - Drugs interacting with the gene(s)
    - Pharmaceutical products containing the related drug(s)  
    (Solved by creating layered star-graph)

12. **Corelation between price and number of manufacturers:** 💊\n 
    Test the hypothesis: Does bigger concurrency on the market lead to lower prices of drugs? Present the data on the scatter plot.
    
14. **Test Database Simulator:** 💊\n
    Create a simulator that generates a test database with 1000 drugs. The first 900 entries in the “DrugBank Id” column should be sequential numbers, while the other columns should contain values randomly selected from the existing 100 drugs. Save the generated data as `drugbank_partial_and_generated.xml` and perform the analyses from tasks 1–12 on this test dataset.  

15. **RESTful Service for Drug Queries:** 💊\n
    Modify task 6 so that it is possible to send a drug ID to your server, which then returns the analysis result. Implement the server using FastAPI and Uvicorn. A demonstration via a POST request (e.g., using the Execute feature in the documentation) is sufficient.  
