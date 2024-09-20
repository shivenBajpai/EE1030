import ctypes
import numpy as np
import matplotlib.pyplot as plt
import sys

# Load the shared C library 
lib = ctypes.CDLL('./alt.so')

# Define the argument and return types for the C function
lib.calculateVertices.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
lib.freeMat.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.calculateVertices.restype = ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))

# Call the C function
a, b, c = 5.0, 6.0, 7.0  # Example values for the sides of the triangle
vertices_ptr = lib.calculateVertices(a, b, c)

if not vertices_ptr: sys.exit(1)

A = np.array([vertices_ptr[0][0][0], vertices_ptr[0][1][0]]).reshape(-1, 1);
B1 = np.array([vertices_ptr[1][0][0], vertices_ptr[1][1][0]]).reshape(-1, 1);
B2 = np.array([vertices_ptr[2][0][0], vertices_ptr[2][1][0]]).reshape(-1, 1);
C = np.array([vertices_ptr[3][0][0], vertices_ptr[3][1][0]]).reshape(-1, 1);

# Plotting
plt.figure()

# Plot points A, B1, B2, and C
plt.scatter([A[0], B1[0], B2[0], C[0]], [A[1], B1[1], B2[1], C[1]], color='k')
plt.text(A[0]-0.5, A[1], 'A', fontsize=12, ha='right')
plt.text(B1[0]-0.5, B1[1], 'B1', fontsize=12, ha='right')
plt.text(B2[0]+1, B2[1]-1, 'B2', fontsize=12, ha='right')
plt.text(C[0]-0.5, C[1]+0.5, 'C', fontsize=12, ha='right')

# Draw lines for triangle A B1 C
plt.plot([A[0], B1[0]], [A[1], B1[1]], color='brown')
plt.plot([B1[0], C[0]], [B1[1], C[1]], color='orange')
plt.plot([A[0], C[0]], [A[1], C[1]], color='red')

# Draw lines for triangle A B2 C
plt.plot([A[0], B2[0]], [A[1], B2[1]], color='brown')
plt.plot([B2[0], C[0]], [B2[1], C[1]], color='orange')
plt.plot([A[0], C[0]], [A[1], C[1]], color='red')

# Plot circles around A and C
circle_A = plt.Circle((A[0], A[1]), c, color='blue', fill=False) 
circle_C = plt.Circle((C[0], C[1]), a, color='green', fill=False) 

plt.gca().add_patch(circle_A)
plt.gca().add_patch(circle_C)

# Setting the axis limits and labels
plt.xlim(-c-1, C[0]+a+1)
plt.ylim(-max(c, a)-1, max(c, a)+1)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X')
plt.ylabel('Y')

# Display the plot
plt.grid(True)
plt.show()

#Free the memory later
lib.freeMat(vertices_ptr[0], 2)
lib.freeMat(vertices_ptr[1], 2)
lib.freeMat(vertices_ptr[2], 2)
lib.freeMat(vertices_ptr[3], 2)
lib.free(vertices_ptr)
