import numpy as np

class SVMClassifier:
    def __init__(self, learning_rate=0.001, regularization=0.01, num_iterations=1000):
        """
        Initialize the Support Vector Machine classifier.

        Parameters:
        learning_rate (float): Learning rate for gradient descent.
        regularization (float): Regularization strength.
        num_iterations (int): Number of iterations for gradient descent.
        """
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """
        Train the Support Vector Machine using stochastic gradient descent.

        Parameters:
        X (numpy array): Training features.
        y (numpy array): Target values (labels).
        """
        num_samples, num_features = X.shape
        y_transformed = np.where(y <= 0, -1, 1)  # Convert labels to -1 and 1

        self.weights = np.zeros(num_features)  # Initialize weights
        self.bias = 0  # Initialize bias

        for _ in range(self.num_iterations):
            # Stochastic gradient descent
            for idx, x_i in enumerate(X):
                condition = y_transformed[idx] * (np.dot(x_i, self.weights) - self.bias) >= 1
                if condition:
                    # If the condition is satisfied, update weights with regularization
                    self.weights -= self.learning_rate * (2 * self.regularization * self.weights)
                else:
                    # If the condition is not satisfied, update weights and bias
                    self.weights -= self.learning_rate * (
                        2 * self.regularization * self.weights - np.dot(x_i, y_transformed[idx])
                    )
                    self.bias -= self.learning_rate * y_transformed[idx]

    def predict(self, X):
        """
        Predict the target values based on the learned hyperplane.

        Parameters:
        X (numpy array): Features for prediction.

        Returns:
        numpy array: Predicted labels (-1 or 1).
        """
        linear_output = np.dot(X, self.weights) - self.bias
        return np.sign(linear_output)  # Return -1 or 1 depending on sign of linear_output
