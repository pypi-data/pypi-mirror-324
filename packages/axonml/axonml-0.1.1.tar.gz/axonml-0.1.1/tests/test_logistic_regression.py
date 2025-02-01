from axonml import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

def run():
    iris = load_iris()
    X = iris.data[iris.target != 2]  # Use only two classes for binary classification
    y = iris.target[iris.target != 2]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train custom logistic regression model
    model = LogisticRegression(learning_rate=0.1, num_iterations=2000)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\nMy Model for Logistic Regression")
    print("\nPredictions:", predictions)
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    run()
