#Program to plot an ellipse 
#Code by GVV Sharma
#August 8, 2020
#Revised August 16, 2024

import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

# import sys                                          #for path to external scripts
# sys.path.insert(0, '/sdcard/github/matgeo/codes/CoordGeo')        #path to my scripts

#local imports
from CoordGeo.line.funcs import *
from CoordGeo.triangle.funcs import *
from CoordGeo.conics.funcs import *

#if using termux
# import subprocess
# import shlex
#end if

#setting up plot
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, aspect='equal')
length = 100
y = np.linspace(-2,2,length)

#hyperbola parameters, first eigenvalue should be negative
V = np.array(([-1/2,0],[0,1/2]))
u = np.array(([0,0])).reshape(-1,1)
f = 1
n,c,F,O,lam,P,e = conic_param(V,u,f)
#print(lam,P)
ab = ellipse_param(V,u,f)
#Generating the Standard Hyperbola
x = hyper_gen(y)
ParamMatrix = np.diag(ab)

#Affine conic generation
# Of = O.flatten()
Of = np.array([1,1])

cl = (n.T@F).flatten()

P = rotmat(-np.pi/4)@ref
F = P@F + Of

#Directrix
k1 = -5
k2 = 5

#Latus rectum

# print(c)


#Generating lines
x_A = P@line_norm(n,c[0],k1,k2)+Of[:,np.newaxis]#directrix
x_B = P@line_norm(n,cl[0],k1,k2)+Of[:,np.newaxis]#latus rectum
x_C = P@line_norm(n,c[1],k1,k2)+Of[:,np.newaxis]#directrix
x_D = P@line_norm(n,cl[1],k1,k2)+Of[:,np.newaxis]#latus rectum

xStandardHyperLeft = np.block([[-x],[y]])
xStandardHyperRight= np.block([[x],[y]])

# Endpoints of parabola
StandardEndpoints = np.array([
    [-np.sqrt(2), 2],
    [np.sqrt(2), 2],
    [-np.sqrt(2), -2],
    [np.sqrt(2), -2]
]).T
ActualEndpoints = rotmat(-np.pi/4)@StandardEndpoints+Of[:,np.newaxis]

#Generating the actual hyperbola
xActualHyperLeft = P@ParamMatrix@xStandardHyperLeft+Of[:,np.newaxis]
xActualHyperRight = P@ParamMatrix@xStandardHyperRight+Of[:,np.newaxis]


#plotting
plt.plot(xActualHyperLeft[0,:],xActualHyperLeft[1,:],label='Actual hyperbola',color='r')
plt.plot(xActualHyperRight[0,:],xActualHyperRight[1,:],color='r')
plt.plot(x_A[0,:],x_A[1,:], 'b',label='Directrix')
plt.plot(x_B[0,:],x_B[1,:], 'g',label='Latus Rectum')
plt.plot(x_C[0,:],x_C[1,:], 'b')
plt.plot(x_D[0,:],x_D[1,:], 'g')
#
#Labeling the coordinates
tri_coords = np.block([O,F,ActualEndpoints])
vert_labels = ['$\\mathbf{O}$','$\\mathbf{F}_1$','$\\mathbf{F}_2$','$\\mathbf{X}_2$','$\\mathbf{X}_4$','$\\mathbf{X}_1$','$\\mathbf{X}_3$']
offset_type = [0,0,1,0,0,1,1]
offsets = [(25,5), (-25,-25)]
colors = np.arange(1,len(vert_labels)+1)
plt.scatter(tri_coords[0,:], tri_coords[1,:], c='k')
for i, txt in enumerate(vert_labels):
#    plt.annotate(txt, # this is the text
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.2f}, {tri_coords[1,i]:.2f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=offsets[offset_type[i]], # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

# use set_position
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.set_xlim([-4, 6])
ax.set_ylim([-4, 6])
'''
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
'''
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend(loc='best')
plt.grid() # minor
plt.xticks(np.arange(-10, 11, 1.0))
plt.yticks(np.arange(-10, 11, 1.0))
plt.axis('equal')

#if using termux
# plt.savefig('.fig-temp.pdf')
# subprocess.run(shlex.split("termux-open ./fig-temp.pdf"))
#else
plt.show()