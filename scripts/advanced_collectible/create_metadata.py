from brownie import AdvancedCollectible, network
#here we will create the metadata for our NFTs.
#metadata is data regarding the NFT attributes we cannot store directly in the smart contract
#but with the tokenURI we associate the metadata of the NFT.
#metadata includes also the image stored in a decentralized way with IPFS

from metadata import sample_metadata
from scripts.helpful_scripts import get_breed

from pathlib import Path

import os

import requests

import json

def main():
    print("Working on " + network.show_active())

    advanced_collectible  = AdvancedCollectible[len(AdvancedCollectible) - 1]

    #we need to get our nft just minted, therefor we need the tokenId of the NFT to get it's breed so we can assign the correct image of the dog

    number_of_tokens = advanced_collectible.tokenCounter() #number of nfts minted
    print("The number of tokens (NFTs) deployed: " + str(number_of_tokens))

    write_metadata(number_of_tokens, advanced_collectible) #I want to write metadata for each token deployed


def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template 
        breed = get_breed(nft_contract.tokenIdToBreed(token_id)) #getting the breed for each token deployed
        metadata_file_name = ( 
            "./metadata/{}/".format(network.show_active()) + str(token_id) + "-" + breed + ".json" #creating this json file with this name and path
        )

        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating Metadata File: {}".format(metadata_file_name))
            collectible_metadata["name"] = get_breed(nft_contract.tokenIdToBreed(token_id))
            collectible_metadata["description"] = "An adorable {} pup!".format(collectible_metadata["name"])

            print(collectible_metadata)

            #Now we need to use IPFS to upload the image and the json.
            #First download IPFS Command-Line LINUX: https://docs.ipfs.io/install/command-line/#official-distributions
            #then start it with
            # ipfs daemon 
            # download ipfs companion on chrome extension and go to settings and change port to 5002 so it doesn't conflict with the local one

            image_to_upload = None

            if os.getenv("UPLOAD_IPFS") == "true": #only if the environment variable is true
                image_path = "./img/{}.jpg".format(breed.lower().replace("_","-"))
                image_to_upload = upload_to_ipfs(image_path)

            collectible_metadata["image"] = image_to_upload

            with open(metadata_file_name, "w") as file: #writing the file in the directory metadata/rinkeby/
                json.dump(collectible_metadata, file)       

            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name) #we need to upload to ipfs also the metadata file       

#we want to upload our images with python to IPFS
# with curl we just had to do:
# curl -X POST -F file=@img/pug.png http://localhost:5001/api/v0/add            

#with python:

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp: #opening the image as binary
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary}) #api/v0/add can be found in the IPFS HTTP commands of the IPFS API documentation
        print(response.json()) #gave us the response and a hash: QmdjRoYnPQ3Givcg46zxtECmEwA9DSMHUkiX9QcFwof19w of the file

        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]

        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)

        print(uri)

        return uri