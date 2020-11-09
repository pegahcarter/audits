# DeFI777
## Carl Farterson


## Scope


[](https://github.com/carlfarterson/defi777)

This audit covers [DeFi77](https://defi777.com), a website where you can wrap ERC-20 tokens into ERC-777 tokens.

Commit [`38542e7`](https://github.com/carlfarterson/defi777)


## Description

ERC-777 tokens generally offer more functionality than ERC-20 tokens.




## -------------------------------------------





## Notes


## 2020.10.15

## Resources
* [ERC-20 vs ERC-777 tokens explained](https://hackernoon.com/erc777-is-the-new-token-standard-replacing-the-erc20-fd6319c3b13)
* [Summary](https://docs.google.com/document/d/1mbkmh_4j9ywmFTH0pr34fmpp9rlvPbjsvEfj0MbIyv8/edit)
* ERC-777
  * [EIP](https://eips.ethereum.org/EIPS/eip-777)
  * [OpenZeppelin Docs](https://docs.openzeppelin.com/contracts/3.x/erc777)
  * https://www.wealdtech.com/articles/understanding-erc777-token-contracts/
  * https://www.wealdtech.com/articles/understanding-erc777-token-operator-contracts/




## 2020.11.08
[`ERC777WithGranularity.sol`](https://github.com/) Contains [`_mint()`](https://github.com/) and [`_burn()`](https://github.com/) definitions

- It would help if _`mint()` / `_burn()` were defined in this [`Wrapped777.sol`]().

- Can `flashMint()` be manipulated?

## Slither Analysis
First, some live DeFi777 contract addresses:
* [uniswap777 .eth](https://etherscan.io/address/uniswap777.eth)
* []()
* []()