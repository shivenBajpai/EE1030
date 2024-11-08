import numpy as np
import math
import matplotlib.pyplot as plt

plt.figure(figsize = (8,8))

# Define the function
f1 = lambda x: math.e**(1.41421*x) if x<0 else math.e**(-3.41421*x)
vf1 = np.vectorize(f1)

f2 = lambda x: math.e**(3.41421*x) if x<0 else math.e**(-1.41421*x)
vf2 = np.vectorize(f2)

# Plot curve
x = np.linspace(-5,5,101) # Odd amount to ensure there is a sample point at x=0
y1 = vf1(x)
y2 = vf2(x)

plt.plot(x, y1, 'r', label="g(x) for x4")
plt.plot(x, y2, 'g', label="g(x) for x2")

# For saving as png
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