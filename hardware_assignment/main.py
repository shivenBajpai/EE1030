import numpy as np
import matplotlib.pyplot as plt

def loss(x, y, h):
    return sum(((x@h)-y)**2)

def plot(axes, p, x, y, model, title):
    axes.plot(p, x@model)
    axes.plot(p, y, 'k.')
    axes.grid()
    axes.set_ylabel('Output Voltage (V)')
    axes.set_xlabel('Temperature ($^{\\circ}$C)')
    axes.set_title(title)

# Data loading and extraction
A = np.loadtxt('data.csv', dtype=np.double)
np.random.shuffle(A)
X = np.hstack((np.ones((A.shape[0],1)),A[:,[0]],A[:,[0]]**2))
X_train = np.sort(X[:-5], axis=0)
X_test = np.sort(X[-5:], axis=0)
T_train = np.sort(A[:,[0]][:-5], axis=0)
T_test = np.sort(A[:,[0]][-5:], axis=0)
Y_train = np.sort(A[:,[1]][:-5], axis=0)
Y_test = np.sort(A[:,[1]][-5:], axis=0)

# Setup subplots
fig, axes = plt.subplots(2, 3, figsize=(10,8))

# Least squares method
n_lsq = np.array(np.linalg.lstsq(X_train, Y_train, rcond=None)[0])

plot(axes[0][0], T_train, X_train, Y_train, n_lsq, "Using np.linalg.lstsq")
plot(axes[1][0], T_test, X_test, Y_test, n_lsq, "Validation")

# Plot the training results
# axes[0][0].plot(T_train, X_train@n_lsq)
# axes[0][0].plot(T_train, Y_train, 'k.')
# axes[0][0].grid()
# axes[0][0].set_ylabel('Output Voltage (V)')
# axes[0][0].set_xlabel('Temperature ($^{\\circ}$C)')
# axes[0][0].set_title("Using np.linalg.lstsq")

# Plot the validation results
# axes[1][0].plot(T_test, X_test@n_lsq)
# axes[1][0].plot(T_test, Y_test, 'k.')
# axes[1][0].grid()
# axes[1][0].set_ylabel('Output Voltage (V)')
# axes[1][0].set_xlabel('Temperature ($^{\\circ}$C)')
# axes[1][0].set_title("Validation")



# Normal equation method
a = np.linalg.inv(X_train.T@X_train)@X_train.T@Y_train

# Plot the training results
axes[0][1].plot(T_train, X_train@a)
axes[0][1].plot(T_train, Y_train, 'k.')
axes[0][1].grid()
axes[0][1].set_title('Least Squares Fit using Normal Equation')
axes[0][1].set_ylabel('Output Voltage (V)')
axes[0][1].set_xlabel('Temperature ($^{\\circ}$C)')

# Plot the validation results
axes[1][1].plot(T_test, X_test@a)
axes[1][1].plot(T_test, Y_test, 'k.')
axes[1][1].grid()
axes[1][1].set_ylabel('Output Voltage (V)')
axes[1][1].set_xlabel('Temperature ($^{\\circ}$C)')
axes[1][1].set_title("Validation")





# Perform SVD
U, Sigma, VT = np.linalg.svd(X_train)

# Construct the pseudoinverse matrix
Sigma_pseudoinverse = np.zeros((U.shape[0], VT.shape[0]))

# Take the reciprocal of the non-zero singular values
for i in range(len(Sigma)): 
    if Sigma[i] != 0: Sigma_pseudoinverse[i, i] = 1 / Sigma[i]

# Calculate the coefficients
beta = VT.T @ Sigma_pseudoinverse.T @ U.T @ Y_train

# Plot the training results
axes[0][2].plot(T_train, X_train @ beta)
axes[0][2].plot(T_train, Y_train, '.k')
axes[0][2].grid()
axes[0][2].set_ylabel('Output Voltage (V)')
axes[0][2].set_xlabel('Temperature ($^{\\circ}$C)')
axes[0][2].set_title('Least Squares Fit using SVD')

# Plot the validation results
axes[1][2].plot(T_test, X_test@beta)
axes[1][2].plot(T_test, Y_test, 'k.')
axes[1][2].grid()
axes[1][2].set_ylabel('Output Voltage (V)')
axes[1][2].set_xlabel('Temperature ($^{\\circ}$C)')
axes[1][2].set_title("Validation")

plt.tight_layout()
plt.show()

# Print out the losses of all 3 approaches
print(loss(X_train,Y_train,n_lsq))
print(loss(X_train,Y_train,a))
print(loss(X_train,Y_train,beta))
