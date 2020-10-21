# WhalerDAO/tree-contracts

## Scope
This audit covers smart contracts on commit [`9d4f735ab9a1e7ae3310069ab637c9bec4e72d21`](https://github.com/WhalerDAO/tree-contracts/tree/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21)



## Validating README
Below is a summary of the [README](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/README.md) which compares the README to the codebase.

### Rebase
* [x] [When the price of 1 TREE exceeds 1.05 yUSD, a rebase will be triggered, minting TREE proportional to the price deviation.  TREE will not rebase when price is below 1 yUSD.](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/contracts/TREERebaser.sol#L133)
    * [1.01 yUSD, max is 1.10 yUSD](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/contracts/TREERebaser.sol#L51)
* [x] Of the minted TREE, 10% is sent to a rewards pool for TREE-yUSD UNI-V2 liquidity providers, 10% is sold for yUSD and sent to the charity DAO, and 80% is sold for yUSD and put into the reserve.



## Contracts
### TREE.sol
* `initContracts()`: Set the initial `rebaser` and `reserve` addresses
* `ownerMint()`: The EOA that deployed the address can mint TREE tokens
* `rebaserMint()`: Gives `rebaser` the ability to mint TREE tokens
* `reserveBurn()`: Gives `reserve` the ability to burn TREE tokens 




## Areas of Concern

### Governance
