import numpy as np

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, min_impurity_decrease=0.0, method="entropy", task="classification"):
        """
        Initialize the decision tree classifier.

        Parameters:
        max_depth (int or None): Maximum depth of the tree. None means no limit.
        min_samples_split (int): Minimum number of samples required to split an internal node.
        min_impurity_decrease (float): Minimum impurity decrease to make a split.
        method (str): The method used for splitting ('entropy' or 'gini').
        task (str): The type of task ('classification' or 'regression').
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease
        self.method = method
        self.task = task
        self.tree = None

    def fit(self, X, y):
        """
        Fit the model to the training data.
        
        Parameters:
        X (numpy array): Training features.
        y (numpy array): Target values.
        """
        self.tree = self.build_tree(X, y)

    def predict(self, X):
        """
        Predict the target values for the input features.
        
        Parameters:
        X (numpy array): Features for prediction.
        
        Returns:
        numpy array: Predicted target values.
        """
        return np.array([self._traverse_tree(x, self.tree) for x in X])

    def build_tree(self, X, y, depth=0):
        """
        Recursively build the decision tree.

        Parameters:
        X (numpy array): Training features.
        y (numpy array): Target values.
        depth (int): Current depth of the tree.
        
        Returns:
        dict: The structure of the decision tree.
        """
        if (self.max_depth is not None and depth >= self.max_depth) or len(X) < self.min_samples_split or len(np.unique(y)) == 1:
            return {"leaf": True, "value": self._leaf_value(y)}

        best_feature, best_threshold, best_gain = self._find_best_split(X, y)

        if best_feature is None or best_gain < self.min_impurity_decrease:
            return {"leaf": True, "value": self._leaf_value(y)}

        left_idxs, right_idxs = self._split(X[:, best_feature], best_threshold)

        return {
            "leaf": False,
            "feature": best_feature,
            "threshold": best_threshold,
            "left": self.build_tree(X[left_idxs], y[left_idxs], depth + 1),
            "right": self.build_tree(X[right_idxs], y[right_idxs], depth + 1),
        }

    def _find_best_split(self, X, y):
        """
        Find the best feature and threshold to split the data based on information gain.
        
        Parameters:
        X (numpy array): Features.
        y (numpy array): Target values.
        
        Returns:
        tuple: Best feature, best threshold, and best information gain.
        """
        best_gain, best_feature, best_threshold = -1, None, None
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                gain = self._information_gain(X[:, feature], y, threshold)
                if gain > best_gain:
                    best_gain, best_feature, best_threshold = gain, feature, threshold

        return best_feature, best_threshold, best_gain

    def _information_gain(self, X_column, y, threshold):
        """
        Calculate the information gain for a split.
        
        Parameters:
        X_column (numpy array): A single feature column.
        y (numpy array): Target values.
        threshold (float): Threshold value for splitting.
        
        Returns:
        float: The information gain from the split.
        """
        left_idxs, right_idxs = self._split(X_column, threshold)
        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        if self.task == "classification":
            parent_impurity = self._entropy(y) if self.method == "entropy" else self._gini(y)
            left_impurity = self._entropy(y[left_idxs]) if self.method == "entropy" else self._gini(y[left_idxs])
            right_impurity = self._entropy(y[right_idxs]) if self.method == "entropy" else self._gini(y[right_idxs])
        else:  # Regression
            parent_impurity = self._variance(y)
            left_impurity = self._variance(y[left_idxs])
            right_impurity = self._variance(y[right_idxs])

        n = len(y)
        return parent_impurity - (len(left_idxs) / n * left_impurity + len(right_idxs) / n * right_impurity)

    def _split(self, X_column, threshold):
        """
        Split the data based on the given threshold.
        
        Parameters:
        X_column (numpy array): A single feature column.
        threshold (float): Threshold for the split.
        
        Returns:
        tuple: Indices of samples in the left and right splits.
        """
        left_idxs = np.where(X_column <= threshold)[0]
        right_idxs = np.where(X_column > threshold)[0]
        return left_idxs, right_idxs

    def _entropy(self, y):
        """
        Calculate the entropy of the target variable.
        
        Parameters:
        y (numpy array): Target values.
        
        Returns:
        float: The entropy of the target variable.
        """
        pro = np.bincount(y) / len(y)
        return -np.sum([p * np.log2(p) for p in pro if p > 0])

    def _gini(self, y):
        """
        Calculate the Gini impurity of the target variable.
        
        Parameters:
        y (numpy array): Target values.
        
        Returns:
        float: The Gini impurity of the target variable.
        """
        pro = np.bincount(y) / len(y)
        return 1 - np.sum([p ** 2 for p in pro])

    def _variance(self, y):
        """
        Calculate the variance of the target variable.
        
        Parameters:
        y (numpy array): Target values.
        
        Returns:
        float: The variance of the target variable.
        """
        return np.var(y)

    def _leaf_value(self, y):
        """
        Determine the value assigned to a leaf node.
        
        Parameters:
        y (numpy array): Target values.
        
        Returns:
        value: The leaf node value.
        """
        if self.task == "classification":
            return np.bincount(y).argmax()
        else:  # Regression
            return np.mean(y)

    def _traverse_tree(self, x, node):
        """
        Traverse the decision tree to make a prediction.
        
        Parameters:
        x (numpy array): A single sample.
        node (dict): The current tree node.
        
        Returns:
        value: The predicted value.
        """
        if node["leaf"]:
            return node["value"]
        if x[node["feature"]] <= node["threshold"]:
            return self._traverse_tree(x, node["left"])
        else:
            return self._traverse_tree(x, node["right"])