import matplotlib.pyplot as plt
import numpy as np


rng = np.linspace(0, 1, 999, endpoint=False)
rng2 = [x*x for x in rng]


plt.plot(rng, rng2)
plt.show()