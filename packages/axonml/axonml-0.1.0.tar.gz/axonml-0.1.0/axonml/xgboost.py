import numpy as np

class DecisionTree:
    def __init__(self, max_depth=3):
        """
        Initialize a Decision Tree classifier.

        Parameters:
        max_depth (int): Maximum depth of the tree.
        """
        self.max_depth = max_depth  # Set maximum depth of tree
        self.split_feature = None  # To store the feature that splits the data at the node
        self.split_value = None  # To store the threshold value for the split
        self.left_value = None  # Predicted value for the left leaf node
        self.right_value = None  # Predicted value for the right leaf node

    def fit(self, X, residuals, hessians, depth=2):
        """
        Fit a decision tree based on residuals and Hessians.

        Parameters:
        X (numpy array): Features of the training dataset.
        residuals (numpy array): Gradients (errors) from the previous iteration.
        hessians (numpy array): Second derivatives of the loss function (Hessian).
        depth (int): Current depth of the tree during recursion.
        """
        # Base case: If the tree has reached max depth, calculate the optimal leaf value
        if depth >= self.max_depth:
            self.left_value = -np.sum(residuals) / np.sum(hessians)  # Optimal value for leaf node
            return  # End recursion at max depth

        best_gain = -np.inf  # Initialize the best gain to negative infinity

        # Loop through all features
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])  # Get unique values for the current feature

            # Loop through all possible thresholds for the feature
            for threshold in thresholds:
                # Create boolean arrays for left and right splits based on the threshold
                left_idx = X[:, feature] <= threshold
                right_idx = ~left_idx

                # Skip splits if either side is empty
                if left_idx.sum() == 0 or right_idx.sum() == 0:
                    continue

                # Calculate gain based on residuals and Hessians for the current split
                gain = (np.sum(residuals[left_idx])**2 / np.sum(hessians[left_idx]) +
                        np.sum(residuals[right_idx])**2 / np.sum(hessians[right_idx]))
                
                # Update best split if current gain is better than previous best
                if gain > best_gain:
                    best_gain = gain
                    self.split_feature = feature  # Store the feature index that provides the best split
                    self.split_value = threshold  # Store the threshold value for the best split
                    # Calculate predicted values for the left and right leaf nodes
                    self.left_value = -np.sum(residuals[left_idx]) / np.sum(hessians[left_idx])
                    self.right_value = -np.sum(residuals[right_idx]) / np.sum(hessians[right_idx])

    def predict(self, X):
        """
        Predict values based on the learned decision tree.

        Parameters:
        X (numpy array): Input features for prediction.

        Returns:
        numpy array: Predicted values based on the learned splits.
        """
        # Initialize an array with the left leaf value for all samples
        preds = np.full(X.shape[0], self.left_value)

        # Find samples that satisfy the condition for the left split
        left_idx = X[:, self.split_feature] <= self.split_value
        preds[left_idx] = self.left_value  # Assign left leaf value
        preds[~left_idx] = self.right_value  # Assign right leaf value to the remaining samples

        return preds  # Return the predicted values

class XGBoost:
    def __init__(self, n_estimators=50, learning_rate=0.1, max_depth=1):
        """
        Initialize the XGBoost model from scratch.

        Parameters:
        n_estimators (int): Number of boosting rounds (trees).
        learning_rate (float): Learning rate for gradient boosting.
        max_depth (int): Maximum depth of decision trees.
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []

    def fit(self, X, y):
        """
        Train the XGBoost model using gradient boosting.

        Parameters:
        X (numpy array): Training features.
        y (numpy array): Target values (labels).
        """
        y_pred = np.zeros_like(y, dtype=float)  # Initialize predictions
        for _ in range(self.n_estimators):
            g = self.gradient(y, y_pred)  # Compute the gradient
            h = self.hessian(y)   # Compute the Hessian (second derivative)

            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X, g, h)  # Fit decision tree based on gradient and Hessian

            y_pred += self.learning_rate * tree.predict(X)  # Update predictions
            self.trees.append(tree)

    def predict(self, X):
        """
        Predict the target values using the trained model.

        Parameters:
        X (numpy array): Features for prediction.

        Returns:
        numpy array: Predicted values.
        """
        y_pred = np.zeros(X.shape[0])
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(X)  # Sum up predictions from each tree
        return y_pred

    def gradient(self, y_true, y_pred):
        """
        Calculate the gradient (first derivative) of the loss function.

        Parameters:
        y_true (numpy array): True labels.
        y_pred (numpy array): Predicted values.

        Returns:
        numpy array: Gradient of the loss function.
        """
        return 2 * (y_pred - y_true)  # Gradient of MSE

    def hessian(self, y_true):
        """
        Calculate the Hessian (second derivative) of the loss function.

        Parameters:
        y_true (numpy array): True labels.

        Returns:
        numpy array: Hessian of the loss function.
        """
        return np.ones_like(y_true) * 2  # Hessian for MSE
