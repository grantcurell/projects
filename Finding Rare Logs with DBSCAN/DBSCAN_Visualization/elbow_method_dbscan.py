import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Generate random data
np.random.seed(42)
X = np.random.rand(100, 2)

# Run DBSCAN for a range of epsilon values and record the number of clusters
num_clusters = []
eps_range = np.linspace(0.01, 0.5, num=50)
for eps in eps_range:
    dbscan = DBSCAN(eps=eps, min_samples=5).fit(X)
    num_clusters.append(len(np.unique(dbscan.labels_)))

# Plot the number of clusters vs epsilon and sum of squared distances
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.plot(eps_range, num_clusters, '-o')
ax1.set_xlabel('Epsilon')
ax1.set_ylabel('Number of clusters')
ax1.set_title('Elbow curve')

inertias = []
for eps in eps_range:
    dbscan = DBSCAN(eps=eps, min_samples=5).fit(X)
    if len(set(dbscan.labels_)) > 1:
        mean_center = np.mean(X[dbscan.labels_ != -1], axis=0)
        inertia = np.sum(np.square(X[dbscan.labels_ != -1] - mean_center))
        inertias.append(inertia)
    else:
        inertias.append(0)

ax2.plot(eps_range, inertias, '-o')
ax2.set_xlabel('Epsilon')
ax2.set_ylabel('Inertia')
ax2.set_title('Inertia')
plt.show()
