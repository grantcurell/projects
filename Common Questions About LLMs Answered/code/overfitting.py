import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

# Generate synthetic data points
np.random.seed(0)
x = np.linspace(0, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 2, len(x))

# Generate predictions for model 1 (line between every data point) on training data
y_pred_model1_train = np.array([])
for i in range(len(x) - 1):
    slope = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
    intercept = y[i] - slope * x[i]
    x_range = np.linspace(x[i], x[i + 1], 10)
    y_pred_model1_train = np.concatenate([y_pred_model1_train, slope * x_range + intercept])

# Generate predictions for model 2 (straight line) on training data
y_pred_model2_train = 2 * x + 1

# Calculate MSE for both models on training data
mse_model1_train = mean_squared_error(y, y_pred_model1_train[:len(y)])
mse_model2_train = mean_squared_error(y, y_pred_model2_train)

# Generate new synthetic data points for testing
x_new = np.linspace(0, 10, 100)
y_new = 2 * x_new + 1 + np.random.normal(0, 2, len(x_new))

# Generate predictions for model 1 (line between every data point) on new data
y_pred_model1_new = np.array([])
for i in range(len(x) - 1):
    slope = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
    intercept = y[i] - slope * x[i]
    x_range = np.linspace(x[i], x[i + 1], 10)
    y_pred_model1_new = np.concatenate([y_pred_model1_new, slope * x_range + intercept])

# Generate predictions for model 2 (straight line) on new data
y_pred_model2_new = 2 * x_new + 1

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Top left: Line between every single data point
axes[0, 0].scatter(x, y, label='Training Data', color='blue')
for i in range(len(x) - 1):
    axes[0, 0].plot([x[i], x[i + 1]], [y[i], y[i + 1]], color='red')
axes[0, 0].set_title('Overfit to Training Data')

# Top right: Straight line through the data
axes[0, 1].scatter(x, y, label='Training Data', color='blue')
axes[0, 1].plot(x, 2 * x + 1, color='red', label='Well Fit Line')
axes[0, 1].set_title('Well Fit to Training Data')

# Bottom left: Reproduce the line from top left on new data
axes[1, 0].scatter(x_new, y_new, label='Real Data', color='green')
for i in range(len(x) - 1):
    slope = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
    intercept = y[i] - slope * x[i]
    x_range = np.linspace(x[i], x[i + 1], 10)
    y_range = slope * x_range + intercept
    axes[1, 0].plot(x_range, y_range, color='purple')
axes[1, 0].set_title('Overfit Model in Real World')

# Bottom right: Same straight line as top right on new data
axes[1, 1].scatter(x_new, y_new, label='Real Data', color='green')
axes[1, 1].plot(x_new, 2 * x_new + 1, color='purple', label='Straight Line Fit (New Data)')
axes[1, 1].set_title('Well Fit Model Real World')

# Set common labels and legends
for ax in axes.flatten():
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

plt.tight_layout()
plt.show()
