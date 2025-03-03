import requests
from requests.exceptions import ConnectionError

def pathway_count_server_request(drug_id : str):
    """
    Sends a request for the number of pathwyas that interact 
    with drug under given id to a local server and prints out
    the response.
    """

    url = "http://127.0.0.1:9000/get_number_of_pathways"
    data = {"drug_id": drug_id}
    
    try:
        response = requests.post(url, json=data)
        print(response.json())
    except ConnectionError:
        print("ERROR: Unable to estabilish connection with local server")

if __name__ == "__main__":
    prefix = "DB0000"
    for i in range(1, 10):
        pathway_count_server_request("DB0000" + str(i))