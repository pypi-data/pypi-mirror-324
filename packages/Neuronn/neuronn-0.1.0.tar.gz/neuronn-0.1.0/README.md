
# Py-Neuronn

Neuronn is a collection of machine learning models implemented from scratch. This library provides simple and easy-to-use implementations of various machine learning algorithms, including linear regression, multiple regression, logistic regression, k-nearest neighbors (KNN), decision trees,random forests,XGB classifier and SVM.

## Installation

You can install Neuronn using pip:

```bash
pip install Neuronn
```

## Usage

Here an examples of how to use the models provided by Neuron:

### Linear Regression

```python
from Neuronn import LinearRegression
import numpy as np

# Example data
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

# Create and train the model
model = LinearRegression(learning_rate=0.01, epochs=1000)
model.fit(X, y)

# Make predictions
predictions = model.predict(X)
print("Predictions:", predictions)

```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please contact [Karthikeyan](mailto:karthikkrishna0907@gmail.com).
