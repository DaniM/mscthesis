'''
Created on 04/11/2013

@author: Dani

The test data is taken from Coursera's Machine Learning Course (Andrew Ng)

'''

import ANN
import numpy as np

#test if the sigmoid grad is working properly
print ANN.sigmoidGrad(0)
print ANN.sigmoidGrad(np.zeros((3,3)))

input_layer_size  = 400;  # 20x20 Input Images of Digits
hidden_layer_size = 25;   # 25 hidden units
num_labels = 10;          # 10 labels, from 1 to 10   
                          # (note that we have mapped "0" to label 10)

#load the precalculated weights to check cost function is working
theta1 = np.loadtxt(open("testfiles/Theta1.txt","rb"),delimiter=",")
theta2 = np.loadtxt(open("testfiles/Theta2.txt","rb"),delimiter=",")
X = np.loadtxt(open("testfiles/ann_test_data.txt","rb"),delimiter=",")
y = np.loadtxt(open("testfiles/ann_test_output.txt","rb"),delimiter=",")

m = X.shape[0]
# Add ones to the X data matrix
X = np.hstack( (np.ones((m, 1)), X) )
#Convert Y from a integer [0,9] to a vector[10]
#Because the test is taken from matlab and the indexes values are 1 based
#I'll make a little trick (move all values to the index value - 1 ) 
Y = np.zeros((m, num_labels));
for i in xrange(m):
    Y[i,((y[i]-1)%num_labels)] = 1;
y = Y;


nn_params = np.concatenate((theta1.flatten(),theta2.flatten()),axis=2)

print 'Testing cost function'

J = ANN.costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y)

print 'this value should be about 0.287629', J