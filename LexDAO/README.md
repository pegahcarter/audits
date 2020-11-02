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


### burn()

While SafeMath is built to revert on overflow/underflow, it should not be used to error check on value sent.  In this case SafeMath is used so that `balanceOf[msg.sender] = balanceOf[msg.sender].sub(value)` will revert when the value sent by `msg.sender` is greater than their balance, without a revert message.

__Suggestion:__ add a condition of `require(value <= balanceOf[msg.sender], "value exceeds balance of msg.sender")` to the start of `burn()`.


## Additional Feedback

### Documentation
None of the contracts reviewed had documentation.  [NatSpec](https://solidity.readthedocs.io/en/latest/natspec-format.html#natspec) is the recommended documentation style and should be used throughout the project.

## Testing
There are no tests for the contracts.  Tests are recommended to check for edge cases and ensure contracts function as expected.  I would recommend [Hardhat](https://hardhat.org).


## Disclaimer
This audit was performed at no cost to LexDAO.  This report is not investment advice and in no way proof of a perfect smart contract.  This audit was done to the best of Carl Farterson's ability and focused on several of the primary contracts.

