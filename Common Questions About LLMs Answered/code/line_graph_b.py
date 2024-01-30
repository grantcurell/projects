import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(-20, 20, 200)

# Define slopes and intercepts
slopes = [1, 1, 1]
intercepts = [5, 0, -5]  # Varying intercepts (including one with b=0)

# Create subplots for each intercept value
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for i, intercept in enumerate(intercepts):
    # Calculate the corresponding y values for each intercept
    y = slopes[i] * x + intercept

    # Plot the line graph
    axs[i].plot(x, y, label=f'y = x + {intercept}', color='r')

    # Set axis limits to show all quadrants
    axs[i].set_xlim(-20, 20)
    axs[i].set_ylim(-20, 20)

    # Add axes lines
    axs[i].axhline(0, color='black', linewidth=0.5)
    axs[i].axvline(0, color='black', linewidth=0.5)

    # Add labels and legend
    axs[i].set_xlabel('X')
    axs[i].set_ylabel('Y')
    axs[i].set_title(f'Line Graph with b = {intercept}')
    axs[i].legend()

plt.tight_layout()
plt.show()
