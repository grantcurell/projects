from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import numpy as np

# Generate random data with 2 features and 4 clusters
X, y = make_blobs(n_samples=1000, n_features=2, centers=4, random_state=42)

# Range of cluster sizes to consider
cluster_sizes = range(2, 11)

# For each cluster size, fit a KMeans model and compute the silhouette score
silhouette_scores = []
for k in cluster_sizes:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)

# Plot the silhouette scores vs. cluster size
plt.plot(cluster_sizes, silhouette_scores, '-o')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')
plt.title('Silhouette analysis')
plt.show()
