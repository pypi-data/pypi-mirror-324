import numpy as np

from ._block import Layer
from ._loss import _mse, _dmse, _bce, _cce, _dce

from typing import Callable, Optional, Literal, Tuple
import sys


class _NetworkBasedModel:
    def __init__(self, 
                layers: list[Layer],
                loss: Callable[[np.ndarray, np.ndarray], np.ndarray],
                dLoss: Callable[[np.ndarray, np.ndarray], np.ndarray]):
        # Initialize the model layers
        self.layers = layers
        
        # Initialize the modell loss and its derivative 
        self.loss = loss
        self.dLoss = dLoss
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Get the model predictions for the set of examples X.

        Args:
            X (np.ndarray): The set of examples.
        """
        y = X
        for layer in self.layers: y = layer.get_activation(y)
        return y
    
    def _backpropagate(self, 
                       X: np.ndarray,
                       y: np.ndarray,
                       a: float,
                       clip_gradient: Optional[bool] = False) -> None:
        """Optimize the model parameters using backpropagation.

        Args:
            X (np.ndarray): the set of examples
            y (np.ndarray): the labels
            a (float): the learning rate
            clip_gradient (Optional[bool], optional): clip gradient values during optimization if True. Defaults to False.
        """
        # Calculate the partial derivative of the loss
        # with respect to the predicted values
        y_pred = self.predict(X)
        dy = self.dLoss(y, y_pred)
        
        # Optimize the model layers parameters
        pdz, pw = dy, None
        for i in range(len(self.layers) - 1, -1, -1):
            # Get the previons layer activation
            A = self.layers[i - 1].A if i > 0 else X
            pdz, pw = self.layers[i].optimize(pdz, pw, A, a, clip_gradient)
            
    def fit(self,
            X: np.ndarray,
            y: np.ndarray,
            lr: float,
            batch_size: Literal[1, 16, 32, 64,
            128, 258, 512, 1024],
            epochs: int,
            clip_gradient: Optional[bool] =  False) -> Tuple[np.ndarray, np.ndarray]:
        """Fit the model to the given data.

        Args:
            X (np.ndarray): The set of examples
            y (np.ndarray): The labels
            lr (float): The training learning ratee
            batch_size (Literal[1, 16, 32, 64, 128, 258, 512, 1024]): The training batch size
            epochs (int): The number of training epochs
            clip_gradient (Optional[bool], optional): Clip gradients during Optimization if True. Defaults to False.

        Returns:
            np.ndarray: The training losses and epochs.
        """
        
        m = len(y)
        
        # Ploting data
        training_epochs = []
        training_losses = []
        
        for epoch in range(epochs):
            
            # Shuffle the data before each epoch
            mask = np.random.permutation(m)
            X_shuffled = X[mask]
            y_shuffled = y[mask]
            
            # Process the data in mini bacths & Optimize the model parameters
            for start in range(0, m, batch_size):
                end = min(start + batch_size, m)
                X_batch = X_shuffled[start:end]
                y_batch = y_shuffled[start:end]
                
                self._backpropagate(X_batch, y_batch, lr, clip_gradient)
                
            # Save the Loss after each epoch
            y_pred = self.predict(X)
            loss = self.loss(y, y_pred)
            
            training_epochs.append(epoch)
            training_losses.append(loss)
            
        # Return the ploting Data
        return training_losses, training_epochs

LOSS_FUNCTIONS = {
    'mse': {'loss': _mse, 'dLoss': _dmse},
    'bce': {'loss': _bce, 'dLoss': _dce},
    'cce': {'loss': _cce, 'dLoss': _dce}
}

MODELS = {
    'NetworkBasedModel': _NetworkBasedModel
}

def build_model(
    model: Literal['NetworkBasedModel'],
    loss: Literal['mse', 'bce', 'cce'],
    layers: Optional[list[Layer]]
):
    # Handle when the loss or model is not found
    if loss not in LOSS_FUNCTIONS or model not in MODELS:
        raise ValueError(f"{model} | {loss} is not found")
    
    # get the corresponding loss function and its derivative
    loss, dLoss = LOSS_FUNCTIONS[loss]['loss'], LOSS_FUNCTIONS[loss]['dLoss']
    
    # build the model and returns it
    return MODELS[model](layers, loss, dLoss)