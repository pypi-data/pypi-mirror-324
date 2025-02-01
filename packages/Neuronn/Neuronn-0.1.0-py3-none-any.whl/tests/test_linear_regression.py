import numpy as np
import matplotlib.pyplot as plt
from linear_regression import LinearRegression

np.random.seed(42)
X = np.random.rand(100, 1) * 10  # Features (100 samples, 1 feature)
y = 2 * X + 1 + np.random.randn(100, 1)  # Linear relation (y = 2 * X + 1 + noise)
y = y.reshape(-1)  # Reshape y to match the shape of X for matrix operations

# Train the custom Linear Regression model
custom_model = LinearRegression(learning_rate=0.01, epochs=1000)
custom_model.fit(X, y)
custom_predictions = custom_model.predict(X)


# Print learned weights and bias for comparison
print("\nCustom Linear Regression:")
print(f"Learned weights: {custom_model.weights}")
print(f"Learned bias: {custom_model.bias}")

# Plotting the results
plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, custom_predictions, color='red', label='Custom Model Regression Line')

plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.title('Custom Linear Regression')
plt.show()