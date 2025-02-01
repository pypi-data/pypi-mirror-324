import numpy as np
from collections import Counter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def main():
    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Custom KNN Classifier
    custom_knn = KNN(k=3)
    custom_knn.fit(X_train, y_train)
    custom_predictions = custom_knn.predict(X_test)


    # Accuracy Comparison
    custom_accuracy = accuracy_score(y_test, custom_predictions)


    print("Custom KNN Accuracy:", custom_accuracy)
    # Visualize results using PCA
    pca = PCA(n_components=2)
    X_train_2d = pca.fit_transform(X_train)
    X_test_2d = pca.transform(X_test)

    plt.figure(figsize=(12, 8))

    # Plot training data
    for label in np.unique(y_train):
        plt.scatter(
            X_train_2d[y_train == label, 0],
            X_train_2d[y_train == label, 1],
            label=f"Train Class {label}",
            alpha=0.6,
        )

    # Plot test data predictions (Custom KNN)
    for label in np.unique(custom_predictions):
        plt.scatter(
            X_test_2d[np.array(custom_predictions) == label, 0],
            X_test_2d[np.array(custom_predictions) == label, 1],
            label=f"Custom KNN Class {label}",
            edgecolor="black",
            marker="x",
            s=100,
        )

    plt.title("Custom KNN Classification Results (PCA Reduced Data)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()