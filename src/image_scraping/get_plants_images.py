'''
Created on Jul 6, 2021

@author: yann
'''

from simple_image_download import SID

response = SID

def download_species_image(species):
    response().download(species, 1)