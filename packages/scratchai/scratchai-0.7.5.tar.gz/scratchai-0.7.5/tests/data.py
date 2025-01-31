import numpy as np
from typing import Optional, Tuple

def load_regression(size: Optional[int] = 150, categorical: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
    """Generate random dummy data for regression tasks."""
    
    # generate random feature values
    column_1 = np.random.choice(np.arange(6, 18), size).reshape(-1, 1)
    column_2 = np.random.choice(['Male', 'Female'], size).reshape(-1 , 1)
    if categorical:
        X = np.concatenate((column_1, column_2), axis = 1)
    else:
        X = column_1
    
    # generate random target values
    y = np.random.choice(100, size)
    
    return X, y
    
def load_classification(size: Optional[int] = 150,
                        categorical: Optional[bool] = True, 
                        binary: Optional[bool] = False) -> Tuple[np.ndarray, np.ndarray]:
    """Generate random dummy data for classification tasks."""
    
    # generate random feature values
    column_1 = np.random.choice(100, size = size).reshape(-1, 1)
    column_2 = np.random.choice(['Yes', 'No'], size = size).reshape(-1, 1)
    if categorical:
        X = np.concatenate((column_1, column_2), axis = 1)
    else:
        X = column_1
    
    # generate random target values
    if binary:
        y = np.random.choice([0, 1], size = size)
    else:
        y = np.random.choice(['A', 'B', 'C'], size = size)
    
    return X, y