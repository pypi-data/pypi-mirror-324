import numpy as np
from typing import Optional

import sys

class LinearRegression:
    def __init__(self):
        # model parameters
        self.w = None
        self.b = None
        
        # plotting data
        self.training_losses = []
        self.training_epochs = []
        self.validation_losses = []
        
    def _cost(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate the mean squared error given X and y."""
        y_pred = self.predict(X)
        return (1 / len(y)) * np.sum((y_pred - y) ** 2)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the target given the features array X.

        Args:
            X (np.ndarray): the features values array.

        Returns:
            np.ndarray: the target values array.
        """
            
        return np.dot(X, self.w) + self.b
    
    def _gradient_descent(self,
                        X: np.ndarray,
                        y: np.ndarray,
                        alpha: int,
                        epochs: int,
                        batch_size: int,
                        reg_rate: Optional[int] = 1,
                        X_valid: Optional[np.ndarray] = None, 
                        y_valid: Optional[np.ndarray] = None) -> None:
        """Update the model parameters using the gradient descent algorithm Given X and y."""
        
        m = len(y)
        for epoch in range(epochs):
            
            # shuffling the data before each epoch
            shuffled_indices = np.random.permutation(m)
            X_shuffled = X[shuffled_indices]
            y_shuffled = y[shuffled_indices]
            
            for batch in range(0, m, batch_size):
                # set the X batch and y batch
                X_batch = X_shuffled[batch : batch + batch_size]
                y_batch = y_shuffled[batch : batch + batch_size]
                y_pred = self.predict(X_batch)
                
                # calculate the gradient
                dw = (2 / X_batch.shape[0]) * np.dot(X_batch.T, (y_pred - y_batch))
                db = (2 / X_batch.shape[0]) * np.sum(y_pred - y_batch)
                
                # update the model parameters
                self.w -= alpha * dw
                self.b -= alpha * db
                
                # regularization
                if reg_rate:
                    self.w *= reg_rate
                
            # Storing the Loss and the epoch after each epoch to plot the loss curve
            training_loss= self._cost(X, y)
            validation_loss = self._cost(X_valid, y_valid) if X_valid is not None and y_valid is not None else 0
        
            self.validation_losses.append(validation_loss)
            self.training_losses.append(training_loss)
            self.training_epochs.append(epoch)
    
    def fit(self, 
            X: np.ndarray,
            y: np.ndarray,
            learning_rate: int,
            epochs: int,
            batch_size: int,
            reg_rate: Optional[int] = 1,
            X_valid: Optional[np.ndarray] = None, 
            y_valid: Optional[np.ndarray] = None) -> None:
        """Fit a Linear regression model to the given data.

        Args:
            X (np.ndarray): the features values array.
            y (np.ndarray): the target values array.
            learning_rate (int): the learning rate parameter.
            epochs (int): the number of training epochs.
            batch_size: (int): the batch size parameter.
            reg_rate (int): the regularization rate parameter.
            X_valid (np.ndarray): the features validation array.
            y_valid (np.ndarray): the target validation array.
        """  
        # initialing model params
        self.w = np.zeros(X.shape[1])
        self.b = 0
        
        self._gradient_descent(X, y, learning_rate, epochs, batch_size, reg_rate, X_valid, y_valid)

class LogisticRegression:
    def __init__(self):
        # model parameters
        self.w = None
        self.b = None
        self.threshold = 0.5
        
        # ploting data
        self.training_losses = []
        self.validation_losses = []
        self.traning_epochs = []
            
    def _sigmoid(self, z: float) -> float:
        """Returns the sigmoid out for z."""
        return 1 / (1 + np.exp(-z))
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the probabilites given the features array X.

        Args:
            X (np.ndarray): the features values array.

        Returns:
            np.ndarray: the probabilites array.
        """               
        z = np.dot(X, self.w) + self.b
        return self._sigmoid(z)
    
    def classifie(self, X: np.ndarray) -> np.ndarray:
        """Classifie the given examples in X.

        Args:
            X (np.ndarray): The features values array.

        Returns:
            np.ndarray: the predicted classes array.
        """
        y_pred = self.predict(X)
        y_pred[y_pred > self.threshold] = 1
        y_pred[y_pred <= self.threshold] = 0
        return y_pred
    
    def _cost(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        calculates the model cost.

        Args:
            X (array): the input features
            y (array): the target/label

        Returns:
            int: the calculated model cost.
        """
        total_cost = 0
        batch_size = 100
        
        for i in range(0, len(y), batch_size):
            X_batch = X[i: i + batch_size]
            y_batch = y[i: i + batch_size]
            y_pred_batch = self.predict(X_batch)
            
            total_cost += np.sum(-y_batch * np.log(y_pred_batch) - (1 - y_batch) * np.log(1 - y_pred_batch))
            
        return total_cost / len(y)
    
    def _gradient_descent(self,
                        X: np.ndarray,
                        y: np.ndarray,
                        alpha: int,
                        epochs: int,
                        batch_size: int,
                        reg_rate: Optional[int] = 1,
                        X_valid: Optional[np.ndarray] = None, 
                        y_valid: Optional[np.ndarray] = None) -> None:
        """Update the model parameters using the gradient descent algorithm Given X and y."""
        m = len(y)
        
        for epoch in range(epochs):
            # shuffle the data after each epoch
            shuffled_indices = np.random.permutation(m)
            X_shuffled = X[shuffled_indices]
            y_shuffled = y[shuffled_indices]
            
            for batch in range(0, m, batch_size):
                # get X batch and y batch from the shuffled data
                X_batch = X_shuffled[batch: batch + batch_size] 
                y_batch = y_shuffled[batch: batch + batch_size]
                y_pred = self.predict(X_batch)
                
                # calculating the gradeint
                dw = (1 / batch_size) * np.dot(X_batch.T, (y_pred - y_batch))
                db = (1 / batch_size) * np.sum(y_pred - y_batch)
                
                # update the parameters in the opposite direction of the gradient
                self.w -= alpha * dw
                self.b -= alpha * db
                
                # regularization
                if reg_rate:
                    self.w *= reg_rate
                
            # save the loss after each epoch            
            training_loss = self._cost(X, y)
            validation_loss = self._cost(X_valid, y_valid) if X_valid is not None and y_valid is not None else 0
            
            self.validation_losses.append(validation_loss)
            self.training_losses.append(training_loss)
            self.traning_epochs.append(epoch)
    
    def fit(self, 
            X: np.ndarray,
            y: np.ndarray,
            learning_rate: int,
            epochs: int,
            batch_size: int,
            reg_rate: Optional[int] = 1,
            X_valid: Optional[np.ndarray] = None, 
            y_valid: Optional[np.ndarray] = None) -> None:
        """
        fit the logistic regression model using the gradient descent algorithm

        Args:
            X (array): features
            y (array): target
            learning_rate (int): learning rate
            batch_size (int): batch size
            epochs (int): number of traning epochs
            X_valid (array, optional): validation data to caclulate the validation losses. Defaults to None.
            y_valid (array, optional): validation data to caclulate the validation losses. Defaults to None.
        """
        # initialize the model parameters
        self.w = np.zeros(X.shape[1])
        self.b = 0
         
        self._gradient_descent(X, y, learning_rate, epochs, batch_size, reg_rate, X_valid, y_valid)