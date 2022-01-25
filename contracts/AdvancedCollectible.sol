//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

//Importing also chainlink to get PROVEN RANDOM BREED for the puppies
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    
    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;


    enum Breed{PUG, SHIBA_INU, ST_BERNARD}


    mapping(bytes32 => address) public requestIdToSender;

    mapping(bytes32 => string) public requestIdToTokenURI;

    mapping(uint256 => Breed) public tokenIdToBreed;

    mapping(bytes32 => uint256) public requestIdToTokenId;


    //VRFCoordinator is the address that will get us a proven random number that will be needed for the NFTs 
    //keyhash is used to prove that the random number is actually random
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Doggies", "DOG"){
        keyHash = _keyhash;
        fee = 0.1 * 10**18; //0.1 LINK is the fee to do a randomness request
        tokenCounter = 0; //initializing the token counter that will represent un INCREMENTATORE ogni volta che mintiamo un NFT
    }

    event requestedCollectible(bytes32 indexed requestId);
    
    //userProvidedSeed is a number provided that will be used by chainlink VRF to proove if it is random
    //When we deploy an NFT, we want it to have a picture. Deploying a picture means deploying a lot of data (using a lot of gas)
    //therefore, how do we render the images without having to deploy the whole image on chain?
    //We'll give the NFT a token URI that points to a specific JSON file
    //The JSON file will represent a METADATA file containing a name, description, image and attributes
    //The images will be stored on IPFS which is a peer-to-peer network in a decantralized manner where we can store data
    //IPFS is used for persistance forever, because if we store the image in a centralized platform, we cannot guarantee that it will remain forever
    //IPFS Uses a persistance network like filecoin  
    function createCollectible(uint256 userProvidedSeed, string memory tokenURI) public returns(bytes32){ 
          bytes32 requestId = requestRandomness(keyHash, fee, userProvidedSeed);

          //when the chainlink node responds, it needs to assign the random number to the correct call
          //When I create a collectible, the random number returned needs to be returned to me and not someone else that may have requested also a random number
          requestIdToSender[requestId] = msg.sender; //WHEN I CREATE A REQUEST, THAT REQUEST IS ASSOCIATED TO ME (MY ADDRESS)
          
          //Needed for the API call to the JSON response
          requestIdToTokenURI[requestId] = tokenURI;

          //testing
          //emitting an event. 
          //everytime we request to create a collectible, this event will be emitted, basically a series of events based on the requestId needed in create_collectible.py
          emit requestedCollectible(requestId);
    }

    //When we call requestRandomness chainlink calls this function 
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override { //overriding 
        //address of the person that created the request
        address dogOwner = requestIdToSender[requestId];

        //Token URI
        string memory tokenURI = requestIdToTokenURI[requestId];

        //Everytime we mint a new NFT we need to give it a token ID.
        uint256 newItemId = tokenCounter;

        //_safeMint is from ERC721 of openzeppelin passing the owner that requested the mint of the nft and the id
        _safeMint(dogOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        //We will use the random number to choose a random attribute like a RANDOM BREED from the Breed ENUM
        Breed breed = Breed(randomNumber % 3); // Dividing the random number by 3 and using the remainder to choose the index of the enum for the breed

        //assign the dog breed to the tokenID
        tokenIdToBreed[newItemId] = breed;

        requestIdToTokenId[requestId] = newItemId;

        tokenCounter = tokenCounter + 1; //Incremento
    }

    //Sets the tokenID to the correct TokenURI
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: transfer caller is not owner nor approved");

        _setTokenURI(tokenId, _tokenURI);
    }
}