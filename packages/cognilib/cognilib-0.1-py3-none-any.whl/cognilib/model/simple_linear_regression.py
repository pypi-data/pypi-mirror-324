import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cognilib.loss import mean_squared_error

class SimpleLinearRegression:
    def __init__(self):
        self.slope = np.random.rand()
        self.intercept = np.random.rand()

    def fit(self, X: np.ndarray, y: np.ndarray):
        if X.shape != y.shape:
            raise ValueError("X and y must have the same shape.")
        
        prediction = self.predict(X)

        lr = 0.01
        for _ in range(200):
            d_slope = -2 * np.mean(X * (y - prediction))
            d_intercept = -2 * np.mean(y - prediction)

            self.slope -= lr * d_slope
            self.intercept -= lr * d_intercept

            prediction = self.predict(X)
            
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.slope * X + self.intercept