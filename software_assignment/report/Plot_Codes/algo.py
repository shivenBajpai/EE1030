import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

avgs = lambda arrays: [sum(x)/len(x) for x in arrays]

# GS
A = np.array([6.0000e-04, 2.4000e-03, 1.6600e-02, 8.8000e-03, 7.6200e-02, 3.5200e-02, 4.1000e-02, 1.0000e-01, 1.0920e-01, 2.6240e-01, 2.2900e-01, 4.0060e-01, 3.4900e-01, 5.2800e-01, 5.3240e-01, 7.0200e-01, 8.5080e-01, 1.2348e+00, 1.6310e+00, 1.6512e+00, 2.2278e+00, 2.1796e+00, 3.1142e+00, 3.3100e+00,])

# HH
B = np.array([8.0000e-04, 3.0000e-03, 1.8600e-02, 1.1200e-02, 8.8800e-02, 4.8400e-02, 5.6600e-02, 1.6000e-01, 1.7020e-01, 3.6600e-01, 3.6940e-01, 5.8720e-01, 5.4320e-01, 8.4000e-01, 9.3020e-01, 1.2950e+00, 1.5758e+00, 2.1942e+00, 2.9040e+00, 2.9048e+00, 4.0114e+00, 3.9628e+00, 5.8298e+00, 5.9960e+00,])

classes = [ 'Gram-Schmidt', 'Householder']

# Create the bar graph
plt.figure(figsize=(10, 5))
# bars = plt.barh(classes, averages)#, color='skyblue', edgecolor='black')
plt.plot(np.arange(1,25), A, label=classes[0])
plt.plot(np.arange(1,25), B, label=classes[1])
# plt.plot(np.arange(1,25), C, label=classes[2])
# plt.plot(np.arange(1,25), D, label=classes[3])
# plt.plot(np.arange(1,25), E, label=classes[4])
# plt.plot(np.arange(1,25), F, label=classes[5])
# plt.plot(np.arange(1,25), G, label=classes[6])
# plt.plot(np.arange(1,25), H, label=classes[7])

# Add labels, title, and grid
plt.ylabel('Time taken(s)')
plt.xlabel('Matrix size')
plt.title('Time taken by different algorithms for finding eigenvalues')
plt.xlim(0, 25)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 5:.0f}'))

# Annotate the bars with the average values
# for bar, avg in zip(bars, averages):
#     plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2, 
#              f'{round(avg, 3)}', va='center', fontsize=10)

# Add the configuration text at the bottom
config_text = "Test configuration: Finding Eigenvalues of nxn Matrix, averaged over 5 different cases"
plt.figtext(0.5, 0.005, config_text, wrap=True, horizontalalignment='center', fontsize=10, color='black')

# Show the plot
plt.tight_layout()
plt.savefig("../Figures/algo.png")
plt.show()