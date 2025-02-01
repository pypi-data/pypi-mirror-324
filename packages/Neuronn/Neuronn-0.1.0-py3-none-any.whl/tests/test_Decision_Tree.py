from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from Decision_Tree import DecisionTree
import numpy as np
# Load the Iris dataset
data = load_iris()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the custom decision tree
tree = DecisionTree(max_depth=5)
tree.fit(X_train, y_train)

# Make predictions and calculate accuracy for the custom model
predictions = tree.predict(X_test)
accuracy = np.sum(predictions == y_test) / len(y_test)



# Print accuracy of both models
print(f" DecisionTree Accuracy: {accuracy:.2f}")
