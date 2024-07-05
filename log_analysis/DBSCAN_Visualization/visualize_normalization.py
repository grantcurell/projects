import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import probplot
from sklearn.preprocessing import StandardScaler

# Generate some random data
X = np.random.normal(loc=5, scale=2, size=(100, 2))

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create a figure with subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Plot the data before standardization
axs[0, 0].scatter(X[:, 0], X[:, 1])
axs[0, 0].set_title("Before Standardization")

# Plot the data after standardization
axs[0, 1].scatter(X_scaled[:, 0], X_scaled[:, 1])
axs[0, 1].set_title("After Standardization")

# Plot the Q-Q plots for the two variables before and after standardization
probplot(X[:, 0], plot=axs[1, 0], fit=False)
axs[1, 0].set_title("Before Standardization (Variable 1)")
probplot(X_scaled[:, 0], plot=axs[1, 1], fit=False)
axs[1, 1].set_title("After Standardization (Variable 1)")

# Add labels to the x- and y-axes
axs[0, 0].set_xlabel("Variable 1")
axs[0, 0].set_ylabel("Variable 2")
axs[0, 1].set_xlabel("Variable 1 (standardized)")
axs[0, 1].set_ylabel("Variable 2 (standardized)")
axs[1, 0].set_xlabel("Theoretical Quantiles")
axs[1, 0].set_ylabel("Ordered Values")
axs[1, 1].set_xlabel("Theoretical Quantiles")
axs[1, 1].set_ylabel("Ordered Values")

plt.show()
