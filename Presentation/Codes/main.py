# main.py

import ctypes
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as LA

lib = ctypes.CDLL('./main.so')

omat = np.array([[0, 1], [-1, 0]])

# Utility functions
# Copied from line library from github.com/gadepall/matgeo
def line_gen(A,B):
  len =10
  dim = A.shape[0]
  x_AB = np.zeros((dim,len))
  lam_1 = np.linspace(0,1,len)
  for i in range(len):
    temp1 = A + lam_1[i]*(B-A)
    x_AB[:,i]= temp1.T
  return x_AB 

def circ_gen(O,r):
	len = 50
	theta = np.linspace(0,2*np.pi,len)
	x_circ = np.zeros((2,len))
	x_circ[0,:] = r*np.cos(theta)
	x_circ[1,:] = r*np.sin(theta)
	x_circ = (x_circ + O)
	return x_circ

def line_intersect(n1,A1,n2,A2):
  N=np.block([n1,n2]).T
  p = np.zeros((2,1))
  p[0] = n1.T@A1
  p[1] = n2.T@A2
  P=LA.solve(N,p)
  return P

# Define the Vector struct in Python
class Vector(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double)]

# Specify the return type of the get_data function
lib.calculateVertices.restype = ctypes.POINTER(Vector)
lib.calculateVertices.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]

# Call the C function
a = 5
b = 6
c = 7
v_ptr = lib.calculateVertices(a, b, c)

# Extract information from returned values
A = np.array([v_ptr[0].x, v_ptr[0].y]).reshape(-1,1)
B = np.array([v_ptr[1].x, v_ptr[1].y]).reshape(-1,1)
C = np.array([v_ptr[2].x, v_ptr[2].y]).reshape(-1,1)

# Generate and plot lines
x_AB = line_gen(A,B);
x_BC = line_gen(B,C);
x_CA = line_gen(C,A);
plt.plot(x_AB[0,:],x_AB[1,:],label='$AB$')
plt.plot(x_BC[0,:],x_BC[1,:],label='$BC$')
plt.plot(x_CA[0,:],x_CA[1,:],label='$CA$')

# Circumcircle
O = line_intersect(A-B,(A+B)/2,A-C,(A+C)/2)
r = np.sqrt((A-O).T@(A-O))
ccircle = circ_gen(O, r)
plt.plot(ccircle[0,:], ccircle[1,:], label="Circumcircle")

# Incircle
I = line_intersect(omat@(B-A)/LA.norm(B-A)+omat@(C-A)/LA.norm(C-A),A,omat@(A-B)/LA.norm(A-B) + omat@(C-B)/LA.norm(C-B),B)
r = (omat@(B-C)).T@(I-B)/LA.norm(B-C)
icircle = circ_gen(I, r)
plt.plot(icircle[0,:], icircle[1,:], label="Incircle")

#Labeling the coordinates
tri_coords = np.block([[A,B,C,O,I]])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['A','B','C','O','I']
for i, txt in enumerate(vert_labels):
    plt.annotate(txt, 
                 (tri_coords[0,i], tri_coords[1,i]),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')

# Configure plot
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend(loc='best')
plt.grid() 
plt.axis([-3, 7, -3, 7])
plt.show()

# Free memory
lib.free(v_ptr)
