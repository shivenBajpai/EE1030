# Code by Shiven Bajpai
# August 19, 2024
# Based on code from https://github.com/gadepall/matgeo
# released under GNU GPL
# Section Formula

import sys                                          # for path to external scripts
sys.path.insert(0, '/mnt/Data/Classwork/my_codes/CoordGeo')        # path to my scripts
import matplotlib.pyplot as plt
import numpy as np
import ctypes

# local imports
from line.funcs import *

# if using termux
import subprocess
import shlex
# end if

clib = ctypes.CDLL('./main.so')
data = np.array([0.0,0.0,0.0,0.0,0.0,0.0], dtype=np.float32)
lhs = ctypes.c_float(0.0)
rhs = ctypes.c_float(0.0)
res = clib.get_data(data.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), ctypes.pointer(lhs), ctypes.pointer(rhs))

# Given points
A = np.array((data[:2])).reshape(-1,1)
B = np.array((data[2:4])).reshape(-1,1)
C = np.array((data[4:6])).reshape(-1,1)

print("Taking point P to be:", A)
print("Taking point Q to be:", B)
print("Taking point R to be:", C)
print("Calculated LHS to be:", lhs.value) 
print("Calculated RHS to be:", rhs.value) 

# Generating all lines
x_AB = line_gen(A,B)
x_CB = line_gen(C,B)

# Plotting all lines
plt.plot(x_AB[0,:],x_AB[1,:])
plt.plot(x_CB[0,:],x_CB[1,:])

# Labeling the coordinates
tri_coords = np.block([[A,B,C]])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['P','Q','R']

for i, txt in enumerate(vert_labels):
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.2f}, {tri_coords[1,i]:.2f})',
                 (tri_coords[0,i], tri_coords[1,i]), #  this is the point to label
                 textcoords="offset points", #  how to position the text
                 xytext=(50,0), #  distance from text to points (x,y)
                 ha='center') #  horizontal alignment can be left, right or center

ax = plt.gca()
ax.plot()
plt.grid() 
plt.axis([-2,8,-2,8])

# if using termux
# plt.savefig('chapters/10/7/2/1/figs/fig.pdf')
# subprocess.run(shlex.split("termux-open chapters/10/7/2/1/figs/fig.pdf"))
# else
plt.savefig('../Figures/Figure.png')
plt.show()