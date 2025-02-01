import numpy as np

class LogisticRegression:
    """
    A custom logistic regression model implemented from scratch using 
    gradient descent to optimize the weights and bias.
    """
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        """
        Initialize the logistic regression model with the given hyperparameters.

        Parameters:
        learning_rate (float): The step size used to update the weights during training.
        num_iterations (int): The number of iterations for training the model.
        """
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None  
        self.bias = None 

    @staticmethod
    def sigmoid(z):
        """
        The sigmoid activation function used for binary classification.

        Parameters:
        z (numpy array): The input value (linear combination of inputs and weights).

        Returns:
        numpy array: The sigmoid function applied element-wise to z.
        """
        return 1 / (1 + np.exp(-z))

    def initialize_params(self, n_features):
        """
        Initialize the weights and bias of the model to zeros.

        Parameters:
        n_features (int): The number of features in the input dataset.
        """
        self.weights = np.zeros(n_features)
        self.bias = 0

    def binary_cross_entropy(self, y_true, y_pred):
        """
        Compute the binary cross-entropy loss, which measures the difference 
        between the predicted probabilities and the actual labels.

        Parameters:
        y_true (numpy array): The true labels.
        y_pred (numpy array): The predicted probabilities.

        Returns:
        float: The binary cross-entropy loss value.
        """
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)  # To avoid log(0)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss

    def fit(self, X, y):
        """
        Train the logistic regression model using gradient descent.

        Parameters:
        X (numpy array): The input features.
        y (numpy array): The true labels.
        """
        num_samples, num_features = X.shape
        self.initialize_params(num_features)  # Initialize parameters

        # Gradient Descent loop for weight optimization
        for i in range(self.num_iterations + 1):
            linear_model = np.dot(X, self.weights) + self.bias  # Linear combination
            y_pred = self.sigmoid(linear_model)  # Sigmoid function for probabilities

            # Calculate gradients for weights and bias
            dw = (1 / num_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / num_samples) * np.sum(y_pred - y)

            # Update weights and bias using the computed gradients
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X, threshold=0.5):
        """
        Predict the class labels for the given input data.

        Parameters:
        X (numpy array): The input features.
        threshold (float): The probability threshold to classify as positive (default is 0.5).

        Returns:
        numpy array: The predicted class labels (0 or 1).
        """
        linear_model = np.dot(X, self.weights) + self.bias
        y_pred = self.sigmoid(linear_model)
        return (y_pred >= threshold).astype(int)

    def evaluate_accuracy(self, y_true, y_pred):
        """
        Evaluate the accuracy of the model based on true and predicted labels.

        Parameters:
        y_true (numpy array): The true labels.
        y_pred (numpy array): The predicted class labels.

        Returns:
        float: The accuracy percentage.
        """
        accuracy = np.mean(y_true == y_pred) * 100
        return accuracy
