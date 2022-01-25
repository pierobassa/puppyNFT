from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_advanced_collectible

def main():
    #brownie gives us the AdvancedCollectible as a big list of all the deployments (NFTs) of the AdvancedCollectible
    #so we can get the length
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) -1]
    
    fund_advanced_collectible(advanced_collectible)