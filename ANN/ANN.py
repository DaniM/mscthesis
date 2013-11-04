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

    The vector y passed into the function is a vector of labels
    containing values from 1..K. You need to map this vector into a 
    binary vector of 1's and 0's to be used with the neural network
    cost function.
  
    The gradient is an "unrolled" vector of the partial derivatives of the neural network.
    '''
    m = X.shape[0]
    #Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
    #for our 2 layer neural network
    Theta1 = nnParams[0:hiddenLayerSize * (inputLayerSize + 1)].reshape( 
                (hiddenLayerSize, (inputLayerSize + 1)) )

    Theta2 = nnParams[(hiddenLayerSize * (inputLayerSize + 1)):].reshape(
                 (numLabels, (hiddenLayerSize + 1)) )
    
    # cost and grad 
    J = 0;
    Theta1_grad = np.zeros(Theta1.shape)
    Theta2_grad = np.zeros(Theta2.shape);
    
    # Feedforward the neural network and return the cost in the variable J
    a1 = X;
    z2 = np.dot(a1,Theta1.T)
    a2 = sigmoid(z2)
    #Add the ones
    a2 = np.hstack((np.ones((m,1)), a2))

    z3 = np.dot(a2 ,Theta2.T)
    a3 = h = sigmoid(z3);
    
    aux = np.sum(np.multiply(-y,np.log(h)) - np.multiply((1-y),np.log(1 - h)), axis=1)
    cost_term = (1./m)*sum(aux);
    J=cost_term;
    
    #backpropagation algorithm to compute the gradients Theta1_grad and Theta2_grad
    
    delta3 = a3 - y;
    z2 = np.hstack((np.ones((m,1)),z2));
    delta2 = np.multiply(np.dot(delta3, Theta2),sigmoidGrad(z2)) 
    delta2 = delta2[:,1:] # Do not get the column of ones we have just pushed
    Theta2_grad = (1./m) * (Theta2_grad + np.dot(delta3.T,a2));
    Theta1_grad = (1./m) * (Theta1_grad + np.dot(delta2.T,a1));
    grad = np.concatenate((Theta1_grad.flatten(order='F'),Theta2_grad.flatten(order='F')),axis=2);
    
    return J,grad

def sigmoid(x):
    y = np.exp(-x)
    return 1/(1 + y)

def sigmoidGrad(x):
    sig = sigmoid(x)
    return np.multiply(sig,(1-sig))