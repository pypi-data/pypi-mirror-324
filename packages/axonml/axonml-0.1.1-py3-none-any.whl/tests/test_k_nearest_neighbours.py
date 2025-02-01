from axonml import KNN
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def run():
    data = load_iris()
    X = data.data
    y = data.target

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train KNN model from scratch (with Manhattan distance and weighted votes)
    knn_scratch = KNN(k=3, metric='manhattan', weighted=True)
    knn_scratch.fit(X_train, y_train)
    y_pred_scratch = knn_scratch.predict(X_test)

    # Accuracy of the KNN from scratch
    accuracy_scratch = accuracy_score(y_test, y_pred_scratch)
    print(f"Accuracy of KNN from Scratch (Manhattan & Weighted): {accuracy_scratch * 100:.2f}%")

if __name__ == "__main__":
    run()
