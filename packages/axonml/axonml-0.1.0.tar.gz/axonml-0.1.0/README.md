# AxonML

AxonML is a lightweight machine learning package that provides easy-to-use implementations of fundamental ML algorithms. It is designed for beginners and practitioners who want to understand and experiment with ML models without relying on heavy dependencies.

## Features

- **Simple and efficient implementations** of core ML algorithms.
- **No heavy dependencies**—built using NumPy.
- **Easy-to-use API** for training and predictions.

## Installation

```bash
pip install axonml
```

## Supported Algorithms

AxonML includes the following machine learning algorithms:

1. **Linear Regression** – Predicts continuous values using a linear relationship.
2. **Multiple Linear Regression** – Extends linear regression to multiple features.
3. **Logistic Regression** – Used for binary classification tasks.
4. **K-Nearest Neighbors (KNN)** – A non-parametric classification algorithm.
5. **Decision Tree** – A tree-based model for classification and regression.
6. **Random Forest** – An ensemble learning method using multiple decision trees.
7. **Support Vector Machine (SVM)** – A powerful classification model.
8. **XGBoost** – Gradient boosting algorithm for improved accuracy.

## Usage

### Example: Linear Regression

```python
from axonml.linear_regression import LinearRegression
import numpy as np

# Sample dataset
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Model training
model = LinearRegression()
model.fit(X, y)

# Prediction
predictions = model.predict(X)
print(predictions)
```
