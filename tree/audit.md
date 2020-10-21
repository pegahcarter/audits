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
* `initContracts(address _rebaser, address _reserve)`
    * Set the initial `rebaser` and `reserve` addresses
* `ownerMint(address account, uint256)`
    * The EOA that deployed the address can mint TREE tokens
* `rebaserMint(address account, uint256)`
    * Gives `rebaser` the ability to mint TREE tokens
* `reserveBurn(address account, uint256)`
    * Gives `reserve` the ability to burn TREE tokens 

### TREERebaser.sol
* `rebase()`: Perform the TREE rebase by:
    * Determining if TREE price is above the price peg (1.01 yUSD <= price <= 1.10 yUSD)
    * If TREE price is above, calculate difference in current price to price peg and apply `multiplier` (0.05x <= multiplier <= 10x) to get `indexDelta`
    * Multiply `indexDelta` to current supply to determine quantity of new TREE minted as `supplyChangeAmount`
    * Mint TREE to the `reserve` address using `tree.rebaserMint()`
    * Let `reserve` perform actions with the minted TREE with `reserve.handlePositiveRebase(supplyChangeAmount)`
* `_treePrice()`:
    * fetch TREE price from the `oracle`
* `setGov(address _newValue)`:
    * Set `gov` to a new address
* `setOracle(address _newValue)`:
    * Set `oracle` to a new address
* `setMinimumRebaseInterval(uint256 _newValue)`:
    * Set `minimumRebaseInterval` to a new value
* `setDeviationThreshold(uint256 _newValue)`:
    * Set `deviationThreshold` to a new value
* `setRebaseMultiplier(uint256 _newValue)`:
    * Set `rebaseMultiplier` to a new value


### TREEReserve.sol
* `initContracts(_rebaser)`
    * Set the initial `rebaser` address
* `handlePositiveRebase(uint256 mintedTREEAmount)`
    * Calculate then send the quantity of TREE to `lpRewards` from the `mintedTREEAmount`
    * Sell remaining `mintedTREEAmount` for `reserveToken` using _`sellTREE(remainingTREEAmount)`
    * Burn unsold TREE due to limited Uniswap liquidity using `tree.reserveBurn()`
    * Calculate then send a percentage of `reserveToken` to `charity`
* `burnTREE(uint256 amount)`
    * Burn TREE for msg.sender using `tree.reserveBurn()`
    * Calculate then send the quantity of `reserveToken` based on quadratic shares
* `_sellTREE(uint256 amount)`
    * Fetch uniswap reserves
    * Calculate max TREE to sell so that price doesn't go below peg using `_uniswapMaxSellAmount()` 
    * Swap TREE for uniswap pair
* `_uniswapMaxSellAmount(uint256 token0Reserves, uint256 token1Reserves)`
    * Use token reserves for the TREE uniswap pair to calculate how much TREE to sell 



* `setGov(address _newValue)`
    * set Gov to a new address
* `setCharity(address _newValue)`
    * set Charity to a new address 
* `setLPRewards(address _newValue)`
    * set LPRewards to a new address 
* `setUniswapPair(address _newValue)`
    * set UniswapPair to a new address 
* `setUniswapRouter(address _newValue)`
    * set UniswapRouter to a new address 
* `setOmniBridge(address _newValue)`
    * set OmniBridge to a new address 
* `setCharityCut(uint256 _newValue)`
    * set CharityCut to a new value
* `setRewardsCut(uint256 _newValue)`
    * set RewardsCut to a new value

## Areas of Concern

### Governance
1. `setGov()`
2. No minimum time locks on governance

### rebaseMultiplier (TREERebaser.sol)
The `rebaseMultiplier` variable can range between 0.05x and 10x.  This is a range of 2000x (0.05 * 2000 = 10) and is unnecessarily large.  Large changes in `rebaseMultiplier` may have unintended consequences on TREE price and supply.

### Quadratic burning
Where quadratic voting favors the smaller vote, quadratic burning favors the larger burn

|---|---|
|Quadratic Voting|
| # of votes | Cost |
| 1 | 1  |
| 2 | 4  |
| 5 | 25 |
| 10| 100|
| 100| 10000|


| Quadratic Burning |
| % Supply burned |  % of reserves received |
| 0.01 | 0.0001 |

| 10 | 1 |

