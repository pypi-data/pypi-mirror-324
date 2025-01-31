import numpy as np
from collections import Counter
from typing import Optional

# static helpers functions
def _to_numeric(array: np.ndarray):
    """Convert the given array to numeric if it is possible."""
    try:
        return array.astype('float')
    except:
        return array
    
def _most_common(array: list):
    """Returns the most common value in array"""
    count = Counter(array)
    return count.most_common(1)[0][0]

# Tree metrics functions
def entropy(y: np.ndarray):
    """Returns the entropy of the given set y."""
    _, counts = np.unique(y, return_counts = True)
    p = counts / len(y)
    return abs(-np.sum(p * np.log2(p)))

# Tree nodes
class _DecisionNode:
    def __init__(self, feature = None, value = None, left = None, right = None):
        self.feature = feature
        self.value = value
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
        self.num_split_features = 0
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X: np.ndarray):
        """Initialize features data types by getting each column data type in X."""
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X: np.ndarray, y: np.ndarray, n_features: Optional[int] = 0):
        """fit the decision tree model to the data

        Args:
            X (array): the features array
            y (array): the target array
            n_features (int): the number of features to consider when looking for the best split
        """
        # initialize the features data types and grow the three
        self.num_split_features = n_features if n_features > 0 else X.shape[1]
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X: np.ndarray, y: np.ndarray, depth = 0):
        """Build the decsion tree nodes recursivly and return the root node."""
        n_samples = X.shape[0]
        n_labels = len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or n_labels == 1:
            leaf_val = _most_common(y)
            return _LeafNode(value = leaf_val)
        
        # find the best split
        best_feature, best_threshold = self._best_split(X, y)
        
        x = _to_numeric(X[:, best_feature])
        if self.dtypes[best_feature] == 'numeric':
            mask = (x >= best_threshold)
        else:
            mask = (x == best_threshold)
                 
        # split the data and pass it to the children nodes
        X_left, X_right = X[mask], X[~mask]
        y_left, y_right = y[mask], y[~mask]
        
        left, right = [self._grow_tree(X_sample, y_sample, depth + 1) 
                    for X_sample, y_sample in [(X_left, y_left),(X_right, y_right)]]
        
        return _DecisionNode(best_feature, best_threshold,
                            left, right)
        
    def _best_split(self, X: np.ndarray, y: np.ndarray):
        """Finds the best condition among all feature given in X."""
        # randomly select features to consider for split
        n_features = X.shape[1]
        feature_idxs = np.random.choice(n_features,
                                        min(n_features, self.num_split_features),
                                        replace=False)
        
        # initialize the split results
        best_gain = float('-inf')
        best_feature = None
        best_threshold = None
        
        def eavluate_split(feature_idx: int):
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
                    valid_thresholds = (left_counts > 0) & (right_counts > 0)
                    thresholds_sample = thresholds_sample[valid_thresholds]
                    masks = masks[valid_thresholds]
                    
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
            
    def _gain(self, y: np.ndarray, mask: np.ndarray):
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
    
    def _traverse_tree(self, X: np.ndarray, node: _DecisionNode):
        """Given a data point X, finds the prediction by traversing the tree recursivly and returns it."""
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        
class DecisionTreeRegressor:
    def __init__(self, min_samples_split = 20, max_depth = 50):
        # Tree root
        self.root = None
        
        # Tree parameters
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
        # performance settings
        self.thresh_batch = 64
        self.process_batch = 128
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X):
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X, y):
        """fit the decision tree model to the data

        Args:
            X (array): the features array
            y (array): the target array
        """
        # initialize the features data types and grow the three
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X, y, depth = 0):
        n_samples, uniques = X.shape[0], len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or uniques == 1:
            leaf_val = np.mean(y)
            return _LeafNode(value = leaf_val)
        
        split_feature, split_val = self._best_split(X, y)
        split_column = _to_numeric(X[:, split_feature])
        
        left_mask = split_column >= split_val if self.dtypes[split_feature] == 'numeric' else split_column == split_val
        right_mask = ~left_mask 
        
        X_left, X_right = X[left_mask], X[right_mask]
        y_left, y_right = y[left_mask], y[right_mask]
        
        left_node, right_node = self._grow_tree(X_left, y_left, depth + 1), self._grow_tree(X_right, y_right, depth + 1)
        return _DecisionNode(split_feature, split_val, left_node, right_node)
    
    
    def _best_split(self, X, y):
        n_features = X.shape[1]
        split_feature, split_val = None, None
        split_error = float('inf')
        
        for feature in range(n_features):
            cur_column = _to_numeric(X[:, feature])
            
            if self.dtypes[feature] == 'numeric':
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    x_sample = cur_column[start:end]
                    y_sample = y[start:end]
            
                    uniques = np.unique(x_sample)
                    thresholds = (uniques[1:] + uniques[:-1]) / 2
                    
                    for batch in range(0, len(thresholds), self.thresh_batch):
                        thresholds_batch = thresholds[batch: batch + self.thresh_batch]
                        
                        erros, thresholds_batch = self._mean_squared_errors(x_sample, y_sample, thresholds_batch, 'numeric')
                        min_error = np.argmin(errors)
                        
                        if len(errors) == 0:
                            continue
                        
                        if errors[min_error] < split_error:
                            split_error = errors[min_error]
                            split_feature, split_val = feature, thresholds_batch[min_error]
            else:
                uniques = np.unique(cur_column)
                
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    x_sample = cur_column[start:end]
                    y_sample = y[start:end]
                
                    for batch in range(0, len(uniques), self.thresh_batch):
                        uniques_batch = uniques[batch: batch + self.thresh_batch]
                        
                        erros, uniques_batch = self._mean_squared_errors(x_sample, y_sample, uniques_batch, 'categprical')
                        min_error = np.argmin(errors)
                        
                        if errors[min_error] < split_error:
                            split_error = errors[min_error]
                            split_feature, split_val = feature, uniques_batch[min_error]
                        
        return split_feature, split_val
    
    def _mean_squared_errors(self, X, y, thresholds, feature_dtype):
        masks = X[None ,:] >= thresholds[:, None] if feature_dtype == 'numeric' else X[None ,:] == thresholds[:, None]
        
        left_counts = np.sum(masks, axis = 1)
        right_counts = np.sum(~masks, axis = 1)
        
        valid_thresholds = (left_counts > 0) & (right_counts > 0)
        masks = masks[valid_thresholds]
        thresholds = thresholds[valid_thresholds]
        
        if len(masks) == 0:
            return np.array([]), np.array([])
        
        left_means = np.sum(y * masks, axis = 1) / np.sum(masks, axis = 1)
        right_means = np.sum(y * ~masks, axis = 1) / np.sum(~masks, axis = 1)
        
        y_preds = left_means[:, None] * masks + right_means[:, None] * ~masks
        errors = np.sum((y_preds - y) ** 2, axis = 1)
        
        return errors, thresholds
        
    
    def predict(self, X):
        """predict the target values for the given data X

        Args:
            X (array): the features array

        Returns:
            array: the preicted values from X
        """
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X, node):
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        