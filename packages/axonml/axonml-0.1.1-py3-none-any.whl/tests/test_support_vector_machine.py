from axonml import SVMClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score

def run():
    X, y = make_blobs(n_samples=50, n_features=2, centers=2, cluster_std=1.05, random_state=40) 
    y = np.where(y == 0, -1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    svm_classifier = SVMClassifier()
    svm_classifier.fit(X_train, y_train)
    predictions = svm_classifier.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print("SVM Classification Accuracy:", accuracy)

if __name__ == "__main__":
    run()
