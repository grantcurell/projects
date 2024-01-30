import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(-20, 20, 200)

# Define slopes with the middle panel having slope 1
slopes = [0.5, 1, 1.5]
intercepts = [0, 0, 0]  # Fixed intercepts at 0

# Create subplots for each slope value
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for i, slope in enumerate(slopes):
    # Calculate the corresponding y values for each slope
    y = slope * x

    # Plot the line graph
    axs[i].plot(x, y, label=f'y = {slope}x', color='r')

    # Set axis limits to show all quadrants
    axs[i].set_xlim(-20, 20)
    axs[i].set_ylim(-20, 20)

    # Add axes lines
    axs[i].axhline(0, color='black', linewidth=0.5)
    axs[i].axvline(0, color='black', linewidth=0.5)

    # Add labels and legend
    axs[i].set_xlabel('X')
    axs[i].set_ylabel('Y')
    axs[i].set_title(f'Line Graph with Slope = {slope}')
    axs[i].legend()

plt.tight_layout()
plt.show()
