import unittest
import numpy as np
from cognilib.loss import mean_squared_error

class TestMeanSquaredError(unittest.TestCase):

    def test_mean_squared_error(self):
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.1, 3.1, 4.1, 5.1])
        mse = mean_squared_error(y_true, y_pred)
        self.assertTrue(np.isclose(mse, 0.01), f"Mean Squared Error is {mse}")

        print("TestMeanSquaredError: Test passed!")

if __name__ == '__main__':
    unittest.main()
