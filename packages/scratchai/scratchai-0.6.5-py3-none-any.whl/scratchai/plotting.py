import matplotlib.pyplot as plt
import numpy as np

def plot_loss_curve(model) -> plt.plot:
    """
    Plot the losses over the number of iterations

    Args:
        losses (array): the training losses
        itertions (array): the number of iterations/epochs
    """
    plt.plot(model.training_epochs, model.training_losses, color = 'red')
    plt.xlabel('Number of Iterations/Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Curve')
    plt.show()
    
def plot_generalization_curve(model) -> plt.plot:
    """
    Plot the traning losses and the testing losses over the number of iterations

    Args:
        traning_lossses (array): the training losses
        testing_losses (array): the testing losses
        iterations (array): the number of iterations/epochs
    """
    plt.plot(model.training_epochs, model.training_losses, color = 'red')
    plt.plot(model.training_epochs, model.validation_losses, color = 'blue')
    plt.legend(['Training', 'Validation'])
    plt.title('Generalization Curve')
    plt.show()