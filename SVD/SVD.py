import numpy as np


# SVD函数
def get_svd(A):
    (u1, u2) = np.linalg.eig(A.dot(A.T))
    index1 = u1.argsort()[::-1]
    u1 = u1[index1]
    u2 = u2[:, index1]

    sigma = np.power(u1, 0.5)

    count = len(sigma > 0)

    U = u2[:, 0:count]
    V = A.T.dot(U).dot(np.diag(1/sigma))

    return U, sigma, V, count
