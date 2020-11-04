# LexDAO audit
## Carl Farterson

## Scope
This audit covers LexDAO's LEX token contracts on commit [`498bf4b`](https://github.com/lexDAO/LexCorpus/tree/498bf4b50ae5f6c4719998346f6f5a54ba273537).  Contracts reviewed are within [`contracts/token/lextoken/solidity`](https://github.com/lexDAO/LexCorpus/tree/498bf4b50ae5f6c4719998346f6f5a54ba273537/contracts/token/lextoken/solidity).


## Overview
LexDAO is a group of legal engineering professionals who are seeking to provide a trusted layer between the decentralized world of blockchains and legal settlement layer in the real world.  LexDAO provides a tool to tokenize yourself with the "LexDAO Certified Personal Token Factory", where you can mint personal tokens based on Ethereum through the LexDAO website.

A token factory (technically speaking, a "clone factory") is used to efficiently deploy the same type of contract repeatedly.  Instead of deploying all new code for each contract, you can create a generalized contract that you plan to use which will accept different parameters when created.  LexDAO uses a custom token factory to create personal tokens, where different parameters may include token symbol, supply, token manager address, etc.  An additional functionality of the LexDAO token factory is to award an address with a `userReward` quantity of `lexDAOtoken` when it uses the factory to launch a token.

The beauty of LexToken is in its' simplicity.  250 lines of code is used to deploy personal tokens with SafeMath and a brief ERC20 interface, with an additional 96 lines of code used for the token factory.


## Contracts Reviewed
* LexToken.sol
* LexTokenFactory.sol

### LexTokenFactory.sol
The token factory to create personal tokens.

