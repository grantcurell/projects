import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Generate sample data
np.random.seed(0)
x = np.random.rand(50) * 10
y = 2 * x + 1 + np.random.randn(50) * 2  # Adding some random noise

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Create a scatterplot of the data
plt.scatter(x, y, label='Data', color='b')

# Create the regression line
regression_line = slope * x + intercept

# Plot the regression line
plt.plot(x, regression_line, label='Linear Regression', color='r')

# Add labels and legend
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

# Display the plot
plt.title('Linear Regression Demo')
plt.show()

# Output the regression results
print(f"Slope: {slope:.2f}")
print(f"Intercept: {intercept:.2f}")
print(f"R-squared value: {r_value**2:.2f}")
