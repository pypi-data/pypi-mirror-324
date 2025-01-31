import numpy as np

from typing import Optional, Tuple

class StandardScaler:
    def __init__(self):
        self.std = dict()
        self.mean = dict()
        
    def transform(self, X: Optional[np.ndarray], columns: list[Optional[int]]):
        for column in columns:
            # store the feature standard and the mean for inverse sacling
            self.std[column] = X[column].std()
            self.mean[column] = X[column].mean()
            
            # scale the feature using the stored standard and mean
            X.loc[:, column] = (X[column] - self.mean[column]) / self.std[column]
            
        return X
    
    def inverse_transform(self, X: Optional[np.ndarray], columns: Optional[list[int]]):
        for column in columns:
            if column not in self.mean or column not in self.std:
                raise ValueError(f"{column} not found in StandardScaler")
            
            X[column] = (X[column] + self.mean[column] * self.std[column])
            
        return X
    
def split_data(X: Optional[np.ndarray], split_size: Optional[float] = 0.8) -> Tuple[np.ndarray, np.ndarray]:
    n_examples = len(X)
    
    # shuffle X before spliting
    shuffled = np.random.permutation(X)
    
    # split the set of examples X into two sets and return them
    splitIdx = int(n_examples * split_size)
    fst, snd = X[:splitIdx], X[splitIdx:]
    
    return fst, snd
    
def polynomial_features(X: np.ndarray, degree: int = 1, inetraction_term: Optional[bool] = False):
    poly_features = []
    
    for row in X:
        inter_term = 1
        poly_row = []
        for v in row:
            inter_term *= v
            poly_row += [v ** d for d in range(1, degree + 1)]
        if inetraction_term:
            poly_row.append(inter_term)
        poly_features.append(poly_row)
        
    return np.array(poly_features)

# TODO: Complete onhot_encode and add a label_encode
class DataEncoder:
    def __init__(self):
        pass
    
    def onthot_encode(self, 
                      X: Optional[np.ndarray], 
                      columns: Optional[list[int]] = None, 
                      dtype: Optional[str] = 'int') -> np.ndarray:
        def onthot_column(x: np.ndarray):
            uniques = np.unique(x)
            if len(uniques) >= 20:
                raise ValueError(f"DataEncoder cannot encode data with more than 20 classes")

            encoded = x[None ,:] == uniques[:, None]
            return encoded.astype(dtype)
                
        
        # Handle when given a single column
        if not columns and X.ndim == 1:
            return onthot_column(X, 0)