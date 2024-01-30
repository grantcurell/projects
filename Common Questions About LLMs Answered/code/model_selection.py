import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generating a synthetic dataset for house prices
np.random.seed(0)
data_size = 100
features = ['size', 'num_rooms']
X = np.random.rand(data_size, len(features)) * 100
prices = X[:, 0] * 3000 + X[:, 1] * 20000  # Price based on size and number of rooms

# Creating a DataFrame
df = pd.DataFrame(X, columns=features)
df['price'] = prices

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(df[features], df['price'], test_size=0.3, random_state=1)

# Appropriate Model: Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_predictions = linear_model.predict(X_test)

# Inappropriate Model: K-Means Clustering
kmeans_model = KMeans(n_clusters=3, random_state=1)
kmeans_model.fit(X_train)
kmeans_predictions = kmeans_model.predict(X_test)
kmeans_centers = kmeans_model.cluster_centers_
kmeans_prices = kmeans_centers[kmeans_predictions, 0] * 3000 + kmeans_centers[kmeans_predictions, 1] * 20000

# Selecting a few samples to plot
samples_to_plot = 5
indices = np.random.choice(range(len(y_test)), samples_to_plot, replace=False)

# Plotting the results
plt.figure(figsize=(10, 6))
width = 0.3  # the width of the bars
ind = np.arange(samples_to_plot)  # the x locations for the groups

# True values
plt.bar(ind - width, y_test.iloc[indices], width, label='True Values')

# Linear Regression Predictions
plt.bar(ind, linear_predictions[indices], width, label='Linear Regression Predictions')

# K-Means 'Predictions'
plt.bar(ind + width, kmeans_prices[indices], width, label='K-Means Cluster Center Prices')

plt.ylabel('Prices')
plt.title('Comparison of True Prices and Predictions')

plt.xticks(ind, [f'Sample {i+1}' for i in range(samples_to_plot)])
plt.legend(loc='best')
plt.show()
