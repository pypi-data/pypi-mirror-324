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

1. **Linear Regression** - A basic regression model that fits a linear relationship between independent and dependent variables.
2. **Multiple Linear Regression** - An extension of linear regression that handles multiple input features.
3. **Logistic Regression** - A classification algorithm based on the sigmoid function for binary classification problems.
4. **K-Nearest Neighbors (KNN)** - A non-parametric method used for classification and regression based on distance metrics.
5. **Decision Tree** - A tree-based model that splits data based on feature importance to make decisions.
6. **Random Forest** - An ensemble method using multiple decision trees to improve prediction accuracy and reduce overfitting.
7. **Support Vector Machine (SVM)** - A powerful classification algorithm that finds the optimal hyperplane for separating classes.
8. **XGBoost** - An optimized gradient boosting algorithm that builds trees sequentially to minimize errors.

## Usage

### Example: Linear Regression

```python
from axonml import LinearRegression
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

Similarly, you can use other models like **Logistic Regression, KNN, Decision Tree, Random Forest, SVM, and XGBoost**.

## License

AxonML is licensed under the MIT License.

---

**Happy Coding with AxonML! 🚀**
