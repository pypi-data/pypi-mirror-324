import numpy as np

# Loss functions
def _mse(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return (1 / len(y)) * np.sum((y - y_pred) ** 2)

def _dmse(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return (-1 / len(y)) * (y - y_pred)

def _bce(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return (1 / len(y)) * (-y * np.log2(y_pred) - (1 - y) * np.log2(1 - y_pred))

def _cce(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return (1 / len(y)) * -np.sum(y * np.log2(y_pred))

def _dce(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return y_pred - y

if __name__ == '__main__' or __package__ == None:
    raise ImportError('This is an internel module and not meant for direct import.')