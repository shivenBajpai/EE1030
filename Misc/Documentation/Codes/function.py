import matplotlib.pyplot as plt
import numpy as np
from common import *

plt.figure(figsize = (8,8))

# Define the function
g1 = g_gen(3.41421, 1.41421)
g2 = g_gen(1.41421, 3.41421)

k1 = -5
k2 = 5
xG1 = func_gen(g1, k1, k2)
xG2 = func_gen(g2, k1, k2)

# Plotting functions
plt.plot(xG1[:,0], xG1[:,1], 'r', label="g(x) for x4")
plt.plot(xG1[:,0], xG2[:,1], 'g', label="g(x) for x2")

# Configuring Plot
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.set_xlim([-5, 5])
ax.set_ylim([-0.5, 1.5])
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend(loc='best')
plt.grid()
plt.xticks(np.arange(-5, 6, 1.0))
plt.yticks(np.arange(-5, 6, 1.0))
plt.savefig("../Figures/function.png", transparent=True, bbox_inches='tight', pad_inches=0)

plt.show()  