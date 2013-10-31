## simple test to check everything is alright
import numpy as np
import ANN
from ANN import sigmoid, costFunction
a = np.mat([[2,2],[2,2]],float)
b = np.ones((2,2))
print a * b
print np.multiply(a,b)

#test the sigmoid is working
a = np.eye(3)
print sigmoid(a)
print sigmoid(0)

data = np.loadtxt(open("test_data.txt","rb"),delimiter=",")
X = data[:,:data.shape[1]-1]
m,n = X.shape
y = np.matrix(data[:,-1]).T

# add intercept term 
X = np.hstack((np.ones((m,1)), X))
initial_theta = np.zeros((n+1,1))
#test if costFunction function is working
cost,grad = costFunction(initial_theta,X,y)

print 'Training a simple perceptron'
# NOTE: because using scipy implies a bunch of libraries installed in your system, we'll do a gradient descent manually
# in case you have scipy installed use the fmin function

# gradient descent
MaxIts = 5000
alpha = 0.1
theta = initial_theta
for _ in xrange(MaxIts):
    cost,grad = costFunction(theta,X,y)
    theta = theta - (alpha * grad)
print theta, cost

h = sigmoid( np.dot(X,theta) )
print np.hstack((h,y))