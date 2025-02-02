import unittest
import numpy as np
from cognilib.model import MultipleLinearRegression

class TestMultipleLinearRegression(unittest.TestCase):

    def test_multiple_linear_regression(self):
        # Generate some random data
        X = np.random.rand(100, 3)
        y = 2 * X[:, 0] + 3 * X[:, 1] + 4 * X[:, 2] + 5 + np.random.randn(100) * 0.1  # y = 2X1 + 3X2 + 4X3 + 5 + noise

        # Initialize and fit the model
        model = MultipleLinearRegression()
        model.fit(X, y)

        # Make predictions
        predictions = model.predict(X)

        # Check if predictions are close to actual values
        self.assertTrue(np.allclose(predictions, y, atol=0.5), "Predictions are not close to actual values")

        print("TestMultipleLinearRegression: Test passed!")

if __name__ == '__main__':
    unittest.main()
