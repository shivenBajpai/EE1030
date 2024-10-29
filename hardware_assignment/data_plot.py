import numpy as np
import matplotlib.pyplot as plt

A = np.loadtxt('data.csv', dtype=np.double)
plt.plot(A[:,[0]], A[:,[1]], 'k.')
plt.ylabel('Output Voltage (V)')
plt.xlabel('Temperature ($^{\\circ}$C)')
plt.title("Readings of Voltage across PT-100")
plt.show()