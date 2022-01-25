#Importing the AdvancedCollectible contract, accounts associated with our private key, network represents the network we are on and the configuration
from brownie import AdvancedCollectible, accounts, network, config
#default network for brownie is ganache

from scripts.helpful_scripts import fund_advanced_collectible

def main():
    #config gets the brownie-config.yaml file
    dev = accounts.add(config['wallets']['from_key'])

    #print(dev)
    publish_source = False #not publishing to etherscan 

    advanced_collectible = AdvancedCollectible.deploy( #calling the constructor of AdvancedCollectible.sol
        config['networks'][network.show_active()]['vrf_coordinator'], #getting the vrf coordinator of rinkeby (if rinkeby is specifies with --network rinkeby when launching the script with brownie run scripts/advanced_collectible/deploy_advanced.py --network rinkeby)
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        {"from":dev}, #we always have to add who is deploying/calling the function
        publish_source = publish_source
    )

    fund_advanced_collectible(advanced_collectible)

    return advanced_collectible

    #in terminal: brownie run scripts/advanced_collectible/deploy_advanced.py --network rinkeby
    # this deploys the smart contract "AdvancedCollectible" which regards our NFT smart contract
    # first transaction regards the deployment TxID: 0x174f496b14275f67ec3b8706e56b0197b4c8413f12579b408e232db3a1dcbe44
    # the second transaction regards FUNDING the smart contract with link:
    # TxID of the funding of LINK to the smart contract: 0xce6862e2b6002db87165f91a740e285769622bcb145ed4d656826d8df4b63154
    # Smart contract of our AdvancedCollectible that handles the puppy NFTS: 0xf810001E6b26146cB9B0384e45eA82D0B3e419FC

