import  numpy as np
a = np.array([[1, 2, 3]])

b = np.r_[np.ones([1, a.shape[1]]), a]
print(b)
