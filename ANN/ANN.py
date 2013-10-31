'''
Created on 30/10/2013

@author: Dani
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
    
    #do some checking to avoid NaN
    
    aux = np.dot(-y.T,np.log(h)) - np.dot((1-y).T,np.log(1-h))
    # sum it just to have a single number and not a 1x1 matrix
    J = (1./m) * np.sum(aux)
    grad = (1./m) * np.dot(X.T,(h - y))
    return J,grad

if __name__ == '__main__':
    pass