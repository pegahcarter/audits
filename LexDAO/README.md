# LexDAO audit
## Carl Farterson

## Scope
This audit covers LexDAO's LEX token contracts on commit [`498bf4b`](https://github.com/lexDAO/LexCorpus/tree/498bf4b50ae5f6c4719998346f6f5a54ba273537).  Contracts reviewed are within [`contracts/token/lextoken/solidity`](https://github.com/lexDAO/LexCorpus/tree/498bf4b50ae5f6c4719998346f6f5a54ba273537/contracts/token/lextoken/solidity).

# LexToken

[LexToken](https://github.com/lexDAO/LexToken) represents assets with LexDAO smart contracts and legal wrappers.

## Use LexToken

You can deploy a LexToken on Ethereum mainnet: [0x3F59353034424839dbeBa047991f3E54E1AD19E5](https://etherscan.io/address/0x3F59353034424839dbeBa047991f3E54E1AD19E5#code). 


### init()

There is no check that `_managerSupply` and `_saleSupply` is <= `_totalSupplyCap`.  If the supply is greater for `_managerSupply` and `_saleSupply`, it would lead to init() reverting when attempting to mint `_saleSupply`.  `DOMAIN_SEPARATOR` would not be set, leading to a broken `permit()` function.

__Suggestion:__ Add a condition of `require(_managerSupply.add(_saleSupply) <= totalSupplyCap, "_managerSupply + _saleSupply > totalSupplyCap")` to `init()` before variables are set.


### updateSale()

If `_saleSupply + totalSupply > totalSupplyCap`, the mint will revert but only after updating `saleRate` and `forSale` variables, and will not emit `UpdateSale`, even though variables were updated.

__Suggestion:__ TODO 

If you are only trying to update `_saleRate` or `_forSale`, `_saleSupply = 0` will still call `_mint()` even though no new tokens were created for the sale.

__Suggestion:__ TODO


An additional functionality to `updateSale()` that would be beneficial is an option to burn the tokens for sale.  In the current implementation, tokens are able to be created and sent to the contract, but once they're in the contract they're only able to be removed through purchase.

A scenario where this would play out would be if you had a token sale for a duration of time and not all tokens were sold.  With the current implementation, the best you could do after the sale would be to set `forSale` to `false`.  Then, if you wanted to have a second token sale, you would not be able to sell less tokens than what was not sold in the first round.





### receive()
An address can purchase tokens from the contract by sending ETH to the contract.  



### withdrawToken()
`withrawTo` is misspelled and should be `withdrawTo` 



## Additional Feedback

### Documentation
None of the contracts reviewed had documentation.  [NatSpec](https://solidity.readthedocs.io/en/latest/natspec-format.html#natspec) is the recommended documentation style and should be used throughout the project.

## Testing
There are no tests for the contracts.  Tests are recommended to check for edge cases and ensure contracts function as expected.  I would recommend [Hardhat](https://hardhat.org).


## Disclaimer
This audit was performed at no cost to LexDAO.  This report is not investment advice and in no way proof of a perfect smart contract.  This audit was done to the best of Carl Farterson's ability and focused on several of the primary contracts.

