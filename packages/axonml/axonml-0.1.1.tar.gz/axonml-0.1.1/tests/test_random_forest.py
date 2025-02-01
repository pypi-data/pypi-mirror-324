import pandas as pd
import numpy as np
from axonml import RandomForest
from sklearn.metrics import accuracy_score

def run():
    # Load the Iris dataset
    data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data", header=None)
    data[4] = data[4].astype("category").cat.codes
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Split into training and test sets
    indices = np.random.permutation(len(X))
    train_size = int(0.8 * len(X))
    train_idx, test_idx = indices[:train_size], indices[train_size:]
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    # Train custom random forest
    rf = RandomForest(n_estimators=100, max_depth=5, min_impurity_decrease=0.01)
    rf.fit(X_train, y_train)

    # Evaluate
    predictions = rf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print("Random Forest Accuracy:", accuracy)

if __name__ == "__main__":
    run()
