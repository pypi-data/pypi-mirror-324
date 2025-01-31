import numpy as np

# Classification metrics
def recall(y: np.array, y_pred: np.ndarray) -> float:
    """
    Calculate the reall(True positive rate)

    Args:
        y_true (array): the actucal values
        y_pred (array): the predicted values

    Returns:
        int: the number of true positives over the number of actual positives
    """
    true_positives = 0
    actual_positives = 0
    for i in range(0, len(y), 100):
        y_true_batch = y[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        
        true_positives += np.sum((y_true_batch == 1) & (y_pred_batch == 1))
        actual_positives += np.sum(y_true_batch == 1)
        
    return true_positives / actual_positives

def precision(y: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate the precision

    Args:
        y_true (array): the actual values
        y_pred (array): the predicted values

    Returns:
        int: the number of true positives over the number of classsified positives
    """
    true_positives = 0
    calassified_possitives = 0
    for i in range(0, len(y), 100):
        y_true_batch = y[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        
        true_positives += np.sum((y_true_batch == 1) & (y_pred_batch == 1))
        calassified_possitives += np.sum(y_pred_batch == 1)
        
    return true_positives / calassified_possitives

def accuracy(y: np.ndarray, y_pred: np.ndarray) -> float:
    """
    calculate the accuracy

    Args:
        y_true (array): the actual values
        y_pred (array): the predicted values

    Returns:
        int: None
    """
    total_acurracy = 0
    for i in range(0, len(y), 100):
        y_true_batch = y[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        total_acurracy += np.sum(y_true_batch == y_pred_batch)
        
    return total_acurracy / len(y)

def confusion_matrix(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    true_positives = np.sum((y == 1) & (y_pred == 1))
    false_positives = np.sum((y == 0) & (y_pred == 1))
    true_negatives = np.sum((y == 0) & (y_pred == 0))
    false_negatives = np.sum((y == 1) & (y_pred == 0))
    return np.array([[true_positives, false_positives], [true_negatives, false_negatives]])

# Regression metcircs
def mean_absolute_error(y: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sum(np.abs(y_pred - y)) / len(y)

def mean_squared_error(y: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sum((y_pred - y) ** 2) / len(y)

def root_mean_squared_error(y: np.ndarray, y_pred: np.ndarray) -> float:
    """Cacluates the root mean squared error 
    given the actual values and the predicted ones.

    Args:
        y (np.ndarray): the actucal values
        y_pred (np.ndarray): the prediced values

    Returns:
        float: the rmse value
    """
    
    return np.sqrt(mean_squared_error(y, y_pred))