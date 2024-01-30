import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate sample data
np.random.seed(0)
X = np.random.rand(50) * 10
y = 2 * X + 1 + np.random.randn(50) * 2  # Adding some random noise

# Create a range of hyperparameter values
slopes = [1.5, 2.0, 2.5]
intercepts = [0.5, 1.0, 1.5]

# Create subplots for each hyperparameter combination
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for i, (slope, intercept) in enumerate(zip(slopes, intercepts)):
    # Create and fit a linear regression model with the current hyperparameters
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)

    # Plot the scatterplot of the data points
    axs[i].scatter(X, y, label='Data', color='b')

    # Plot the regression line using the current hyperparameters
    regression_line = slope * X + intercept
    axs[i].plot(X, regression_line, label=f'LR (Slope={slope}, Intercept={intercept})', color='r')

    # Add labels and legend
    axs[i].set_xlabel('X')
    axs[i].set_ylabel('Y')
    axs[i].set_title(f'Linear Regression (Slope={slope}, Intercept={intercept})')
    axs[i].legend()

plt.tight_layout()
plt.show()
