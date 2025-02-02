import numpy as np
import matplotlib.pyplot as plt

class MultipleLinearRegression:
    def __init__(self, learning_rate=0.01, iterations=10000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.coefficients = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        # Add a column of ones to include the intercept in the coefficients
        X = np.c_[np.ones((n_samples, 1)), X]
        self.coefficients = np.zeros(n_features + 1)
        self.errors = []

        # Gradient descent
        for _ in range(self.iterations):
            y_predicted = np.dot(X, self.coefficients)
            residuals = y_predicted - y
            gradient = (1 / n_samples) * np.dot(X.T, residuals)
            self.coefficients -= self.learning_rate * gradient
            error = self.mean_squared_error(y, y_predicted)
            self.errors.append(error)

    def predict(self, X: np.ndarray) -> np.ndarray:
        n_samples = X.shape[0]
        X = np.c_[np.ones((n_samples, 1)), X]
        # print("print", self.coefficients)
        return np.dot(X, self.coefficients)

    def mean_squared_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.mean((y_true - y_pred) ** 2)

    def calculate_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return 100 - np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def plot_errors(self):
        plt.plot(range(self.iterations), self.errors)
        plt.xlabel('Iterations')
        plt.ylabel('Mean Squared Error')
        plt.title('Error Plot')
        plt.show()
