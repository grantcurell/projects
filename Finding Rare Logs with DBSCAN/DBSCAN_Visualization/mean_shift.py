import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import MeanShift

# Generate random data
X, y = make_blobs(n_samples=1000, centers=5, random_state=42)

# Apply mean shift clustering
bandwidth = 1.5
ms = MeanShift(bandwidth=bandwidth)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

# Plot the results
fig, ax = plt.subplots()
ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')

# Plot the cluster centers
ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], s=100, marker='o', facecolors='none', edgecolors='k')

plt.title('Mean Shift Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
