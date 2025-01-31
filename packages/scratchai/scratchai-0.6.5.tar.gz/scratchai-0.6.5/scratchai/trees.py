import numpy as np
from collections import Counter
from typing import Optional, Tuple

# static helpers functions
def _to_numeric(array: np.ndarray) -> np.ndarray:
    """Convert the given array to numeric if it is possible."""
    try:
        return array.astype('float')
    except:
        return array
    
def _most_common(array: list):
    """Returns the most common value in the given array."""
    count = Counter(array)
    return count.most_common(1)[0][0]

# Tree metrics functions
def entropy(y: np.ndarray) -> float:
    """Returns the entropy of the given set y."""
    _, counts = np.unique(y, return_counts = True)
    p = counts / len(y)
    return abs(-np.sum(p * np.log2(p)))

# Tree nodes
class _DecisionNode:
    def __init__(self, feature = None, threshold = None, left = None, right = None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        
class _LeafNode:
    def __init__(self, value = None):
        self.value = value

# Incomplete - Todo: provide doc strings for both tree classes methods.
class DecisionTreeClassifier:
    def __init__(self, max_depth: Optional[int] = 50, min_samples_split: Optional[int] = 5):
        # thr root node of th three
        self.root = None
        
        # the tree parameters
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = 0
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X: np.ndarray) -> None:
        """Initialize the features data types ."""
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X: np.ndarray, y: np.ndarray, max_features: Optional[int] = 0) -> None:
        """fit the decision tree model to the data.

        Args:
            X (array): the features array
            y (array): the target array
            max_features (int): the number of features to consider when looking for the best split
        """
        # initialize the features data types and grow the three
        self.max_features = max_features if max_features > 0 else X.shape[1]
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X: np.ndarray, y: np.ndarray, depth: Optional[int] = 0) -> Optional[_DecisionNode]:
        """Build the decsion tree nodes recursivly and return the root node."""
        n_samples = X.shape[0]
        n_labels = len(np.unique(y))
        
        # stop when no further split is needed
        if depth >= self.max_depth or n_samples <= self.min_samples_split or n_labels == 1:
            leaf_val = _most_common(y)
            return _LeafNode(value = leaf_val)
        
        # find the best split
        best_feature, best_threshold = self._best_split(X, y)
        
        # stop if there is no valid split
        if not best_feature and not best_threshold:
            leaf_val = _most_common(y)
            return _LeafNode(leaf_val)
        
        x = _to_numeric(X[:, best_feature])
        if self.dtypes[best_feature] == 'numeric':
            mask = (x >= best_threshold)
        else:
            mask = (x == best_threshold)
                 
        # split the data and pass it to the children nodes
        X_left, y_left = X[mask], y[mask]
        X_right, y_right = X[~mask], y[~mask]
        
        return _DecisionNode(best_feature,
                            best_threshold,
                            self._grow_tree(X_left, y_left, depth + 1),
                            self._grow_tree(X_right, y_right, depth + 1))
        
    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, Optional[int]]:
        """Finds the best condition among all feature given in X."""
        # randomly select features to consider for split
        n_features = X.shape[1]
        feature_idxs = np.random.choice(n_features,
                                        min(n_features, self.max_features),
                                        replace=False)
        
        # initialize the split results
        best_gain = float('-inf')
        best_feature = None
        best_threshold = None
        
        def eavluate_split(feature_idx: int) -> Tuple[int, int, Optional[int]]:
            """Returns the best condition given a feature."""
            # get the corresponding column for feature_idx
            x = _to_numeric(X[:, feature_idx])
            
            # initialize the feature_idx split reults
            best_gain = float('-inf')
            best_threshold = None
            
            # process the data in mini batches
            for start in range(0, X.shape[0], 512):
                end = min(start + 512, X.shape[0])
                x_sample = x[start:end]
                y_sample = y[start:end]
                
                # get the thresholds for the current batch
                thresholds = np.unique(x_sample)
                for start in range(0, thresholds.shape[0], 512):
                    end = min(start + 512, thresholds.shape[0])
                    thresholds_sample = thresholds[start:end]
                    
                    # get the mask for thresholds_sample
                    if self.dtypes[feature_idx] == 'numeric':
                        masks = x_sample[None ,:] >= thresholds[:, None]
                    else:
                        masks = x_sample[None ,:] == thresholds[:, None]
                        
                    # only evaluate valid thresholds to avoid division erros
                    left_counts = np.sum(masks, axis = 1)
                    right_counts = np.sum(~masks, axis = 1)
                    valid_splits = (left_counts > 0) & (right_counts > 0)
                    thresholds_sample = thresholds_sample[valid_splits]
                    masks = masks[valid_splits]
                    
                    if np.sum(valid_splits) == 0:
                        continue
                    
                    # evaluate the information gain and update the results
                    gains = np.array([self._gain(y_sample, mask) for mask in masks])
                    
                    if gains.shape[0] == 0:
                        continue
                    
                    max_gain = np.argmax(gains)
                    if gains[max_gain] > best_gain:
                        best_gain = gains[max_gain]
                        best_threshold= thresholds_sample[max_gain]
                        
            return best_gain, feature_idx, best_threshold
        
        results = [eavluate_split(feature_idx) for feature_idx in feature_idxs]
        for gain, feature, threshold in results:
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = threshold
                
        return best_feature, best_threshold
            
    def _gain(self, y: np.ndarray, mask: np.ndarray) -> float:
        """Returns the information gain based on the split mask."""
        left_entropy = entropy(y[mask])
        right_entropy = entropy(y[~mask])
        w = np.sum(mask) / len(y)
        
        return entropy(y) - (w * left_entropy + (1 - w) * right_entropy)
        
    
    def predict(self, X: np.ndarray):
        """predict the target values for the given data X

        Args:
            X (array): the features array

        Returns:
            array: the preicted values from X
        """
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X: np.ndarray, node: Optional[_DecisionNode]) -> Optional[int]:
        """Given a data point X, finds the prediction by traversing the tree recursivly and returns it."""
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.threshold:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.threshold:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        
class DecisionTreeRegressor:
    def __init__(self, max_depth: Optional[int] = 50, min_samples_split: Optional[int] = 5) -> None:
        # Tree root
        self.root = None
        
        # Tree parameters
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.max_features = 0
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X: np.ndarray) -> None:
        """Initialize the features data types."""
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X: np.ndarray, y: np.ndarray, max_features: Optional[int] = 0) -> None:
        """fit the decision tree model to the data.

        Args:
            X (array): the features array
            y (array): the target array
            max_features (int): the number of features to consider when looking for the best split
        """
        # initialize tree parameters and grow the three
        self.max_features = max_features if max_features > 0 else X.shape[1]
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X: np.ndarray, y: np.ndarray, depth: Optional[int] = 0) -> Optional[_DecisionNode]:
        """Grow the tree recursivly."""
        n_samples, uniques = X.shape[0], len(np.unique(y))
        
        # Stop if no further split is needed
        if depth >= self.max_depth or n_samples <= self.min_samples_split or uniques == 1:
            leaf_val = np.mean(y)
            return _LeafNode(value = leaf_val)
        
        # Finds the best split for the current node
        best_feature, best_threshold = self._best_split(X, y)
        
        # stop if there is no valid split
        if not best_feature and not best_threshold:
            leaf_val = np.mean(y)
            return _LeafNode(leaf_val)
            
        x = _to_numeric(X[:, best_feature])
        if self.dtypes[best_feature] == 'numeric':
            mask = (x >= best_threshold)
        else:
            mask = (x == best_threshold)
        
        # split the data and continue building the tree
        X_left, y_left = X[mask], y[mask]
        X_right, y_right = X[~mask], y[~mask]
        
        return _DecisionNode(best_feature,
                            best_threshold,
                            self._grow_tree(X_left, y_left, depth + 1),
                            self._grow_tree(X_right, y_right, depth + 1)
                            )
        
    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, Optional[int]]:
        """Finds the best split given X and y and returns the best feature and threshold."""
        # Randomly selects features to consider
        n_features = X.shape[1]
        feature_idxs = np.random.choice(n_features,
                                        min(n_features, self.max_features),
                                        replace=False)
        
        # Initialize the split results
        min_error = float('inf')
        best_feature, best_threshold = None, None
        
        def evaluate_split(feature_idx: int) -> Tuple[int, int, Optional[int]]:
            """Evaluate the feature_idx split."""
            # get the column corresponding to feature_idx
            x = _to_numeric(X[:, feature_idx])
            
            # initialize the feature_idx split results
            min_error = float('inf')
            best_threshold = None
            
            for start in range(0, X.shape[0], 512):
                end = min(start + 512, X.shape[0])
                x_sample = x[start:end]
                y_sample = y[start:end]
                
                # get all the possible thresholds for x_sample
                thresholds = np.unique(x_sample)
                for start in range(0, thresholds.shape[0], 256):
                    end = min(start + 256, thresholds.shape[0])
                    thresholds_sample = thresholds[start:end]
                    if self.dtypes[feature_idx] == 'numeric':
                        masks = x[None ,:] >= thresholds_sample[:, None]
                    else:
                        masks = x[None ,:] == thresholds_sample[:, None]
                    
                    # filter the thresholds sample to avoid computaional errors
                    left_counts = np.sum(masks, axis = 1)
                    right_counts = np.sum(~masks, axis = 1)
                    valid_splits = (left_counts > 0) & (right_counts > 0)
                    thresholds_sample = thresholds_sample[valid_splits]
                    masks = masks[valid_splits]
                    
                    if np.sum(valid_splits) == 0:
                        continue
                    
                    # caclulate the error for each valid threshold
                    errors = np.array([self._error(y_sample, mask) for mask in masks])
                    min_idx = np.argmin(errors)

                    if errors[min_idx] < min_error:
                        min_error = errors[min_idx]
                        best_threshold = thresholds_sample[min_idx]

            return min_error, feature_idx, best_threshold
                
        
        # evalute all features in feature_idxs and return the one with the min error
        results = [evaluate_split(feature_idx) for feature_idx in feature_idxs]
        for error, feature, threshold in results:
            if error < min_error:
                min_error = error
                best_feature = feature
                best_threshold = threshold
        
        return best_feature, best_threshold
            
    def _error(self, y: np.ndarray, mask: np.ndarray) -> float:
        """Calculate the mean squared error Given the set of examples y and mask."""
        left_mean = np.mean(y[mask])
        right_mean = np.mean(y[~mask])
        
        y_pred = left_mean * mask + right_mean * ~mask
        error = np.sum((y_pred - y) ** 2) / len(y)
        
        return error     
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """predict the target values for the given data X

        Args:
            X (array): the features array

        Returns:
            array: the preicted values from X
        """
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X: np.ndarray, node: Optional[_DecisionNode]) -> Optional[int]:
        """Traverse the tree recursively and return the prediction corresponding to X."""
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.threshold:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.threshold:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        