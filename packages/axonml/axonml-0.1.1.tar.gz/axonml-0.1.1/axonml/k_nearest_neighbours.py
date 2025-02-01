import numpy as np
from collections import Counter

class KNN:
    """
    K-Nearest Neighbors (KNN) classifier implemented from scratch.
    The algorithm classifies a sample based on the majority label of its k-nearest neighbors.
    """
    
    def __init__(self, k=3, metric='euclidean', weighted=False):
        """
        Initialize the KNN classifier with hyperparameters.
        
        Parameters:
        k (int): The number of nearest neighbors to consider.
        metric (str): The distance metric to use ('euclidean' or 'manhattan').
        weighted (bool): Whether to apply weighted voting based on distance.
        """
        self.k = k
        self.metric = metric
        self.weighted = weighted
    
    def fit(self, X_train, y_train):
        """
        Store the training data (X_train, y_train) for use during prediction.
        
        Parameters:
        X_train (numpy array): The training features.
        y_train (numpy array): The labels for the training data.
        """
        self.X_train = X_train
        self.y_train = y_train
    
    def predict(self, X_test):
        """
        Predict the class labels for the test dataset.
        
        Parameters:
        X_test (numpy array): The input features for prediction.
        
        Returns:
        numpy array: The predicted class labels for each test sample.
        """
        predictions = [self._predict(x) for x in X_test]
        return np.array(predictions)
    
    def _predict(self, x):
        """
        Predict the class label for a single test sample by calculating 
        the distances to all training samples and selecting the most 
        common class label among the k-nearest neighbors.
        
        Parameters:
        x (numpy array): The test sample.
        
        Returns:
        int: The predicted class label.
        """
        # Calculate distances between the test sample and all training samples
        distances = [self._compute_distance(x, x_train) for x_train in self.X_train]
        
        # Get the indices of the k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        if self.weighted:
            # Apply weighted voting based on inverse distance
            return self._predict_weighted(k_nearest_labels, distances, k_indices)
        
        # Return the most common class label among the k neighbors
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]
    
    def _compute_distance(self, x1, x2):
        """
        Compute the distance between two points based on the selected metric.
        
        Parameters:
        x1 (numpy array): The first point.
        x2 (numpy array): The second point.
        
        Returns:
        float: The computed distance based on the selected metric.
        """
        if self.metric == 'manhattan':
            return self.manhattan_distance(x1, x2)
        return self.euclidean_distance(x1, x2)
    
    def euclidean_distance(self, x1, x2):
        """
        Calculate the Euclidean distance between two points (x1, x2).
        
        Parameters:
        x1 (numpy array): First data point.
        x2 (numpy array): Second data point.
        
        Returns:
        float: The Euclidean distance between the points.
        """
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def manhattan_distance(self, x1, x2):
        """
        Calculate the Manhattan distance between two points (x1, x2).
        
        Parameters:
        x1 (numpy array): First data point.
        x2 (numpy array): Second data point.
        
        Returns:
        float: The Manhattan distance between the points.
        """
        return np.sum(np.abs(x1 - x2))
    
    def _predict_weighted(self, k_nearest_labels, distances, k_indices):
        """
        Compute the class label prediction using weighted voting.
        
        Parameters:
        k_nearest_labels (list): Labels of the k nearest neighbors.
        distances (list): List of distances to the nearest neighbors.
        k_indices (list): Indices of the k nearest neighbors.
        
        Returns:
        int: The class label with the highest weighted vote.
        """
        # Calculate weights based on distance (1/distance)
        weights = [1 / (distances[i] + 1e-5) for i in k_indices]  # Adding epsilon to avoid division by zero
        label_weights = {}
        
        # Accumulate the weights for each label
        for i, label in enumerate(k_nearest_labels):
            if label in label_weights:
                label_weights[label] += weights[i]
            else:
                label_weights[label] = weights[i]
        
        # Return the class with the maximum weight
        return max(label_weights, key=label_weights.get)