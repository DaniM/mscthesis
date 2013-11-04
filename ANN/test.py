# The test data is taken from Coursera's Machine Learning Course (Andrew Ng)

## simple test to check everything is alright
import numpy as np
import LinearRegressionPerceptron
from ClassifierPerceptron import sigmoid, costFunction, gradientDescent
a = np.mat([[2,2],[2,2]],float)
b = np.ones((2,2))
# oprations test
print a * b
print np.multiply(a,b)

print 'Regression'

data = np.loadtxt(open("testfiles/test_data1.txt","rb"),delimiter=",")
X = data[:,:data.shape[1]-1]
m,n = X.shape
y = np.matrix(data[:,-1]).T

# add intercept term 
X = np.hstack((np.ones((m,1)), X))
initial_theta = np.zeros((n+1,1))

cost, grad = LinearRegressionPerceptron.costFunction(initial_theta, X, y)
print 'Cost at initial theta (zeros): ',cost

# lets solve with the built-in function linalg.lstsq(a, b, rcond=-1)
print 'Solving analitically (lstsq)'
solution = np.linalg.lstsq(X, y)
theta = solution[0]
h = np.dot(X,theta)
print np.hstack((h,y))

# another method, the normal eq
print 'Solving analitically (normal eq)'
Xinv = np.linalg.pinv( np.dot(X.T,X) )
theta = np.dot(np.dot( Xinv, X.T ),y)

h = np.dot(X,theta)
print np.hstack((h,y))


print 'Training linear regression perceptron'
history,theta = LinearRegressionPerceptron.gradientDescent(initial_theta, X, y, 0.01, 1e-10,1500)


print 'Final theta: ', theta
print 'Error func last steps: ', history[-5:]

print 'Classifier'

#test the sigmoid is working
a = np.eye(3)
print sigmoid(a)
print sigmoid(0)

data = np.loadtxt(open("testfiles/test_data2.txt","rb"),delimiter=",")
X = data[:,:data.shape[1]-1]
m,n = X.shape
y = np.matrix(data[:,-1]).T

# add intercept term 
X = np.hstack((np.ones((m,1)), X))
initial_theta = np.zeros((n+1,1))
#test if costFunction function is working
cost,grad = costFunction(initial_theta,X,y)
print 'Cost at initial theta (zeros): ',cost
print 'Gradient at initial theta (zeros): ',grad

print 'Training a simple perceptron'
# NOTE: because using scipy implies a bunch of libraries installed in your system, we'll do a gradient descent manually
# in case you have scipy installed use the fmin function

# gradient descent (little useless)
MaxIts = 1000000
alpha = 0.001
theta = initial_theta
history,theta = gradientDescent(theta, X, y, alpha, 1e-10, MaxIts)
print 'Final theta: ', theta
print 'Error func last steps: ', history[-5:]
