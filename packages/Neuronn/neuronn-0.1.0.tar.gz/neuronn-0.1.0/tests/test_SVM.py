import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


iris = load_iris()
X, y = iris.data, iris.target

# Select only two classes for binary classification
X = X[y != 2]
y = y[y != 2]
y = np.where(y == 0, -1, 1)  # Convert labels to {-1, 1}

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM
svm = SVM()
svm.fit(X_train, y_train)
predictions = svm.predict(X_test)

# Print results
print("Predictions:", predictions)
print("True Labels:", y_test)

# PCA for visualization
pca = PCA(n_components=2)
X_train_2d = pca.fit_transform(X_train)
X_test_2d = pca.transform(X_test)

plt.figure(figsize=(10, 6))

# Plot training data
for label in np.unique(y_train):
    plt.scatter(
        X_train_2d[y_train == label, 0],
        X_train_2d[y_train == label, 1],
        label=f"Train Class {label}",
        alpha=0.6
    )

# Plot test data
for label in np.unique(predictions):
    plt.scatter(
        X_test_2d[predictions == label, 0],
        X_test_2d[predictions == label, 1],
        label=f"Test Predicted Class {label}",
        edgecolor="black",
        marker="x",
        s=100
    )

plt.title("SVM Classification Results (PCA Reduced Data)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid()
plt.show()