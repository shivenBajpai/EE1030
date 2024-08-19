#Code by Shiven Bajpai
#August 19, 2024
#Based on code from https://github.com/gadepall/matgeo
#released under GNU GPL
#Section Formula

import sys                                          #for path to external scripts
sys.path.insert(0, '/mnt/Data/Classwork/my_codes/CoordGeo')        #path to my scripts
import numpy as np
import matplotlib.pyplot as plt

#local imports
from line.funcs import *

#if using termux
import subprocess
import shlex
#end if

#Given points
A = np.array(([-1,3])).reshape(-1,1)
B = np.array(([2,5])).reshape(-1,1)

#Ratio
n=4/3

#Point
P= (B+n*A)/(1+n) # calculating the coordinate points of P which divides the join between the two points

#Generating all lines
x_AB = line_gen(A,B)

#Plotting all lines
plt.plot(x_AB[0,:],x_AB[1,:],label='$AB$')

#Labeling the coordinates
tri_coords = np.block([[P,A,B]])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['P','A','B']

for i, txt in enumerate(vert_labels):
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.2f}, {tri_coords[1,i]:.2f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(20,-20), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

ax = plt.gca()
ax.plot()
plt.legend(loc='best')
plt.grid() 
plt.axis([-2,6,-2,6])

#if using termux
#plt.savefig('chapters/10/7/2/1/figs/fig.pdf')
#subprocess.run(shlex.split("termux-open chapters/10/7/2/1/figs/fig.pdf"))
#else
plt.savefig('Figures/Figure.png')
plt.show()
