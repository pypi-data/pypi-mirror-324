import numpy as np

class MultipleLinearRegression:
    """
    Custom implementation of Multiple Linear Regression using Gradient Descent.
    """

    def __init__(self, learning_rate=0.01, epochs=1000):
        """
        Initialize the model with hyperparameters.
        
        Parameters:
        learning_rate (float): The learning rate for gradient descent.
        epochs (int): The number of iterations for training.
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None  # Coefficient(s)
        self.bias = None     # Intercept

    def fit(self, X, y):
        """
        Train the model using gradient descent.
        
        Parameters:
        X (numpy array): Training data (features).
        y (numpy array): Target values.
        """
        m, n = X.shape  # Number of samples (m) and features (n)
        
        # Initialize weights and bias to zero
        self.weights = np.zeros(n)
        self.bias = 0

        # Gradient Descent loop
        for epoch in range(self.epochs):
            # Predictions: y = X * weights + bias
            y_pred = np.dot(X, self.weights) + self.bias
            
            # Compute gradients
            dw = (-2 / m) * np.dot(X.T, (y - y_pred))  # Gradient for weights
            db = (-2 / m) * np.sum(y - y_pred)         # Gradient for bias
            
            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        """
        Predict target values for given features.
        
        Parameters:
        X (numpy array): Input features for prediction.
        
        Returns:
        numpy array: Predicted values.
        """
        # Predict: y = X * weights + bias
        return np.dot(X, self.weights) + self.bias
