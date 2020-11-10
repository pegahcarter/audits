# DeFI777
## Carl Farterson


## Scope


[](https://github.com/carlfarterson/defi777)

This audit covers [DeFi77](https://defi777.com), a website where you can wrap ERC-20 tokens into ERC-777 tokens.

Commit [`8b834e`](https://github.com/carlfarterson/defi777)


## Description

ERC-777 tokens generally offer more functionality than ERC-20 tokens.  The TLDR of it is:
* ERC-777 can flash mint / burn


## Resources
* [ERC-20 vs ERC-777 tokens explained](https://hackernoon.com/erc777-is-the-new-token-standard-replacing-the-erc20-fd6319c3b13)
* [Summary](https://docs.google.com/document/d/1mbkmh_4j9ywmFTH0pr34fmpp9rlvPbjsvEfj0MbIyv8/edit)
* ERC-777
  * [EIP](https://eips.ethereum.org/EIPS/eip-777)
  * [OpenZeppelin Docs](https://docs.openzeppelin.com/contracts/3.x/erc777)
  * https://www.wealdtech.com/articles/understanding-erc777-token-contracts/
  * https://www.wealdtech.com/articles/understanding-erc777-token-operator-contracts/


---

## Repository structure

```
├── contracts
│   ├── farming
│   │   ├── FarmerTokenFactory.sol
│   │   ├── FarmerToken.sol
│   │   ├── IFarmerTokenFactory.sol
│   │   ├── IFarmerToken.sol
│   │   ├── IYieldAdapterFactory.sol
│   │   ├── YieldAdapterFactory.sol
│   │   └── YieldAdapter.sol
│   ├── GuardedReceiver.sol
│   ├── InfiniteApprove.sol
│   ├── interfaces
│   │   └── IWETH.sol
│   ├── Migrations.sol
│   ├── protocols
│   │   ├── aave
│   │   │   ├── Aave777.sol
│   │   │   ├── AToken777.sol
│   │   │   ├── ERC777WithoutBalance.sol
│   │   │   ├── IAToken.sol
│   │   │   ├── ILendingPoolAddressesProvider.sol
│   │   │   ├── ILendingPoolCore.sol
│   │   │   ├── ILendingPool.sol
│   │   │   ├── test
│   │   │   │   ├── TestAaveLendingPoolAddressProvider.sol
│   │   │   │   ├── TestAaveLendingPoolCore.sol
│   │   │   │   ├── TestAaveLendingPool.sol
│   │   │   │   └── TestAToken.sol
│   │   │   └── WadRayMath.sol
│   │   ├── balancer
│   │   │   ├── BalancerPoolExitFactory.sol
│   │   │   ├── BalancerPoolExit.sol
│   │   │   ├── BalancerPoolFactory.sol
│   │   │   ├── BalancerPool.sol
│   │   │   ├── IBalancerPoolFactory.sol
│   │   │   ├── interfaces
│   │   │   │   ├── BFactory.sol
│   │   │   │   └── BPool.sol
│   │   │   └── test
│   │   │       ├── TestBFactory.sol
│   │   │       └── TestBPool.sol
│   │   ├── curve
│   │   │   ├── CRVFarmerFactory.sol
│   │   │   ├── CRVFarmerToken.sol
│   │   │   ├── CurveAdapter.sol
│   │   │   ├── CurveExitAdapter.sol
│   │   │   ├── ICRVFarmerFactory.sol
│   │   │   ├── interfaces
│   │   │   │   ├── ICurveGague.sol
│   │   │   │   ├── ICurveMinter.sol
│   │   │   │   └── ICurvePool.sol
│   │   │   └── test
│   │   │       ├── TestCurveGague.sol
│   │   │       ├── TestCurveMinter.sol
│   │   │       └── TestCurvePool.sol
│   │   ├── pooltogether
│   │   │   ├── IPoolTogetherPool.sol
│   │   │   ├── PoolTogether777.sol
│   │   │   ├── test
│   │   │   │   ├── TestPoolTogetherPool.sol
│   │   │   │   └── TestPoolToken.sol
│   │   │   └── UniswapPoolTogether777.sol
│   │   ├── synthetix
│   │   │   ├── interfaces
│   │   │   │   ├── ISynthetix.sol
│   │   │   │   └── ISynth.sol
│   │   │   ├── ISynthExchangeFactory.sol
│   │   │   ├── SynthExchangeFactory.sol
│   │   │   ├── SynthExchange.sol
│   │   │   └── test
│   │   │       ├── TestSynthetix.sol
│   │   │       └── TestSynth.sol
│   │   ├── uniswap
│   │   │   ├── interfaces
│   │   │   │   ├── IUniswapV2Factory.sol
│   │   │   │   ├── IUniswapV2Pair.sol
│   │   │   │   └── IUniswapV2Router01.sol
│   │   │   ├── IUniswapAdapterFactory.sol
│   │   │   ├── test
│   │   │   │   ├── TestUniswapFactory.sol
│   │   │   │   ├── TestUniswapPair.sol
│   │   │   │   └── TestUniswapRouter.sol
│   │   │   ├── UniswapAdapterFactory.sol
│   │   │   ├── UniswapAdapter.sol
│   │   │   ├── UniswapPoolAdapterFactory.sol
│   │   │   └── UniswapPoolAdapter.sol
│   │   └── yearn
│   │       ├── interfaces
│   │       │   └── IyVault.sol
│   │       ├── IYVaultAdapterFactory.sol
│   │       ├── test
│   │       │   └── TestYVault.sol
│   │       ├── YVaultAdapterFactory.sol
│   │       └── YVaultAdapter.sol
│   ├── Receiver.sol
│   ├── test
│   │   ├── MaliciousUpgradeToken.sol
│   │   ├── TestDai.sol
│   │   ├── TestERC20.sol
│   │   ├── TestERC2612.sol
│   │   ├── TestFlashLoanRecipient.sol
│   │   ├── TestGranularity.sol
│   │   ├── TestMKR.sol
│   │   ├── TestUSDC.sol
│   │   └── WETH.sol
│   └── tokens
│       ├── AddressBook.sol
│       ├── ERC777WithGranularity.sol
│       ├── Granularity.sol
│       ├── IAddressBook.sol
│       ├── IPermit.sol
│       ├── IWrapped777.sol
│       ├── IWrapperFactory.sol
│       ├── Unwrapper.sol
│       ├── Wrapped777.sol
│       └── WrapperFactory.sol
├── deploy
│   ├── AddressBook.js
│   └── WrapperFactory.js
├── deployments
│   └── kovan
│       ├── AddressBook.json
│       ├── solcInputs
│       │   └── 154b6895e0a4b76c9249b199b14f57cd.json
│       └── WrapperFactory.json
├── hardhat.config.js
├── integration-test
│   ├── balancer-pools.js
│   ├── constants.js
│   ├── integration-test.js
│   └── lib.js
├── migrations
│   ├── 1587828582_wrappers.js
│   ├── 1587828590_uniswap.js
│   └── 1_initial_migration.js
├── package.json
├── README.md
├── test
│   ├── aave.js
│   ├── address-book.js
│   ├── balancer-pools.js
│   ├── curve.js
│   ├── farmer-token.js
│   ├── granularity.js
│   ├── pooltogether.js
│   ├── test-lib.js
│   ├── uniswap.js
│   ├── uniswap-pools.js
│   ├── unwrapper.js
│   ├── wrappers.js
│   └── yearn.js
├── truffle-config.js
└── yarn.lock

```




---

## Tests

`yarn install`

### Hardhat
In order to run the hardhat tests, you'll need to first set .env variables for `INFURA_KEY` and `MNEMONIC`.  I would suggest creating a `sample.env` file like so:
```
INFURA_KEY="{enter key here}"
MNEMONIC=slender language drastic vehicle start bachelor distance shove amount they glide earth width base enjoy
```

`yarn hardhat compile`

`yarn hardhat test`

```
  Contract: Aave
Your project has Truffle migrations, which have to be turned into a fixture to run your tests with Hardhat
    ✓ should deposit and withdraw Dai from Aave using Aave777 (591ms)
    ✓ should deposit and withdraw Dai from Aave using the AToken777 (381ms)
    ✓ should deposit and withdraw ETH from Aave using Aave777 (305ms)
    ✓ should deposit and withdraw ETH from Aave using the AToken777 (319ms)

  Contract: AddressBook
    ✓ should allow looking up addresses using an addressbook (151ms)

  Contract: Balancer Pools
    ✓ should join and exit a balancer pool with ETH (187ms)
    ✓ should join a balancer pool with Dai777 (263ms)
    ✓ should farm tokens when exiting a pool (353ms)

  Contract: Curve pools
    ✓ should join a curve pool (275ms)
    ✓ should use CRV farmer tokens (464ms)

  Contract: Farmer Token
    ✓ should allocate tokens correctly (479ms)
    ✓ should let users withdraw using yield tokens (263ms)
    ✓ should let a farmer token be unwrapped down to 0 (306ms)
    ✓ should let a farmer token be unwrapped with other users (369ms)
    ✓ should handle remainders well (1409ms)

  Contract: Granularity
    ✓ 18 decimals
    ✓ 6 decimals

  Contract: PoolTogether
    ✓ should deposit and withdraw (219ms)

  Contract: Uniswap Pools
    ✓ should join a Uniswap pool with ETH (238ms)
    ✓ should join a Uniswap pool with Dai777 (384ms)

  Contract: Uniswap
    ✓ Should swap ETH for a token (217ms)
    ✓ Should swap a 777 token for ETH (267ms)
    ✓ Should swap a 777 token for another token (290ms)

  Contract: Unwrapper
    ✓ should unwrap an ERC20 token (124ms)
    ✓ should unwrap a token with less than 18 decimals (124ms)

  Contract: Wrapped777
    ✓ Should wrap an ERC20 token and unwrap it (128ms)
    ✓ shold wrap an ERC20 using permit (112ms)
    ✓ Should wrap an Dai and unwrap it (104ms)
    ✓ Should wrap USDC and unwrap it (123ms)
    ✓ Should wrap MKR and other tokens using bytes32 names (75ms)
    ✓ should upgrade old 777 tokens (166ms)
@openzeppelin/test-helpers WARN expectRevert: Assertions may yield false negatives!

Revert reason checks are only known to work on Ganache >=2.2.0, and the current node is HardhatNetwork/2.0.2/ethereumjs-vm/4.2.0.

If your node does support revert reasons, please let us know: https://github.com/OpenZeppelin/openzeppelin-test-helpers/issues/new
    ✓ should not allow fake tokens to execute upgrades (122ms)
    ✓ Should issue flash loans (129ms)
    - Should set allowance with permit()

  Contract: yEarn
    ✓ should join and exit a yEarn vault (299ms)
    ✓ should join and exit an ETH yEarn vault (237ms)


  35 passing (11s)
  1 pending

Done in 13.84s.
```



---

## Contracts








---

## Notes

### 2020.11.08
[`ERC777WithGranularity.sol`](https://github.com/) Contains [`_mint()`](https://github.com/) and [`_burn()`](https://github.com/) definitions

- It would help if _`mint()` / `_burn()` were defined in this [`Wrapped777.sol`]().

- Can `flashMint()` be manipulated?

### Slither Analysis
First, some live DeFi777 contract addresses:
* [uniswap777 .eth](https://etherscan.io/address/uniswap777.eth)
* []()
* []()