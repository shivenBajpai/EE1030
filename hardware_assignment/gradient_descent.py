import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split

# Load data
A = np.loadtxt('data.csv', dtype=np.double)
P = A[:, [0]]
Y = A[:, [1]].ravel()

# Transform data to include polynomial features
poly = PolynomialFeatures(degree=2)
X = poly.fit_transform(P)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, Y_train, Y_test, P_train, P_test = train_test_split(X_scaled, Y, P, test_size=0.1, shuffle=True)

# Initialize and fit the model with gradient descent
model = SGDRegressor(verbose=True, penalty='l2', early_stopping=False, learning_rate='invscaling', max_iter=50000, tol=1e-13)
model.fit(X_train, Y_train)

# Print the coefficients and intercept
print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)

# Plotting function
def plot(ax, P, Y_true, Y_pred, title):
    ax.plot(P, Y_true, 'k.', label="True")
    ax.plot(P, Y_pred, 'r.', label="Predicted")
    ax.set_title(title)
    ax.legend()

# Plot training and test predictions
fig, axes = plt.subplots(1, 2, figsize=(10,5))
plot(axes[0], P_train, Y_train, model.predict(X_train), "Training Data")
plot(axes[1], P_test, Y_test, model.predict(X_test), "Validation")

print((sum((model.predict(X_train)-Y_train)**2)))

plt.tight_layout()
plt.show()