* `contract CloneFactory`
    * Follows [EIP-1167](https://eips.ethereum.org/EIPS/eip-1167) guidelines to create simple contract clones.  Code matches the template of function `createClone` found in an example clone factory [repository](https://github.com/optionality/clone-factory/blob/32782f82dfc5a00d103a7e61a17a5dedbd1e8e9d/contracts/CloneFactory.sol#L32).

* `contract LexTokenFactory`
    * Utilizes `CloneFactory` to launch personal tokens.
    * Variables
        * `lexDAO`: address allowed to update governance
        * `lexDAOtoken`: token rewarded to an address that use the contract to deploy a personal token
        * `template`: generic personal token contract that is copied for each new token deployment
        * `userReward`: amount of tokens rewarded when a personal token is deployed
        * `details`: contains additional information
    * Functions
        * `launchLexToken()`: creates personal tokens and rewards the token creator the `userReward` amount of `lexDAOtoken`
        * `updateGovernance()`: used to update `lexDAO`, `lexDAOtoken`, `userReward`, and `details` variables, called by `lexDAO`

### LexToken.sol
The ERC20-like token launched from `LexTokenFactory`.  There are some key additions to the ERC20 standard worth noting:
1. The contract is able to sell its' token when ETH is sent to the contract.
2. The contract manager is able to disable token transfers.
3. The contract manager and resolver are able to withdraw tokens from addresses and send those tokens to addresses of their choice.
4. LexToken utilizes [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) to combine approve and transfers into one transaction.  It also allows gasless token transfers by paying for gas in the token and allowing someone else to pay for the gas cost entirely.


* `interface IERC20`: brief ERC-20 interface

* `library SafeMath`: arithmatic wrapper for uint under/overflow check

* `contract LexToken`
    * Variables
        * `manager`: account managing token rules and sale - updateable by `manager`
        * `resolver`: account acting as backup for lost token and arbitration of disputed token transfers - updateable by `manager`
        * `decimals`: fixed unit scaling factor - default 18 to match ETH
        * `saleRate`: rate of tokens purchased when sending ETH to contract - updateable by `manager`
        * `totalSupply`: tracks outstanding token mint - updateable by `manager`
        * `totalSupplyCap`: maximum of token mintable
        * `DOMAIN_SEPARATOR`: EIP-2612 permit() pattern - hash identifies contract
        * `PERMIT_TYPEHASH`: EIP-2612 permit() pattern - hash identifies function
        * `details`: details token offering, redemption, etc. - updateable by `manager`
        * `name`: fixed token name
        * `symbol`: fixed token symbol
        * `forSale`: status of token sale - e.g. if `false`, ETH sent to token address will not return token per saleRate - updateable by `manager`
        * `initialized`: internally tracks token deployment to signify contract creation
        * `transferable`: transferability of token - does not affect token sale - updateable by `manager`
    * Functions
        * `init()`: Runs at contract creation and sets variables
        * `receive()`: Handles ETH sent to the contract and returns the contract token to the sender if a token sale is active 
        * `approve()` and `_approve()`: Allow an address to send an amount of the sender's tokens
        * `balanceResolution()`: Resolve disputed or lost balances, called by `resolver`
        * `burn()`: Remove tokens from the token supply from an address
        * `permit()`: Allow an address to spend your tokens until a specified deadline
        * `transfer()` and `_transfer`: Transfer tokens from one address to another address
        * `transferBatch()`: Transfer tokens from one address to many addresses at once
        * `transferFrom()`: Use a permitted address to send your tokens to another address
        * `mint()` and `_mint()`: Generate tokens and send to a specified address, called by `manager`
        * `mintBatch()`: Generate tokens and send to many addresses at once, called by `manager`
        * `updateGovernance()`: Modify `manager`, `resolver`, and `details`, called by `manager`
        * `updateSale()`: Modify `saleRate` and `forSale`, and mint tokens to the contract address to sell, called by `manager`
        * `updateTransferability()`: Modify `transferable`, called by `manager`
        * `withdrawToken()`: Withdraw many ERC20-like tokens from the contract address at once to one address, called by `manager`


## Suggestions

### updateSale()
If you are only trying to update `_saleRate` or `_forSale`, `_saleSupply = 0` will still call `_mint()` even though no new tokens were created for the sale.

__Suggestion:__ Add a conditional statement to only mint when `_saleSupply != 0`.
```Javascript
if (_saleSupply != 0) {_mint(address(this), _saleSupply);}
```

An additional functionality to `updateSale()` is an option to burn the tokens for sale.  In the current implementation, tokens are able to be created and sent to the contract, but once they're in the contract they're only able to be removed through purchase or calling `withdrawToken()`.  As `withdrawToken()` is built to transfer multiple tokens, I would argue `withdrawToken()` is meant to handle ERC-20 tokens other than the contract token.

A scenario where this would play out would be if you had a token sale for a duration of time and not all tokens were sold.  With the current implementation, the best you could do after the sale to remove the tokens from circulation would be for the `manager` to call `withdrawToken()` to send the remaining tokens to an external address, then call `burn()`.  However, this adds an additional layer of risk as the external address would have control of the tokens before burning them.  Burning the tokens directly from the contract removes that risk. 

__Suggestion:__ add a boolean `burnTokens` paramater to `updateSale()` to indicate when tokens for sale are burned.

```Javascript
function updateSale(uint256 _saleRate, uint256 _saleSupply, bool _forSale, bool burnTokens) external onlyManager {
    saleRate = _saleRate;
    forSale = _forSale;

    if (_saleSupply != 0 && !burnTokens) {
        _mint(address(this), _saleSupply);
    }

    if (_saleSupply != 0 && burnTokens) {
        burn(address(this), _saleSupply);
    }

    emit UpdateSale(_saleRate, _saleSupply, _forSale, burnTokens);
}
```

__Suggestion:__ To further standardize events, `UpdateSale` should include all parameters used in `updateSale()`.  This is to align with the events within `updateGovernance` and `updateTransferability` that accept all of their respective function parameters.


### receive()
An address can purchase tokens from the contract by sending ETH to the contract, and receives a multiple of how much ETH was sent through `msg.value.mul(saleRate)`.  This ratio is one-directional, meaning you cannont receive less than a 1:1 return for ETH deposited.  If the token has a low supply, a sell ratio of 1:1 may be too high, and instead would want senders to receive a fraction of the quantity received.  In addition, a fixed 1:1 ratio pegs the token sell price to ETH price, which may not be preferred.

__Suggestion:__ Create a `saleRate` ratio using the 18 decimal places ETH and LEX token utilize for additional flexilibity in token pricing.

```Javascript

library SafeMath {
    ...
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
}

contract LexToken {
    
    uint256 public constant PRECISION = 10**18;
    saleRate = 5 * 10**17;  // 50%

    receive() external payable { // SALE 
        require(forSale, "!forSale");
        (bool success, ) = manager.call{value: msg.value}("");
        require(success, "!ethCall");
        _transfer(address(this), msg.sender, msg.value.mul(saleRate.div(PRECISION)));
    } 

}
```

### withdrawToken()
`withrawTo` is misspelled.

__Suggestion:__ change `withrawTo` to `withdrawTo`.


## Additional Feedback

### Documentation
Neither of the contracts reviewed had proper documentation.  [NatSpec](https://solidity.readthedocs.io/en/latest/natspec-format.html#natspec) is the recommended documentation style and should be used throughout the project.

## Testing
There are no tests for the contracts.  Tests are recommended to check for edge cases and ensure contracts function as expected.  I recommend [Hardhat](https://hardhat.org).


## Disclaimer
This audit was performed at no cost to LexDAO.  This report is not investment advice and in no way proof of a perfect smart contract.  This audit was done to the best of Carl Farterson's ability and focused on LexDAO's implementation of LexToken.

