import numpy as np
import matplotlib.pyplot as plt

avgs = lambda arrays: [sum(x)/len(x) for x in arrays]

A = [3.838, 3.829, 3.830, 3.822] # Deflation off
B = [1.111, 1.121, 1.081, 1.101] # Deflate every iteration
C = [1.089, 1.096, 1.098, 1.127] # Deflate every other iteration
D = [1.01, 1.093, 1.118, 1.108] # Deflate every 4 iterations
E = [1.105, 1.086, 1.094, 1.098] # Deflate every 8 iterations

classes = ['Deflation off', 'Deflate every \niteration', 'Deflate every \nother iteration', 'Deflate every \n4 iterations', 'Deflate every \n8 iterations']
averages = avgs([A,B,C,D,E])

# Create the bar graph
plt.figure(figsize=(10, 6))
bars = plt.barh(classes, averages)#, color='skyblue', edgecolor='black')

# Add labels, title, and grid
plt.ylabel('Deflation Frequency')
plt.xlabel('Average Time (5 runs)')
plt.title('Time Taken vs Deflation Frequency')
plt.xlim(0, 4)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate the bars with the average values
for bar, avg in zip(bars, averages):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2, 
             f'{round(avg, 3)}', va='center', fontsize=10)

# Add the configuration text at the bottom
config_text = "Test configuration: 75x75 Complex Matrix, No iteration limit, tolerance 1e-9, Gram-Schmidt"
plt.figtext(0.5, 0.005, config_text, wrap=True, horizontalalignment='center', fontsize=10, color='black')

# Show the plot
plt.tight_layout()
plt.subplots_adjust(right=0.9) 
plt.savefig("../Figures/deflation.png")
plt.show()