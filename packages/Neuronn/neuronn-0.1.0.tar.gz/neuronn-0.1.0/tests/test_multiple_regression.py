import numpy as np
from sklearn.metrics import mean_squared_error
from  multiple_regression import MultipleLinearRegression

# Generate synthetic data with 3 features
np.random.seed(42)
X = np.random.rand(100, 3) * 10  # 100 samples, 3 features
y = 2 * X[:, 0] + 3 * X[:, 1] + 4 * X[:, 2] + 5 + np.random.randn(100)  # Linear relation (y = 2*x1 + 3*x2 + 4*x3 + 5 + noise)

# Custom Multiple Linear Regression Model
custom_model = MultipleLinearRegression(learning_rate=0.01, epochs=1000)
custom_model.fit(X, y)
custom_predictions = custom_model.predict(X)



# Print learned weights and bias for comparison
print("\nCustom Multiple Linear Regression:")
print(f"Learned weights: {custom_model.weights}")
print(f"Learned bias: {custom_model.bias}")


# Calculate Mean Squared Error for both models
custom_mse = mean_squared_error(y, custom_predictions)


print("\nMean Squared Error Comparison:")
print(f"Custom Model MSE: {custom_mse}")