import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Generate random data
np.random.seed(42)
X = np.random.rand(100, 2)

# Set up parameter grid
eps_range = np.linspace(0.01, 0.5, num=50)
min_samples_range = range(1, 11)
param_grid = [(eps, min_samples) for eps in eps_range for min_samples in min_samples_range]

# Run DBSCAN for each parameter combination and record the number of clusters
num_clusters = []
for eps, min_samples in param_grid:
    dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    num_clusters.append(len(np.unique(dbscan.labels_)))

# Reshape results into a grid
num_clusters = np.array(num_clusters)
num_clusters_grid = num_clusters.reshape(len(eps_range), len(min_samples_range))

# Plot the grid search results
plt.imshow(num_clusters_grid, cmap='viridis', aspect='auto', extent=[1, 10, 0.01, 0.5])
plt.xlabel('min_samples')
plt.ylabel('eps')
plt.title('Grid search results')
plt.colorbar()
plt.show()
