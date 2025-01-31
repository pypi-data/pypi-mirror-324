import numpy as np

from typing import Callable, Optional
import sys

from ._activation import _Activation, Linear, ReLU, Sigmoid, SoftMax

class Layer:
    def __init__(self,
                n_input: int, 
                n_outpot: int, 
                activation: Callable[[np.ndarray], np.ndarray], 
                dActivation: Callable[[np.ndarray], np.ndarray]):
        
        # Initialize the layer parameters using Xavier's initialization
        self.weights = np.random.normal(0, np.sqrt(2 / (n_input + n_outpot)), (n_input, n_outpot))
        self.biases = np.zeros((1, n_outpot))
        
        # Setup the layer activation function and its derivative
        self.activation = activation
        self.dActivation = dActivation
        
        # Initilize the layer activation and linear transfomration
        self.Z = None
        self.A = None
        
    def get_activation(self, X: np.ndarray):
        # Save the layer linear transformation and its activation
        self.Z = np.dot(X, self.weights) + self.biases
        self.A = self.activation(self.Z)
        
        # returns the layer activation
        return self.A
        
    def optimize(self, 
                pdz: np.ndarray, pw: np.ndarray, 
                nA: np.ndarray, 
                a: float, 
                clip_gradients: Optional[bool] = False,
                dz: Optional[np.ndarray] = None):
        # Compute the gradient
        if dz is None:
            dz = np.dot(pdz, pw.T) * self.dActivation(self.Z)
        dw, db = np.dot(nA.T, dz), np.sum(dz, axis = 0, keepdims = True)
        
        # Clip the gradient if needed
        if clip_gradients:
            dw, db = np.clip(dw, -1, 1), np.clip(db, -1, 1)
        
        # Update the layer parameters
        self.weights -= (a * dw)
        self.biases -= (a * db)
        
        # To compute the next layer gradient
        return dz, self.weights

class HiddenLayer(Layer):
    def __init__(self, 
                n_input: int, 
                n_outpot: int, 
                activation: _Activation):
        super().__init__(n_input, n_outpot, 
                        activation = activation().func, 
                        dActivation = activation().dfunc)
        
        self.type = 'HiddenLayer'
        
    def optimize(self, 
                pdz: np.ndarray, 
                pw: np.ndarray, 
                nA: np.ndarray,
                a: float, 
                clip_gradients: Optional[bool] = False):
        return super().optimize(pdz, pw, nA, a, clip_gradients, dz = None)
    
class LinearOutpotLayer(Layer):
    def __init__(self, 
                n_input: int, 
                n_outpot: int):
        
        # Setup the Layer
        super().__init__(n_input, n_outpot, 
                        activation = Linear().func, 
                        dActivation = Linear().dfunc)
        
    def optimize(self, 
                pdz: np.ndarray, 
                pw: np.ndarray, 
                nA: np.ndarray,
                a: float, 
                clip_gradients: Optional[bool] = False):
        return super().optimize(pdz, pw, nA, a, clip_gradients, dz = pdz)
    
class ReLUOutpotLayer(Layer):
    def __init__(self, 
                n_input: int, 
                n_outpot: int):
        super().__init__(n_input, n_outpot, 
                        activation = ReLU().func, 
                        dActivation = ReLU().dfunc)
        
    def optimize(self, 
                pdz: np.ndarray, 
                pw: np.ndarray, 
                nA: np.ndarray,
                a: float, 
                clip_gradients: Optional[bool] = False):
        
        # Compute the the partial derivative of Loss function
        # with respect the the layer linear transfomration
        dz = pdz * self.dActivation(self.Z)
        return super().optimize(pdz, pw, nA, a, clip_gradients, dz = dz)
    
class SigmoidOutpotLayer(Layer):
    def __init__(self, 
                n_input: int, 
                n_outpot: int):
        super().__init__(n_input, n_outpot, 
                        activation = Sigmoid().func, 
                        dActivation = Sigmoid().dfunc)
        
    def optimize(self, 
                pdz: np.ndarray, 
                pw: np.ndarray, 
                nA: np.ndarray,
                a: float, 
                clip_gradients: Optional[bool] = False):
        return super().optimize(pdz, pw, nA, a, clip_gradients, dz = pdz)

class SoftmaxOutpotLayer(Layer):
    def __init__(self, 
                n_input: int, 
                n_outpot: int):
        super().__init__(n_input, n_outpot, 
                        activation = SoftMax().func, 
                        dActivation = SoftMax().dfunc)
    def optimize(self, 
                pdz: np.ndarray, 
                pw: np.ndarray, 
                nA: np.ndarray,
                a: float, 
                clip_gradients: Optional[bool] = False):
        return super().optimize(pdz, pw, nA, a, clip_gradients, dz = pdz)
