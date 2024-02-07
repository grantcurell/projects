import matplotlib.pyplot as plt
import numpy as np

# Define the vertices of an equilateral triangle
radius = 1  # Arbitrary radius
angles = np.deg2rad([0, 120, 240])  # Angles for the vertices
triangle_points = np.array([np.cos(angles), np.sin(angles)]) * radius

# Calculate the center (neutral point) of the triangle
center_point = np.mean(triangle_points, axis=1)

# Plot the equilateral triangle (Phase-to-Phase)
plt.figure(figsize=(6, 6))
plt.plot(*np.hstack((triangle_points, triangle_points[:, [0]])), 'b-', marker='o', label='Phase-to-Phase Voltage')

# Plot lines from the center to each vertex (Phase-to-Neutral Voltage)
for point in zip(*triangle_points):
    plt.plot([center_point[0], point[0]], [center_point[1], point[1]], 'r--', label='Phase-to-Neutral Voltage' if point == tuple(triangle_points[:, 0]) else "")

# Highlight the center point (Neutral)
plt.plot(center_point[0], center_point[1], 'go', label='Neutral Point')

# Add annotations
for i, angle in enumerate(angles, start=1):
    plt.text(triangle_points[0, i-1] * 1.1, triangle_points[1, i-1] * 1.1, f'Phase {i}', horizontalalignment='center')

plt.text(center_point[0] * 0.9, center_point[1] * 0.9, 'Neutral', color='green')

# Adjust plot
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.title('Equilateral Triangle Representing 3-Phase System')
plt.xlabel('Real Axis')
plt.ylabel('Imaginary Axis')
plt.show()
