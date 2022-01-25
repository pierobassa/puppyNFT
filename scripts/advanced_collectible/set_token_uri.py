from brownie import AdvancedCollectible, network, config, accounts
from scripts.helpful_scripts import get_breed

dog_metadata_dic = {
    "SHIBA_INU": "https://gateway.pinata.cloud/ipfs/QmVAhARxc7Lbksu5AeBkAPo1pUGrRwfx35FVSmxkCaupi8",
    "PUG" : "https://gateway.pinata.cloud/ipfs/QmNgNAjGBySivNs84yCGnAVndpWH3JPYtJC7ysqagYS5v6",
    "ST_BERNARD": "https://gateway.pinata.cloud/ipfs/QmQMqXGXsdhaPh2XZ41BnGpZfZctmnbQLL7J46VqxiTwtP"
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    print("Working on " + network.show_active())

    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]

    print("The number of tokens (NFTs) deployed: " + str(advanced_collectible.tokenCounter()))

    number_of_advanced_collectibles = advanced_collectible.tokenCounter()

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))

        if advanced_collectible.tokenURI(token_id).startswith("None"): #If i haven't already set the tokenURI of the NFT. So if this token with id "token_id" doesn't have a tokenURI set (it's set to None) then we'll set it
            print("Setting tokenURI of {}".format(token_id))
            
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])
        else:
            print("Skipping {}, we've already set that tokenURI!".format(token_id))

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])

    nft_contract.setTokenURI(token_id, tokenURI, {"from":dev})

    print("Awesome! you can now view your NFT at {}".format(OPENSEA_FORMAT.format(nft_contract.address, token_id)))
 
    print("Please give up to 20 minutes and hit the 'refresh metadata' button!")