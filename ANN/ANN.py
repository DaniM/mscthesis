'''
Created on 04/11/2013

@author: Dani
'''
import numpy as np

def costFunction(nnParams,inputLayerSize,hiddenLayerSize,numLabels,X,y):
    '''
    computes the cost and gradient of the neural network. The
    parameters for the neural network are "unrolled" into the vector
    nnParams and need to be converted back into the weight matrices. 
  
    The returned parameter grad should be a "unrolled" vector of the
    partial derivatives of the neural network.
    '''
    m = X.shape[0]
    #Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
    #for our 2 layer neural network
    Theta1 = nnParams[0:hiddenLayerSize * (inputLayerSize + 1)].reshape( 
                (hiddenLayerSize, (inputLayerSize + 1)) )

    Theta2 = nnParams[(1 + (hiddenLayerSize * (inputLayerSize + 1))):].reshape(
                 (numLabels, (hiddenLayerSize + 1)) )
    
    # cost and grad 
    J = 0;
    Theta1_grad = np.zeros(Theta1.shape)
    Theta2_grad = np.zeros(Theta2.shape);

def sigmoid(x):
    y = np.exp(-x)
    return 1/(1 + y)

def sigmoidGrad(x):
    sig = sigmoid(x)
    return np.multiply(sig,(1-sig))