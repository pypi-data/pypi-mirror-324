import numpy as np

class LinearRegression:
    """
    A simple Linear Regression model.
    """

    def __init__(self):
        """
        Initializes the model parameters.

        Attributes:
            weights (np.ndarray or None): The coefficients of the model.
            bias (float or None): The intercept term.
        """
        self.weights = None  
        self.bias = None     

    def fit(self, X, y):
        """
        Trains the linear regression model using the Normal Equation.

        Parameters:
            X (np.ndarray): The input features of shape (n_samples, n_features).
            y (np.ndarray): The target variable of shape (n_samples,).

        The function appends a column of ones to X for the bias term, computes
        the optimal weights using the Normal Equation, and separates the bias term.
        """
        X = np.c_[np.ones(X.shape[0]), X]
        X_transpose = X.T
        self.weights = np.linalg.inv(X_transpose.dot(X)).dot(X_transpose).dot(y)
        self.bias = self.weights[0] 
        self.weights = self.weights[1:]  
        
    def predict(self, X):
        """
        Makes predictions using the trained linear regression model.

        Parameters:
            X (np.ndarray): The input features of shape (n_samples, n_features).

        Returns:
            np.ndarray: The predicted values.
        """
        return X.dot(self.weights) + self.bias

    def calculate_mse(self, y_true, y_pred):
        """
        Computes the Mean Squared Error (MSE) between actual and predicted values.

        Parameters:
            y_true (np.ndarray): The actual target values.
            y_pred (np.ndarray): The predicted target values.

        Returns:
            float: The calculated MSE.
        """
        return np.mean((y_true - y_pred) ** 2)
