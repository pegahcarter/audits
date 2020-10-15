# Notes

## 2020.01.15
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
