'''
Created on 04/11/2013

@author: Dani

The test data is taken from Coursera's Machine Learning Course (Andrew Ng)

'''

import ANN
import numpy as np

def debugInitializeWeights(inConnections,outConnections):
    '''
    Initialize the weights of a layer with fan_in 
    incoming connections and fan_out outgoing connections using a fixed 
    strategy. Debug purposes
    '''
    # add the bias term
    W = np.zeros((outConnections,inConnections + 1))
    W = np.array([np.sin(i+1) for i in xrange(W.size)]).reshape(W.shape,order='F') / 10.
    return W

def testGradient():
    '''
    Check if the gradient is calculated correctly
    '''
    input_layer_size = 3
    hidden_layer_size = 5
    num_labels = 3
    m = 5

    # generate some 'random' test data
    Theta1 = debugInitializeWeights(input_layer_size,hidden_layer_size)
    Theta2 = debugInitializeWeights(hidden_layer_size,num_labels)
    # Reusing debugInitializeWeights to generate X
    X  = debugInitializeWeights(input_layer_size - 1,m)
    y = np.array([1 + ((i + 1)%num_labels) for i in xrange(m)])
    
    print 'Theta 1'
    print Theta1
    
    print 'Theta 2'
    print Theta2
    
    print 'X'
    print X
    
    print 'y'
    print y

    # Add ones to the X data matrix
    X = np.hstack( (np.ones((m, 1)), X) )
    #Convert y 
    Y = np.zeros((m, num_labels));
    for i in xrange(m):
        Y[i,((y[i]-1)%num_labels)] = 1;
    y = Y;

    # Unroll parameters
    nn_params = np.concatenate((Theta1.flatten(),Theta2.flatten()),axis=2)
    
    results5 = [-9.2783e-003,8.8991e-003,-8.3601e-003,7.6281e-003,-6.7480e-003]
    
    J,grad = ANN.costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y)
    
    print grad[0:5],results5
    print grad


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

J,grad = ANN.costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y)

print 'this value should be about 0.287629', J

print 'Testing gradient'

testGradient()



    