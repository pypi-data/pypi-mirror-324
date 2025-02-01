import numpy as np
from axonml import MultipleLinearRegression
from sklearn.metrics import mean_squared_error

def run():
    np.random.seed(43)
    X = np.random.rand(100, 3) * 10  # 100 samples, 3 features
    y = 2 * X[:, 0] + 3 * X[:, 1] + 4 * X[:, 2] + 5 + np.random.randn(100)  # Linear relation (y = 2*x1 + 3*x2 + 4*x3 + 5 + noise)

    # Split data into training and testing sets
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Custom Linear Regression
    model = MultipleLinearRegression(learning_rate=0.01, epochs=1000)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Calculate MSE for Custom Model
    custom_mse = mean_squared_error(y_test, predictions)

    # Print Results
    print("Multiple Linear Regression")
    print(f"My Model MSE: {custom_mse:.4f}")

if __name__ == "__main__":
    run()
