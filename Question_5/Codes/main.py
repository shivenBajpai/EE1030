import numpy as np
import ctypes
import matplotlib.pyplot as plt

lib = ctypes.CDLL('./libvectors.so')

# Define the Vector struct in Python
class Vector(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float),
                ("norm", ctypes.c_float)]


# Specify the return type of the get_vector function
lib.get_vector.restype = ctypes.POINTER(Vector)

# Call the C function
vector_ptr = lib.get_vector();
origin = np.array([0,0,0]);
vector = np.array([vector_ptr[0].x, vector_ptr[0].y, vector_ptr[0].z]);

# Plot the Vector
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(*origin, *vector, length=1, color='r')
ax.set_xlim([0, 2])
ax.set_ylim([0, 2])
ax.set_zlim([0, 2])

# Add text to indicate angles
ax.text(vector[0], vector[1], vector[2], 
        f"x\nθ_x: 60°, θ_y: 45°, θ_z: 45°",
        color='blue')


plt.grid(True)
plt.show()
lib.free(vector_ptr)
