import numpy as np
import ctypes
import matplotlib.pyplot as plt

lib = ctypes.CDLL('./libvectors.so')

def draw_angle_between_vectors(v1, v2, ax, angle, text_offset=0):
    # Normalize the vectors
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Compute the normal vector to the plane defined by v1 and v2
    normal = np.cross(v1, v2)
    
    # Normalize the normal vector
    normal = normal / np.linalg.norm(normal)

    # Calculate the angle between the vectors
    angle_rad = np.arccos(np.dot(v1, v2))
    angle_deg = np.degrees(angle_rad)  # Convert to degrees

    # Parametrize the arc
    theta = np.linspace(0, np.arccos(np.dot(v1, v2)), 100)
    arc_points = np.array([np.cos(t) * v1 + np.sin(t) * np.cross(normal, v1) for t in theta])/2

    # Plot the arc
    ax.plot(arc_points[:, 0], arc_points[:, 1], arc_points[:, 2], 'g', label='angle arc')

    # Label the angle in the middle of the arc
    mid_arc_point = arc_points[len(arc_points) // 2] + (v1+v2)/5
    ax.text(mid_arc_point[0]+text_offset, mid_arc_point[1], mid_arc_point[2], f'{angle:.0f}°', color='purple', fontsize=9)
    

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
vector = np.array([vector_ptr[0].x, vector_ptr[0].y, vector_ptr[0].z])*2; # All vectors are scaled by 2 to improve clarity of plot

# Plot the Vector
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(*origin, *vector, length=1, color='r')
ax.quiver(*origin, 0, 0, 2, length=1, color='k')
ax.quiver(*origin, 0, 2, 0, length=1, color='k')
ax.quiver(*origin, 2, 0, 0, length=1, color='k')

# Draw the angle arcs
draw_angle_between_vectors(np.array([0,0,1]),vector,ax,45,0.2)
draw_angle_between_vectors(np.array([0,1,0]),vector,ax,45)
draw_angle_between_vectors(np.array([1,0,0]),vector,ax,60)

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Label Axes
ax.text(1.2, -0.2, 0, "X", color='k')
ax.text(0, 1, 0, "Y", color='k')
ax.text(0, 0, 1, "Z", color='k')

plt.grid(True)
plt.show()
lib.free(vector_ptr)
