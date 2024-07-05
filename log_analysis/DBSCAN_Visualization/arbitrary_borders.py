import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# Generate synthetic data with overlapping Gaussian distributions
np.random.seed(0)
X1 = np.random.multivariate_normal(mean=[-2, -2], cov=[[1, 0], [0, 1]], size=1000)
X2 = np.random.multivariate_normal(mean=[2, 2], cov=[[1, 0], [0, 1]], size=1000)
X = np.vstack([X1, X2])

# Perform DBSCAN clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)

# Plot the results
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.axis('equal')
plt.title('DBSCAN Clustering with Arbitrary Borders')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

# Highlight cluster borders
db = DBSCAN(eps=0.5, min_samples=5).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.show()
