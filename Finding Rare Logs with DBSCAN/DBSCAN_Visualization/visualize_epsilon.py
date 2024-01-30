import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN

# Generate some example data
X, _ = make_moons(n_samples=1000, noise=0.1, random_state=42)

# Define different values of epsilon and min_samples
epsilons = [0.05, 0.1, 0.3]
min_samples = 5

# Run DBSCAN for each value of epsilon and plot the results
fig, axs = plt.subplots(1, len(epsilons), figsize=(12, 4))
for i, epsilon in enumerate(epsilons):
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    y_pred = dbscan.fit_predict(X)
    n_clusters = len(set(y_pred)) - (1 if -1 in y_pred else 0)
    axs[i].scatter(X[:, 0], X[:, 1], c=y_pred)
    axs[i].set_title(f"eps={epsilon}, clusters={n_clusters}")

plt.show()
