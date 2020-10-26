import matplotlib.pyplot as plt
import numpy as np


PRECISION = 10**18

MIN_REBASE_MULTIPLIER = 5 * 10**16  # 0.05x
MAX_REBASE_MULTIPLIER = 10**19      # 10x
MIN_DEVIATION_THRESHOLD = 10**16    # 1%


# Let's assume a price of $1.05/TREE, supply of 1,000 TREE, and a deviationThreshold set at the minimum
treePrice = 1.05 * PRECISION
treeSupply = 1000 * PRECISION
deviationThreshold = MIN_DEVIATION_THRESHOLD

# Create a range of rebase multipliers
rebaseMultiplierRng = np.linspace(MIN_REBASE_MULTIPLIER, MAX_REBASE_MULTIPLIER, 200)

# Initialize a list of supply change by rebases
supplyChangeLst = []

# Calculations
for rebaseMultiplier in rebaseMultiplierRng:
    indexDelta = (treePrice - PRECISION) * rebaseMultiplier / PRECISION # TREERebaser.sol # TODO: insert line
    supplyChangeAmount = treeSupply * indexDelta / PRECISION # TREEREbaser.sol # TODO: insert line

    supplyChangeLst.append(supplyChangeAmount)


plt.plot(supplyChangeLst)
plt.show()
