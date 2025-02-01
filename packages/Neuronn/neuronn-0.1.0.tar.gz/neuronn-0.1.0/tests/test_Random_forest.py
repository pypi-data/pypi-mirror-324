import numpy as np
from sklearn.utils import resample
from Random_forest import RandomForest

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load the Iris dataset
data = load_iris()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the random forest
forest = RandomForest(n_estimators=10, max_depth=3)
forest.fit(X_train, y_train)

# Make predictions and calculate accuracy
predictions = forest.predict(X_test)
accuracy = np.sum(predictions == y_test) / len(y_test)
print(f"Random Forest Accuracy: {accuracy:.2f}")
