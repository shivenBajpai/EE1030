import ctypes
import matplotlib.pyplot as plt

lib = ctypes.CDLL('./libvectors.so')


# Define the Vector struct in Python
class Vector(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float),
                ("norm", ctypes.c_float)]


# Specify the return type of the get_data function
lib.get_data.restype = ctypes.POINTER(ctypes.POINTER(Vector))

# Call the C function
n = 100
vector_ptrs = lib.get_data(n)

# Convert the C array to Python lists
vectors = [vector_ptrs[0][i] for i in range(n)]
scaled_vectors = [vector_ptrs[1][i] for i in range(n)]

# Extract norms for plotting
norms = [v.norm for v in vectors]
scaled_norms = [v.norm for v in scaled_vectors]

# Plot the norms
plt.figure(figsize=(10, 5))
plt.plot(norms, label="Original Norms")
plt.plot(scaled_norms, label="Scaled Norms")
plt.xlabel("Index")
plt.ylabel("Norm")
plt.title("Norms of 100 Randomly Scaled Vectors")
plt.legend()
plt.grid(True)
plt.show()
