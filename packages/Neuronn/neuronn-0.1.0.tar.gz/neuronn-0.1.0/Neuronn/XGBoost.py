import numpy as np
from sklearn.metrics import mean_squared_error
from Decision_Tree_Reg import DecisionTree


class XGBoost:
    def __init__(self, n_estimators=100, learning_rate=0.001, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []

    def _gradient(self, y_true, y_pred):
        return y_true - y_pred  # Gradient for regression is the residual error

    def fit(self, X, y):
        n_samples = X.shape[0]
        y_pred = np.zeros(n_samples)  # Initialize prediction as zeros

        print("\n For training dataset: ")
        for i in range(self.n_estimators):
            gradient = self._gradient(y, y_pred)
            
            # Use the optimized custom decision tree
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X, gradient)  # Fit tree on the residuals
            update = tree.predict(X)
            
            y_pred += self.learning_rate * update  # Update the prediction
            
            if (i + 1) % 10 == 0:
                mse = mean_squared_error(y, y_pred)
                print(f" {i + 1}th Estimator: MSE = {mse}")

    def predict(self, X):
        y_pred = np.zeros(X.shape[0])
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(X)  # No rounding for regression
        return y_pred  # Return continuous output
    

