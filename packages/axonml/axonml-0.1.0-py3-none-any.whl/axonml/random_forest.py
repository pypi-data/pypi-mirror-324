import numpy as np
from axonml.decision_tree import DecisionTree

class RandomForest:
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2, min_impurity_decrease=0.0, method="entropy", task="classification", max_features=None):
        """
        Initialize the random forest classifier.

        Parameters:
        n_estimators (int): The number of decision trees in the forest.
        max_depth (int or None): Maximum depth of the decision trees. None means no limit.
        min_samples_split (int): Minimum number of samples required to split an internal node.
        min_impurity_decrease (float): Minimum impurity decrease to make a split.
        method (str): The method used for splitting ('entropy' or 'gini').
        task (str): The type of task ('classification' or 'regression').
        max_features (int or None): The number of features to consider when looking for the best split. None means all features.
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease
        self.method = method
        self.task = task
        self.max_features = max_features
        self.trees = []

    def fit(self, X, y):
        """
        Train the random forest classifier by building n_estimators decision trees.

        Parameters:
        X (numpy array): Training features.
        y (numpy array): Target values.
        """
        for _ in range(self.n_estimators):
            # Create a bootstrap sample of the data
            X_bootstrap, y_bootstrap = self._bootstrap_sample(X, y)
            
            # Create a new decision tree
            tree = DecisionTree(max_depth=self.max_depth, 
                                min_samples_split=self.min_samples_split, 
                                min_impurity_decrease=self.min_impurity_decrease, 
                                method=self.method, 
                                task=self.task)
            
            # Fit the tree to the bootstrap sample
            tree.fit(X_bootstrap, y_bootstrap)
            
            # Add the trained tree to the forest
            self.trees.append(tree)

    def predict(self, X):
        """
        Predict the target values by aggregating predictions from all trees.

        Parameters:
        X (numpy array): Features for prediction.

        Returns:
        numpy array: Predicted target values.
        """
        # Get predictions from all trees
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        
        if self.task == "classification":
            # Use majority voting for classification
            return np.array([np.bincount(tree_preds).argmax() for tree_preds in tree_predictions.T])
        else:
            # Use averaging for regression
            return np.mean(tree_predictions, axis=0)

    def _bootstrap_sample(self, X, y):
        """
        Generate a bootstrap sample by sampling with replacement.

        Parameters:
        X (numpy array): Features.
        y (numpy array): Target values.

        Returns:
        tuple: Bootstrapped features and target values.
        """
        indices = np.random.choice(len(X), size=len(X), replace=True)
        return X[indices], y[indices]
