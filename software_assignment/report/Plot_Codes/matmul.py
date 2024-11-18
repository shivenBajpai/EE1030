import numpy as np
import matplotlib.pyplot as plt

avgs = lambda arrays: [sum(x)/len(x) for x in arrays]

A = [0.795, .8, .793, .789, .804] 
B = [0.236, 0.235, 0.231, 0.233, 0.242]
C = [.191, .191, .198, .192, .194] 
D = [.146, .151, .150, .144, .145] 
E = [.132, .131, .135, .142, .139] 

classes = ['No Parallelism', 'Parallelized (without \n Handling Cache Conflicts)', 'Parallelized (Base)', 'Parallelized (Base+\nDynamic Scheduling)', 'Parallelized ((Base+\n Dynamic Scheduling\n + Optimal Thread count))']
averages = avgs([A,B,C,D,E])

# Create the bar graph
plt.figure(figsize=(10, 5))
bars = plt.barh(classes, averages)#, color='skyblue', edgecolor='black')

# Add labels, title, and grid
plt.ylabel('Parallelization \nStrategy')
plt.xlabel('Average Time (5 runs)')
plt.title('Matrix Multiplication: Time Taken vs Parallelization Strategy')
plt.xlim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate the bars with the average values
for bar, avg in zip(bars, averages):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2, 
             f'{round(avg, 3)}', va='center', fontsize=10)

# Add the configuration text at the bottom
config_text = "Test configuration: Multiply 2 100x100 Complex Matrices, 1000 repetitions"
plt.figtext(0.5, 0.005, config_text, wrap=True, horizontalalignment='center', fontsize=10, color='black')

# Show the plot
plt.tight_layout()
plt.subplots_adjust(right=0.8) 
plt.savefig("../Figures/matmul.png")
plt.show()