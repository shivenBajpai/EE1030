import ctypes
import matplotlib.pyplot as plt
import numpy as np

lib = ctypes.CDLL('./main.so')

# Function to generate line points
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


#Labeling the coordinates
tri_coords = np.block([[A,B,C]])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['A','B','C']
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
plt.axis([-0.5, 7, -0.5, 7])
plt.show()

# Free memory
lib.free(v_ptr)
