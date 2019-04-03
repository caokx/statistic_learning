import numpy as np
from SVD import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 读取图片为灰度图
img = mpimg.imread('butterfly.bmp')
img_gray = np.dot(img[..., :3], [0.299, 0.587, 0.114])

# 对灰度图进行svd分解
A = np.mat(img_gray)
U, sigma, V, count = get_svd(A)

# 画出奇异值占比曲线
a = np.sum(sigma)
b = np.zeros(count+1)
sum = 0
for i in range(1, count+1):
    sum = sum+sigma[i-1]
    b[i] = sum/a
plt.figure()
plt.plot(np.arange(0, count+1), b)
plt.xlabel("numbers")
plt.ylabel("rate")
plt.show()

# 选取奇异值
temp = 0
for i in [1, 10, 20, 50, 100, count]:
    u = U[:, 0:i]
    s = sigma[0:i]
    v = V[:, 0:i]
    P = u.dot(np.diag(s)).dot(v.T)
    temp += 1
    plt.subplot(2, 3, temp)
    plt.title(str(i))
    plt.imshow(P, cmap=plt.get_cmap('gray'))
plt.show()

