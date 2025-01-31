import numpy as np

from typing import Callable

import sys

class _Activation:
    def __init__(self, 
                func: Callable[[np.ndarray], np.ndarray], 
                dfunc: Callable[[np.ndarray], np.ndarray]):
        self.func = func
        self.dfunc = dfunc
        
class Linear(_Activation):
    def __init__(self):
        super().__init__(func = lambda X: X, dfunc = lambda X: X)
        
class ReLU(_Activation):
    def __init__(self):
        
        def relu(X: np.ndarray):
            return np.array([np.where(row >= 0, row, 0) for row in X])
        
        def drelu(X: np.ndarray):
            return np.array([np.where(row >= 0, 1, 0) for row in X])
        
        super().__init__(func = relu, dfunc = drelu)
        
class SoftPlus(_Activation):
    def __init__(self):
        def softplus(X: np.ndarray):
            return np.log(1 + np.exp(X))
        
        def dsoftplus(X: np.ndarray):
            expX = np.exp(X)
            return expX / (1 + expX)
        
        super().__init__(func = softplus, dfunc = dsoftplus)
        
class Sigmoid(_Activation):
    def __init__(self):
        
        def sigmoid(X: np.ndarray):
            return 1 / (1 + np.exp(-X))
        
        def dsigmoid(X: np.ndarray):
            y = sigmoid(X)
            return y * (1 - y)
        
        super().__init__(func = sigmoid, dfunc = dsigmoid)

class Tanh(_Activation):
    def __init__(self):
        def tanh(X: np.ndarray):
            return np.tanh(X)
        
        def dtanh(X: np.ndarray):
            return 1 - (np.tanh(X) ** 2)
        
        super().__init__(func = tanh, dfunc = dtanh)
        
class SoftMax(_Activation):
    def __init__(self):
        def softmax(X: np.ndarray):
            Xexp = np.exp(X - np.max(X, axis = 1, keepdims = True))
            expSum = np.sum(Xexp, axis = 1, keepdims = True)
            return Xexp / expSum
        
        def dsoftmax(X: np.ndarray):
            def Jacobian(Z: np.ndarray):
                return np.diag(Z) - np.outer(Z, Z)
            
            Z = softmax(X)
            dZ = np.apply_along_axis(Jacobian, 1, Z)
            return np.sum(dZ, axis = -1) if dZ.ndim == 3 else dZ
        
        super().__init__(func = softmax, dfunc = dsoftmax)
        