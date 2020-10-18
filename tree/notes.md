# Notes

## 2020.10.15
### README summary
* DAOs/pools
    * TREE-yUSD uniswap pool
    * charity DAO
    * reserve (holds yUSD from rebases)
* Rebases
    * Only happens when TREE exceed 1.05 yUSD
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
    * Fixed (?) Price to burn TREE
        * If TREE price < price to burn TREE, can arb by buying on Uniswap and burning

### Initial questions
* Can initial holder of TREE burn claim all reserve?
* At quadratic rate, max of 10% can be burned from reserve (Square root of 100% = 10%)
* What is price to burn TREE?
* At rebase, 90% TREE minted is sold for yUSD.  Can this be gamed?
    * What if there's insufficient liquidity?
* Governance to change rebases
    * What if more % sent to rewards pool?  There would be less TREE sold > less effect on price

## 2020.10.16
### Timelock.sol
[Copied from Compound](https://github.com/compound-finance/compound-protocol/blob/master/contracts/Timelock.sol) with several changes.  Also discrepancy in require statements, some are multi-line while some are same-line.

## 2010.10.17
### TREEReserve.sol
* Some functions have a @notice and @param while some do not.  Please standardize.


### TREEReserve.sol & TREERebaser.sol
* Create TREE setGov function.  Otherwise, gov may be set different for TREEReserve and TREERebaser.  Also, gov change emits could be at different timestamps 

Example:
```Solidity
# TREE.sol

modifier onlyGov {
    require(msg.sender == gov, "TREE: not gov");
    _;
}

event SetGov(address _newValue);

function setGov(address _newValue) external onlyGov {
    require(_newValue != gov, "TREE: Address already set")
    require(_newValue != address(0), "TREE: address is 0");
    rebaser.setGov(_newValue);
    reserve.setGov(_newValue);
    emit SetGov(_newValue);
}

# TREERebaser.sol
modifier onlyTree {
    require(msg.sender == tree, "TREERebaser: not tree);
    _;
}

function setGov(address _newValue) external onlyTree {
    gov = _newValue;
}

```