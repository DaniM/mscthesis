'''
Created on 02/11/2013

@author: Dani

Example taken from 'Varieties of Learning' (Richard Evans) of the book AI Game Programming Wisdom
'''
import numpy as np
from ClassifierPerceptron import sigmoid, costFunction, gradientDescent

data = np.loadtxt(open("testfiles/eating_events.txt","rb"),delimiter=",")

X = data[:,:data.shape[1]-1]
m,n = X.shape
y = np.matrix(data[:,-1]).T

# add bias term 
X = np.hstack((np.ones((m,1)), X))
theta = np.array([1,0.5,0.5,0.5],).reshape((4,1))
alpha = 0.1

# do a step by step like AI wisdom
actual = np.dot(X[0].reshape((1,n+1)),theta)
print 'Actual: ', actual
print 'Intended: ',y[0]
cost,grad = costFunction(theta, X[0].reshape((1,n+1)), y[0])
print cost,grad

theta = theta - (alpha * grad)
print 'New Theta ', theta
print 'Actual: ', actual
print 'Intended: ',y[0]
cost,grad = costFunction(theta, X[1].reshape((1,n+1)), y[1])
print cost,grad

theta = theta - (alpha * grad)
cost,grad = costFunction(theta, X[2].reshape((1,n+1)), y[2])
print cost,grad

theta = theta - (alpha * grad)
cost,grad = costFunction(theta, X[3].reshape((1,n+1)), y[3])
print cost,grad

theta = theta - (alpha * grad)
cost,grad = costFunction(theta, X[4].reshape((1,n+1)), y[4])
print cost,grad

theta = theta - (alpha * grad)
print 'Theta:', theta

# memory tab results
print 'Results of the example written in the msc thesis'
theta = np.array([1,0.5,0.5,0.5],).reshape((4,1))
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)
print 'Theta: ',theta
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)
print 'Theta: ',theta
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)
print 'Theta: ',theta
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)
print 'Theta: ',theta
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)
print 'Theta: ',theta

# batch
theta = np.array([1,0.5,0.5,0.5],).reshape((4,1))
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, 1)

print 'Theta: ',theta
print 'History: ',history