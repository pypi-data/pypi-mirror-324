import numpy as np

def train_test_split(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = None, shuffle: bool = True):
    """
    Splits data into training and test sets

    Parameters:
        X (np.ndarray): Features
        y (np.ndarray): Target variable
        test_size (float): Fraction of the data to be used as test set
        random_state (int): Seed for random number generation
        shuffle (bool): Whether to shuffle the data before splitting
    
    Returns:
        X_train, X_test, y_train, y_test: Split subsets of data and target variable
    """

    if (len(X) != len(y)):
        raise ValueError("X and y must have the same length")
    
    if shuffle:
        if random_state is not None:
            np.random.seed(random_state)
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        X = X[indices]
        y = y[indices]
    
    split_index = int(len(X) * (1 - test_size))

    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    return X_train, X_test, y_train, y_test
