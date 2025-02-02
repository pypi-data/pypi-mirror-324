import unittest
import numpy as np
import matplotlib.pyplot as plt
from cognilib.model import SimpleLinearRegression

class TestSimpleLinearRegression(unittest.TestCase):

    def test_simple_linear_regression(self):
        # Generate some random data
        X = np.random.rand(100)
        y = 2 * X + 3 + np.random.randn(100) * 0.1  # y = 2X + 3 + noise

        # Initialize and fit the model
        model = SimpleLinearRegression()
        model.fit(X, y)

        # Make predictions
        predictions = model.predict(X)

        # Check if predictions are close to actual values
        self.assertTrue(np.allclose(predictions, y, atol=0.5), "Predictions are not close to actual values")

        print("TestSimpleLinearRegression: Test passed!")

if __name__ == '__main__':
    unittest.main()
