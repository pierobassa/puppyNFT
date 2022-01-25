from brownie import AdvancedCollectible, accounts, config, interface, network

def fund_advanced_collectible(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])

    #now we need to send the Link token. Here is where we need interfaces!
    #whenever you interact with a smart contract on chain, you need 2 things:
    # 1) the interface (or abi)
    # 2) the address
    # the interface is secretely a way to get the abi. The abi defines the way to interact with a smart contract

    link_token = interface.LinkTokenInterface(config['networks'][network.show_active()]['link_token']) #getting the address of the link token because it changes based on the network used. We specified the address for the rinkeby network

    #sending 0.1LINK to the nft_contract
    link_token.transfer(nft_contract, 100000000000000000, {"from": dev})

def get_breed(breed_number):
    switch = {
        0: 'PUG',
        1: 'SHIBA_INU',
        2: 'ST_BERNARD'
    }

    return switch[breed_number]
