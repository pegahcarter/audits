# WhalerDAO/tree-contracts

## Scope
This audit covers smart contracts from [`github.com/WhalerDAO/tree-contracts`](https://github.com/WhalerDAO/tree-contracts) on commit [`9d4f735 `](https://github.com/WhalerDAO/tree-contracts/tree/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21).


### [README](https://github.com/WhalerDAO/tree-contracts/blob/9d4f735ab9a1e7ae3310069ab637c9bec4e72d21/README.md) Summary
* DAOs/pools
    * TREE-yUSD uniswap pool
    * charity DAO
    * reserve (holds yUSD from rebases)
* Rebases
    * Only happens when TREE price exceeds 1.05 yUSD
    * TREE minted is proportional to price deviation
    * Of the TREE minted
        * 10% sent to rewards pool for uniswap LP's
        * 10% sold for yUSD and sent to charity DAO
        * 80% sold for yUSD and put into reserve
    * Weights can be changed by governance

* Quadratic burning
    * Burn supply to get the square root of reserve
        * burn 1% of supply to get 0.01% of reserve (.01 * .01)
        * burn 25% of supply to get 6.25% of reserve (.25 * .25)
    * If only 1 holder, they can burn to get 100% of reserve
    * Fixed Price to burn TREE
        * If TREE price < price to burn TREE, can arb by buying on Uniswap and burning


## Directory Structure
```
├── buidler.config.js
├── contracts
│   ├── interfaces
│   │   ├── IAMB.sol
│   │   ├── IOmniBridge.sol
│   │   ├── ITREEOracle.sol
│   │   └── ITREERewards.sol
│   ├── libraries
│   │   └── CloneFactory.sol
│   ├── Timelock.sol
│   ├── TREERebaser.sol
│   ├── TREEReserve.sol
│   ├── TREERewardsFactory.sol
│   ├── TREERewards.sol
│   ├── TREE.sol
│   └── UniswapOracle.sol
├── deploy
│   ├── burn-admin-keys.js
│   ├── Forests.js
│   ├── LPRewards.js
│   ├── Timelock-init.js
│   ├── Timelock.js
│   ├── TREE-init.js
│   ├── TREE.js
│   ├── TREERebaser.js
│   ├── TREEReserve-init.js
│   ├── TREEReserve.js
│   ├── TREERewardsFactory.js
│   ├── UniswapOracle-init.js
│   ├── UniswapOracle.js
│   └── UniswapPair.js
├── deploy-configs
│   ├── forests.json
│   ├── get-config.js
│   ├── mainnet-fork.json
│   ├── mainnet.json
│   └── network.json
├── DEPLOY_README.md
├── README.md
├── scripts
│   ├── setup-test-env.js
│   ├── setup-test-rebase.js
│   └── start-mainnet-fork.sh
└── test
    └── test.js
```


---
## Contracts Reviewed
* TREE.sol
* TREERebaser.sol
* TreeReserve.sol

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
* `_treePrice()`
    * fetch TREE price from the `oracle`
* `setGov(address _newValue)`
    * Set `gov` to a new address
* `setOracle(address _newValue)`
    * Set `oracle` to a new address
* `setMinimumRebaseInterval(uint256 _newValue)`
    * Set `minimumRebaseInterval` to a new value
* `setDeviationThreshold(uint256 _newValue)`
    * Set `deviationThreshold` to a new value
* `setRebaseMultiplier(uint256 _newValue)`
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

# Areas of Concern

## Governance
1. `setGov()`
2. No minimum time locks on governance

## rebaseMultiplier (TREERebaser.sol)
* The `rebaseMultiplier` variable can range between 0.05x and 10x.  This is a range of 2000x (0.05 * 2000 = 10) and is unnecessarily large.  Large changes in `rebaseMultiplier` may have unintended consequences on TREE price and supply. (TODO: be more precise about 'unintended consequences')

Let's play out a scenario where TREE price increased 8% in 12 hours to 1.08 yUSD and `rebaseMultiplier` is 5x.

Let's say TREE rebases back to $1.00 with a total supply of 1,000 TREE.  12 hours later, TREE price has increased 8% to $1.08, which is not unheard of in crypto. The price peg to rebalance is $1.05.  `charityCut` and `rewardsCut` are set to the middle value in their range.  `rebaseMultiplier` is set to 5x

Let's also assume selling 8% of total supply will lower price 8%. In reality this will be much lower and depends on the quantity of TREE locked in the LP.

Finally, assume the quantity of reserveTokenReceived is the same quantity of TREE sold.  This number will also be lower in reality due to fees/slippage.

```Javascript

PRECISION = 10**18
treePrice = 1.08 * 10**18
treeSupply = 1000 * 10**18

charityCut = 2.5 * 10**17 // 25%
rewardsCut = 5 * 10**18   // 5%
rebaseMultiplier = 5 * 10**18  // 5x


// TREERebaser.sol lines 136-147

uint256 indexDelta = treePrice.sub(PRECISION).mul(rebaseMultiplier).div(PRECISION);  // 4 * 10**17 or 40%

// calculate the change in total supply
uint256 treeSupply = tree.totalSupply();  // in this case, 1000 * 10**18
uint256 supplyChangeAmount = treeSupply.mul(indexDelta).div(PRECISION);    // 4 * 10**20 or 400 TREE

// rebase TREE
// mint TREE proportional to deviation
// (1) mint TREE to reserve
tree.rebaserMint(address(reserve), supplyChangeAmount);  // Mint 400 TREE to the reserve
// (2) let reserve perform actions with the minted TREE
reserve.handlePositiveRebase(supplyChangeAmount);


// TREEReserve.sol lines 148-174

function handlePositiveRebase(uint256 mintedTREEAmount)
  external
  onlyRebaser
  nonReentrant
{
  // send TREE to TREERewards
  uint256 rewardsCutAmount = mintedTREEAmount.mul(rewardsCut).div(PRECISION);  // 2 * 10**17 or 20 TREE
  tree.transfer(address(lpRewards), rewardsCutAmount);
  lpRewards.notifyRewardAmount(rewardsCutAmount);
  
  // sell remaining TREE for reserveToken
  uint256 remainingTREEAmount = mintedTREEAmount.sub(rewardsCutAmount);  // 3.8 * 10**20 or 380 TREE
  (uint256 treeSold, uint256 reserveTokenReceived) = _sellTREE(  // treeSold = 8 * 10**19 or 80 TREE, reserveTokenReceived = 8 * 10**19 or 80 yUSD
      remainingTREEAmount  // 3 * 10**20 or 300 TREE
  );
  
  // burn unsold TREE
  if (treeSold < remainingTREEAmount) {
      tree.reserveBurn(address(this), remainingTREEAmount.sub(treeSold));  // 300 TREE burned
  }
  
  // send reserveToken to charity
  uint256 charityCutAmount = reserveTokenReceived.mul(charityCut).div(PRECISION.sub(rewardsCut));  // 2.1 * 10**19 or 21 yUSD
  reserveToken.safeIncreaseAllowance(address(omniBridge), charityCutAmount);
  omniBridge.relayTokens(address(reserveToken), charity, charityCutAmount);

```

As you can tell, even with making impossibly-optimistic `treeSold` and `reserveTokenReceived` assumptions, LP providers receive about the same reward as charity.  The imbalance will weight heavily towards LP providers in reality.

The misleading metrics here are `charityCut` and `rewardsCut`.  With `rewardsCut` set to 5% and `charityCut` set to 25%, you'd expect `rewardsCut` to be roughly 1/5 of `charityCut`.  

__Suggestion:__ calculate `charityCut` and `rewardsCut` at the same time. 


### Quadratic burning
Where quadratic voting favors the smaller vote, quadratic burning favors the larger burn.

Quadratic Voting:

| # of votes | Cost |
|--|--|
| 1 | 1  |
| 2 | 4  |
| 5 | 25 |
| 10| 100|


Quadratic Burning:
| % of Supply burned |  % of reserves received |
|---|---|
| 0.01 | 0.0001 |
| 0.02 | 0.0004 |
| 0.05 | 0.0025 |
| 0.10 | 0.01


In both scenarios, each time you increase the quantity by 10x the end result increases by 100x.  The primary difference here is that quadratic voting adds cost to the user, where quadratic burning adds benefits to the user.

Ultimately, my concern is that a flash loan could burn a high percentage of supply as each 10x change in supply burned returns 100x of the reserve.  Repeated flash loans may have the potential to drain the reserves at a rate higher than expected. 



## Additional Feedback
### Documentation
Documentation between contracts is inconsistent and some primary functions are missing comments altogether.  [NatSpec](https://solidity.readthedocs.io/en/latest/natspec-format.html#natspec) is the recommended documentation style and should be used throughout the project.

For example, TREEReserve.burnTREE() will be widely used but has no supporting documentation. 

## Testing
Tests were performed on a Linux OS and Mac OS, and failed on both.  In both instance the same error occured for each test:

```
  0 passing (50s)
  4 failing


  1) TREE
       "before each" hook for "should not have owner":
     ERROR processing /home/carl/Documents/tree-contracts/deploy/UniswapPair.js:
Error: VM Exception while processing transaction: revert UniswapV2: FORBIDDEN


  2) Farming
       "before each" hook for "should give correct reward to regular pool":
     ERROR processing /home/carl/Documents/tree-contracts/deploy/UniswapPair.js:
Error: VM Exception while processing transaction: revert UniswapV2: FORBIDDEN


  3) Rebasing
       "before each" hook for "should not rebase when price delta is below threshold":
     ERROR processing /home/carl/Documents/tree-contracts/deploy/UniswapPair.js:
Error: VM Exception while processing transaction: revert UniswapV2: FORBIDDEN


  4) Reserve
       "before each" hook for "should sell TREE during rebase":
     ERROR processing /home/carl/Documents/tree-contracts/deploy/UniswapPair.js:
Error: VM Exception while processing transaction: revert UniswapV2: FORBIDDEN

```



## Disclaimer
This audit was performed at no cost to WhalerDAO.  This report is not investment advice and in no way proof of a perfect smart contract.  This audit was done to the best of Carl Farterson's ability and focused on several of the primary contracts.  