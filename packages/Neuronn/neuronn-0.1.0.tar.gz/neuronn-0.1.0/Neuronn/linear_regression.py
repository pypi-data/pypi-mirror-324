import numpy as np



# Custom Linear Regression Class (from previous code)
class LinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate  # Learning rate
        self.epochs = epochs  # Number of iterations
        self.weights = None  # Initialize weights
        self.bias = None  # Initialize bias

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

    def compute_loss(self, X, y):
        m = len(y)
        predictions = self.predict(X)
        loss = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        return loss

    def fit(self, X, y):
        m = len(y)
        self.weights = np.zeros(X.shape[1])  # Initialize weights
        self.bias = 0  # Initialize bias
        
        for epoch in range(self.epochs):
            predictions = self.predict(X)
            dw = (1 / m) * np.dot(X.T, (predictions - y))
            db = (1 / m) * np.sum(predictions - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            if epoch % 100 == 0:
                loss = self.compute_loss(X, y)
                print(f"Epoch {epoch}/{self.epochs}, Loss: {loss}")
