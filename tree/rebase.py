import matplotlib.pyplot as plt


PRECISION = 10**18

MIN_REBASE_MULTIPLIER = 5 * 10**16  # 0.05x
MAX_REBASE_MULTIPLIER = 10**19      # 10x
MIN_DEVIATION_THRESHOLD = 10**16    # 1%

# Let's assume a price of $1.05/TREE and a supply of 1,000
treePrice = 1.05 * PRECISION
treeSupply = 1000 * PRECISION

