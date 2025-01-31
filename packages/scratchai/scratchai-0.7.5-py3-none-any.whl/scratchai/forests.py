from joblib import Parallel, delayed
import numpy as np


from scratchai.trees import DecisionTreeClassifier

from typing import Optional, Tuple
from collections import defaultdict


class RandomForestClassifier:
    def __init__(self,
                n_trees: Optional[int] = 50,
                max_depth: Optional[int] = 16,
                min_samples_split: Optional[int] = 10):
        # Random forest parameters
        self.n_trees = n_trees
        self.max_features = 0
        
        # Forest trees parameters
        self.max_depth = max_depth
        self.min_samples_plit = min_samples_split
        
        # Forest trees
        self.trees = []
        
        # evaluation data
        self.oob_eval = False
        self.oob_score = 0.0
        
    def _get_bootstraped(self, X: np.ndarray, return_oob: Optional[bool] = False) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Randomly select n examples from X and keep track of out of bag examples."""
        n_samples = X.shape[0]
        
        # randomly select n_samples for X with replacement
        bootstraped = np.random.choice(n_samples, n_samples)
        if not return_oob:
            return bootstraped
        
        out_of_bag = ~np.isin(np.arange(n_samples), bootstraped)
        return bootstraped, out_of_bag
    
    def _build_tree(self, X: np.ndarray, y: np.ndarray) -> Tuple[DecisionTreeClassifier, Optional[np.ndarray]]:
        """Fit a tree to the given bootstraped data and return it."""
        # get bootstraped data
        if self.oob_eval:
            bootsraped, out_of_bag = self._get_bootstraped(X, return_oob = True)
        else:
            bootsraped = self._get_bootstraped(X)
            
        # fit a decision tree to the bootstraped data
        tree = DecisionTreeClassifier(max_depth = self.max_depth, min_samples_split = self.min_samples_plit)
        tree.fit(X[bootsraped], y[bootsraped], self.max_features)
        
        if not self.oob_eval:
            return tree
        
        # return the fited tree and its out of bag samples
        oob_idxs = np.arange(X.shape[0]) * out_of_bag
        return tree, oob_idxs
    
    def _build_forest(self, X: np.ndarray, y: np.ndarray) -> Tuple[list, Optional[int]]:
        """Build the random forest trees and cacluate the out of bag score if needed."""
        # build and save the forest decision trees
        if not self.oob_eval:
            return Parallel(n_jobs=-1)(delayed(self._build_tree)(X, y) for _ in range(self.n_trees))
        
        trees_data = Parallel(n_jobs=-1)(delayed(self._build_tree)(X, y) for _ in range(self.n_trees))
        
        # get the out of bag samples and calculate the oob score
        oob_samples = defaultdict(list)
        forest_trees = []
        
        for tree, oob_idxs in trees_data:
            forest_trees.append(tree)
            
            for idx in oob_idxs:
                if idx: oob_samples[idx].append(tree)
                
            
        oob_score = self._calculate_oob_score(X, y, oob_samples)
        return forest_trees, oob_score
        
    def _calculate_oob_score(self, X: np.ndarray, y: np.ndarray, oob_samples: defaultdict[list]) -> int:
        """Calculates the out of bag score."""
    
        def sample_error(sample):
            X_sample = X[sample][None ,:]
            y_sample = y[sample]
            
            pred = self._most_common_pred(X_sample, [tree for tree in oob_samples[sample]])
            return pred != y_sample
        
        oob_idxs = np.array(list(oob_samples.keys()))
        
        if len(oob_idxs) == 0:
            return 0.0
    
        oob_error = np.sum([sample_error(sample) for sample in oob_idxs])
        return oob_error / oob_idxs.shape[0]
        
    def fit(self, X: np.ndarray, y: np.ndarray, oob_eval: Optional[bool] = False):
        """Fit a random forest to the given data and evaluate it if needed.

        Args:
            X (np.ndarray): The input features array.
            y (np.ndarray): the target array.
            n_trees (Optional[int], optional): the number of the forest trees. Defaults to 50.
            oob_eval (Optional[bool], optional): cacluate the out of bag error. Defaults to False.
        """
        # initialize tree parameters
        n_features = X.shape[1]
        
        self.max_features = int(np.sqrt(n_features))
        self.oob_eval = oob_eval
        
        # build the random forest
        if oob_eval:
            trees, oob_score = self._build_forest(X, y)
            self.trees.extend(trees)
            self.oob_score = oob_score
        else:
            trees = self._build_forest(X, y)
            self.trees.extend(trees)
            
            
    def _most_common_pred(self, X: np.ndarray, trees: Optional[list] = None):
        """Get the agregation of trees predictions given X."""
        # set trees to the forest trees it not provided
        if not trees:
            trees = self.trees
            
        preds = np.array([tree.predict(X)[0] for tree in trees])
        uniques, counts = np.unique(preds, return_counts = True)
        return uniques[np.argmax(counts)]
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the target given X.

        Args:
            X (np.ndarray): the input features array.

        Returns:
            np.ndarray: the target array.
        """
        return np.array([self._most_common_pred(row[None ,:]) for row in X])