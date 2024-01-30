import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Generate synthetic data resembling a sine wave
np.random.seed(0)
X = np.linspace(0, 10, 100)
y_true = np.sin(X) + np.random.randn(100) * 0.1  # Sine wave with added noise

# Linear Regression
lr = LinearRegression()
lr.fit(X.reshape(-1, 1), y_true)
y_lr = lr.predict(X.reshape(-1, 1))

# Polynomial Regression (Degree 3)
degree_3 = 3
poly_features_3 = PolynomialFeatures(degree=degree_3, include_bias=False)
X_poly_3 = poly_features_3.fit_transform(X.reshape(-1, 1))
lr_poly_3 = LinearRegression()
lr_poly_3.fit(X_poly_3, y_true)
y_poly_3 = lr_poly_3.predict(X_poly_3)

# Polynomial Regression (Degree 5)
degree_5 = 5
poly_features_5 = PolynomialFeatures(degree=degree_5, include_bias=False)
X_poly_5 = poly_features_5.fit_transform(X.reshape(-1, 1))
lr_poly_5 = LinearRegression()
lr_poly_5.fit(X_poly_5, y_true)
y_poly_5 = lr_poly_5.predict(X_poly_5)

# Plot the results
plt.figure(figsize=(12, 6))
plt.scatter(X, y_true, label='True Data', color='b')
plt.plot(X, y_lr, label='Linear Regression', color='r', linestyle='--')
plt.plot(X, y_poly_3, label=f'Polynomial Regression (Degree {degree_3})', color='g')
plt.plot(X, y_poly_5, label=f'Polynomial Regression (Degree {degree_5})', color='purple')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression vs. Polynomial Regression (Degree 3 vs. Degree 5)')
plt.legend()
plt.grid(True)
plt.show()
