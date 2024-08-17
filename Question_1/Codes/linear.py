import sys                                          #for path to external scripts
import math
sys.path.insert(0, '/mnt/Data/Classwork/matgeo/codes/CoordGeo')        #path to scripts (from gadepall/matgeo)
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt

#local imports
from line.funcs import *

#if using termux
#import subprocess
#import shlex
#end if

#Direction vector
m_1 = np.array(([2/3, -1])).reshape(-1,1) 
m_2 = np.array(([1, 0])).reshape(-1,1) 
m_3 = np.array(([0, -1])).reshape(-1,1)
m_4 = np.array([1/2, math.sqrt(3)/2]).reshape(-1,1)
c = 4

#Given points
A = np.array(([3, -2])).reshape(-1,1) 
B1 = np.array(([-1, 4])).reshape(-1,1) 
B2 = np.array(([7, -2])).reshape(-1,1) 
B3 = np.array(([3, 4])).reshape(-1,1) 

k1 = -8
k2 = 8
#Generating Lines
x_AB1 = line_dir_pt(m_1,A,k1,k2)
x_AB2 = line_dir_pt(m_2,A,k1,k2)
x_AB3 = line_dir_pt(m_3,A,k1,k2)
x_AQ = line_dir_pt(m_4,A,k1,k2)

#Plotting all lines
plt.plot(x_AB1[0,:],x_AB1[1,:],label='Subpart 1)',c="blue")
plt.plot(x_AB2[0,:],x_AB2[1,:],label='Subpart 2)',c="g")
plt.plot(x_AB3[0,:],x_AB3[1,:],label='Subpart 3)',c="r")
plt.plot(x_AQ[0,:],x_AQ[1,:],label='Subpart 4)',c="black")

colors = ['black','blue','green','r']
#Labeling the coordinates
tri_coords = np.block([A,B1,B2,B3])
plt.scatter(tri_coords[0,:], tri_coords[1,:], c=colors)
vert_labels = ['A','B_1','B_2','B_3']
for i, txt in enumerate(vert_labels):
    plt.annotate(txt, # this is the text
    #plt.annotate(f'{txt}\n({tri_coords[0,i]:.2f}, {tri_coords[1,i]:.2f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(-10,-10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

# use set_position
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
'''
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend(loc='best')
'''
plt.grid() # minor
plt.legend(loc='best')
plt.axis('equal')

#if using termux
#plt.savefig('chapters/10/7/4/1/figs/fig.pdf')
#subprocess.run(shlex.split("termux-open chapters/10/7/4/1/figs/fig.pdf"))
#else
plt.show()
