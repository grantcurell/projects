import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift
from concurrent.futures import ThreadPoolExecutor

# Generate synthetic data
np.random.seed(0)
X = np.random.randn(1000, 2) * 2 + np.array([10, 10])

# Perform mean-shift clustering
def worker(bandwidth):
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    return ms

bandwidths = np.linspace(0.1, 5, 100)
with ThreadPoolExecutor() as executor:
    ms_list = list(executor.map(worker, bandwidths))

# Find the number of clusters for each bandwidth
n_clusters = [len(np.unique(ms.labels_)) for ms in ms_list]

# Find the bandwidth with the most clusters
best_bandwidth = bandwidths[np.argmax(n_clusters)]

# Perform mean-shift clustering with the best bandwidth
ms = MeanShift(bandwidth=best_bandwidth, bin_seeding=True)
ms.fit(X)

# Plot the results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.scatter(X[:, 0], X[:, 1], s=10)
ax1.set_title('Original data')

ax2.scatter(X[:, 0], X[:, 1], c=ms.labels_, s=10, cmap='viridis')
ax2.set_title(f'Mean-shift clustering (bandwidth={best_bandwidth:.2f})')

plt.show()
