'''
Created on Jul 6, 2021

@author: yann
'''

import requests
import json
from pprint import pprint

API_KEY = "2b10pWROcUivctTkk45sSIwb"  # Set you API_KEY here
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

image_path_1 = "../data/image_1.jpg"
image_path_2 = "../data/image_2.jpg"

def __get_img_data(img_path):
    return open(img_path, 'rb')

def send_request(img_path):
    
    data = {
        'organs': ['flower']
    }
    
    files = [
        ('images', (img_path, __get_img_data(img_path)))
    ]
    
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()
    
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    
    pprint(response.status_code)
    #pprint(json_result)
    return json_result
    
def get_most_probable_species(request, verbose=False):
    try:
        species = request.get("results")[0].get('species')
        if verbose :
            print(species)
        return species
    except TypeError:
        pass
    
def get_most_probable_species_confidence(request, verbose=False):
    try:
        score = request.get("results")[0].get("score")
        if verbose :
            print(score)
        return "{:.2f}".format(score * 100)
    except TypeError:
        pass
    