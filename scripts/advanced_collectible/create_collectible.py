from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_breed
import time

STATIC_SEED = 123

def main():
    dev = accounts.add(config['wallets']['from_key'])

    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1] #getting the most recent deployment of advanced collectible

    transaction = advanced_collectible.createCollectible(STATIC_SEED, "None", {"from": dev})

    transaction.wait(1) #waiting for the transaction to finish with 1 confirmation

    
    #getting the requestId of the dog getting the event we emitted in the AdvancedCollectible contract
    requestId = transaction.events['requestedCollectible']['requestId'] #we're getting the event requestedCollectible and the requestId of the transaction just done above

    #getting the tokenId based off of the requestId from the mapping in the AdvancedCollectible contract
    token_id = advanced_collectible.requestIdToTokenId(requestId) #this gets the tokenId from the 'requestIdToTokenId' which is public so we can call it like this

    time.sleep(45) #waiting for like 35 seconds hoping that by this time the second transaction by the chainlink node (for the random number to generate the breed) has been done.

    #using the token_id I can get the breed of the dog I just created (minted)
    breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))

    print('Dog breed of tokenId {} is {}.'.format(token_id, breed)) 

    #to execute: brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby
    #to verify:
    #brownie console --network rinkeby
    #get the most recent deployment of AdvancedCollectible contract: advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    #then just get the breed of the one just deployed (which is just 1 so it will have id 0):
    # advanced_collectible.tokenIdToBreed(token_id) #this should print the breed 
    # If it's wrong for example i got breed equal to 1 which is shiba inu and previously it printed PUG it means we didn't wait long enough for chainlink to respond


