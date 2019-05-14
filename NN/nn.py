import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def derivative(x):
    return x*(1-x)

X = np.array([[0.35, 0.9]])
Y = np.array([[0.5]])

W1 = np.array([[0.1, 0.7], [0.8, 0.6]])
W2 = np.array([[0.3], [0.9]])

for i in range(10000):
    L0 = X

    Z1 = L0.dot(W1)
    L1 = sigmoid(Z1)

    Z2 = L1.dot(W2)
    L2 = sigmoid(Z2)

    L2_delta = (L2-Y)*derivative(L2)
    W2_derivative = L1.T.dot(L2_delta)

    L1_delta = L2_delta.dot(W2.T)*derivative(L1)
    W1_derivative = L0.T.dot(L1_delta)

    W1 = W1-W1_derivative
    W2 = W2-W2_derivative

#print(W2)
Error = 1 / 2.0 * (Y-L2)**2
print(W2)


