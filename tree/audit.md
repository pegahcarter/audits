# WhalerDAO/tree-contracts

## Scope
This audit covers smart contracts on commit [`9d4f735ab9a1e7ae3310069ab637c9bec4e72d21`](https://github.com/WhalerDAO/tree-contracts/tree/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21)



## Validating README
Below is a summary of the [README](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/README.md) which compares the README to the codebase.

### Rebase
* [x] When the price of 1 TREE exceeds 1.05 yUSD, a rebase will be triggered, minting TREE proportional to the price deviation. Unlike Ampleforth and Yam, TREE does not have negative rebases when the price drops below 1 yUSD.
    * [Location](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/contracts/TREERebaser.sol#L133)
    * Minimum of price deviation to trigger rebase is [1.01 yUSD, max is 1.10 yUSD](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/contracts/TREERebaser.sol#L51)



## Areas of Concern

## Initialization
* Within `Rebaser.sol`, there are no checks for `deviationThreshold`, `minimumRebaseInterval`, `rebaseMultiplier` to validate variables are within the acceptable range.  For `TREERebaser.sol`, `charityCut` and `rewardsCut` are not validated.
