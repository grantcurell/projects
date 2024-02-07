# Import necessary libraries for drawing
import matplotlib.pyplot as plt
import numpy as np

# Initialize figure
plt.figure(figsize=(8, 8))

# Equilateral triangle points (120 degrees apart)
angles_deg = np.array([0, 120, 240]) + 90  # Offset by 90 degrees to stand triangle on a side
angles_rad = np.deg2rad(angles_deg)
triangle_points = np.array([np.cos(angles_rad), np.sin(angles_rad)])

# Center of the triangle (neutral point)
center_point = np.mean(triangle_points, axis=1)

# Draw the equilateral triangle
plt.plot(*np.hstack((triangle_points, triangle_points[:, [0]])), 'b-o', label='Phase-to-Phase')

# Draw phase-to-neutral lines
for i in range(3):
    plt.plot([center_point[0], triangle_points[0, i]], [center_point[1], triangle_points[1, i]], 'r--', label='Phase-to-Neutral' if i == 0 else "")

# Annotate the 30-60-90 triangle
# Draw the 30-60-90 triangle lines
plt.plot([triangle_points[0, 1], 0.5 * (triangle_points[0, 1] + triangle_points[0, 2])],
         [triangle_points[1, 1], 0.5 * (triangle_points[1, 1] + triangle_points[1, 2])], 'g-', label='30-60-90 Triangle')

# Annotations for angles
plt.text(triangle_points[0, 0] * 1.1, triangle_points[1, 0] * 1.1, 'Phase 1', horizontalalignment='center')
plt.text(triangle_points[0, 1] * 1.1, triangle_points[1, 1] * 1.1, 'Phase 2', horizontalalignment='center')
plt.text(triangle_points[0, 2] * 1.1, triangle_points[1, 2] * 1.1, 'Phase 3', horizontalalignment='center')
plt.text(center_point[0], center_point[1], 'Neutral', color='green', horizontalalignment='center')

# Highlight the bisected angle creating the 30-60-90 triangle
midpoint = 0.5 * (triangle_points[:, 1] + triangle_points[:, 2])
plt.plot([center_point[0], midpoint[0]], [center_point[1], midpoint[1]], 'g-', label='Bisector')

# Display settings
plt.xlabel('Real Axis')
plt.ylabel('Imaginary Axis')
plt.title('Equilateral Triangle with 30-60-90 Triangle Highlighted')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
