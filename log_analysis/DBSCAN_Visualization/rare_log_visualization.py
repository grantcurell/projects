import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# Generate simulated data
np.random.seed(42)
X = np.random.randn(1000, 2)
X[:10] += 10  # Add some rare events

# Compute DBSCAN clustering
dbscan = DBSCAN(eps=1.5, min_samples=3).fit(X)

# Identify clusters with low point density
core_samples = dbscan.core_sample_indices_
labels = dbscan.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

# Plot the identified clusters
plt.figure(figsize=(8, 6))
colors = plt.cm.get_cmap('viridis', n_clusters)
for i in range(n_clusters):
    if i == -1:
        color = 'gray'
    else:
        color = colors(i)
    cluster = X[labels == i]
    plt.scatter(cluster[:, 0], cluster[:, 1], c=color, s=50, edgecolors='none')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('DBSCAN Clustering')
plt.show()

# Identify rare events
outliers = X[labels == -1]
print(f'Number of rare events: {len(outliers)}')
