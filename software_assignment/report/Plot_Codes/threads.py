import numpy as np
import matplotlib.pyplot as plt

avgs = lambda arrays: [sum(x)/len(x) for x in arrays]

# 1t
A = np.array([0.137,0.160,0.149,0.142,0.146,0.187,0.148,0.239,0.135,0.162,0.160,0.170,0.153,0.150,0.194,0.167,0.144,0.184,0.148,0.166,0.167,0.147,0.216,0.142,])

# 4t
B = np.array([0.156,0.159,0.208,0.183,0.166,0.204,0.165,0.266,0.160,0.235,0.161,0.213,0.161,0.152,0.202,0.160,0.177,0.414,0.558,0.195,0.207,0.327,0.264,0.152,])

# 6t
C = np.array([0.145,0.153,0.222,0.198,0.193,0.214,0.184,0.283,0.164,0.264,0.172,0.239,0.161,0.157,0.225,0.167,0.175,0.212,0.266,0.184,0.219,0.433,0.292,0.172,])

# 8t
D = np.array([0.155,0.163,0.265,0.222,0.201,0.237,0.208,0.308,0.201,0.301,0.205,0.273,0.190,0.161,0.226,0.170,0.199,0.361,0.321,0.192,0.246,0.534,0.333,0.178,])

# 10t
E = np.array([0.168,0.174,0.306,0.259,0.235,0.267,0.219,0.341,0.215,0.377,0.196,0.319,0.201,0.184,0.267,0.191,0.218,0.254,0.364,0.225,0.272,0.613,0.364,0.197,])

# 12t
F = np.array([0.188,0.182,0.351,0.295,0.257,0.289,0.262,0.397,0.233,0.390,0.185,0.325,0.201,0.201,0.277,0.207,0.227,0.276,0.392,0.215,0.280,0.626,0.367,0.196,])

# 14t
G = np.array([0.212,0.195,0.349,0.286,0.284,0.299,0.293,0.399,0.254,0.445,0.216,0.377,0.245,0.211,0.317,0.222,0.257,0.292,0.414,0.241,0.322,0.745,0.438,0.233,])

# 18t
H = np.array([0.273,0.260,0.513,0.418,0.377,0.429,0.406,0.567,0.335,0.580,0.296,0.501,0.328,0.283,0.406,0.300,0.341,0.393,0.570,0.322,0.408,1.008,0.569,0.301,])

A = A/A
B = A/B
C = A/C
D = A/D
E = A/E
F = A/F
G = A/G
H = A/H

classes = [ '1 Thread (Baseline)', '4 Threads', '6 Threads', '8 Threads', '10 Threads', '12 Threads', '14 Threads', '18 Threads']

# Create the bar graph
plt.figure(figsize=(10, 5))
# bars = plt.barh(classes, averages)#, color='skyblue', edgecolor='black')
plt.plot(np.arange(1,25), A, label=classes[0])
plt.plot(np.arange(1,25), B, label=classes[1])
plt.plot(np.arange(1,25), C, label=classes[2])
# plt.plot(np.arange(1,25), D, label=classes[3])
plt.plot(np.arange(1,25), E, label=classes[4])
# plt.plot(np.arange(1,25), F, label=classes[5])
plt.plot(np.arange(1,25), G, label=classes[6])
plt.plot(np.arange(1,25), H, label=classes[7])

# Add labels, title, and grid
plt.ylabel('Speedup vs.\nBaseline')
plt.xlabel('Matrix size')
plt.title('Speedup vs Single Thread For different threads counts')
plt.xlim(0, 25)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate the bars with the average values
# for bar, avg in zip(bars, averages):
#     plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2, 
#              f'{round(avg, 3)}', va='center', fontsize=10)

# Add the configuration text at the bottom
config_text = "Test configuration: 5 Repetitions of Finding Eigenvalues of nxn Matrix"
plt.figtext(0.5, 0.005, config_text, wrap=True, horizontalalignment='center', fontsize=10, color='black')

# Show the plot
plt.tight_layout()
plt.savefig("../Figures/threads.png")
plt.show()