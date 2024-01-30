import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

# Generate some random points
np.random.seed(42)
points = np.random.rand(100, 2)

# Compute the distances to the 5th nearest neighbor
k = 5
tree = cKDTree(points)
distances, indices = tree.query(points, k=k+1)
avg_distances = np.mean(distances[:, 1:], axis=1)

# Plot the average distances
plt.plot(np.arange(len(points)), np.sort(avg_distances))
plt.xlabel('Point index')
plt.ylabel('Average distance to {}th neighbor'.format(k))
plt.title('Average nearest neighbor distance')
plt.show()
