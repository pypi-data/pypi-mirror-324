import numpy as np
from axonml import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def run():
    X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
    y = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

    # Split data into training and test sets (70% train, 30% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Custom Linear Regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_test_predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, y_test_predictions)
    print(f"My Linear Regression MSE: {mse:.4f}")

if __name__ == "__main__":
    run()
