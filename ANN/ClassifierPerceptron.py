'''
Created on 30/10/2013

@author: Daniel

Just some functions used for a basic perceptron
The objectives for this module is to introduce perceptron as matrices
and consequently a little introduction for numpy
'''
import numpy as np

def sigmoid(x):
    y = np.exp(-x)
    return 1/(1 + y)

def costFunction(theta,X,y):
    J=0 # costFunction
    grad = np.zeros(theta.shape) # gradient
    m,n = X.shape
    # Implementation notes: we could have used * here and there but to make sure lets just use dot
    h = sigmoid( np.dot( X, theta ) ) # hypothesis
    # do some dirty tricks to avoid NaN
    #h = np.where(h==0,1e-10,h)
    #h = np.where(h==1,1. - 1e-10,h)
    aux = np.dot(-y.T,np.log(h)) - np.dot((1-y).T,np.log(1-h))
    # sum it just to have a single number and not a 1x1 matrix
    J = (1./m) * np.sum(aux)
    grad = (1./m) * np.dot(X.T,(h - y))
    return J,grad

def gradientDescent(theta,X,y,alpha,error,maxIts):
    '''Basic implementation of a gradient descent'''
    history = np.zeros((maxIts,1))
    for i in xrange(maxIts):
        cost,grad = costFunction(theta,X,y)
        theta = theta - (alpha * grad)
        history[i] = cost
        if abs(cost) < error :
            break
    return (history,theta)

if __name__ == '__main__':
    pass