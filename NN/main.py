import fun as cf
import numpy as np
from scipy import sparse

if __name__ == '__main__':
    # 读取MNIST数据集
    file = 'train-images-idx3-ubyte'
    images = cf.read_images(file)
    test_file = 't10k-images-idx3-ubyte'
    test_images = cf.read_images(test_file)

    file_ = 'train-labels-idx1-ubyte'
    labels = cf.read_labels(file_)
    test_file_ = 't10k-labels-idx1-ubyte'
    test_labels = cf.read_labels(test_file_)

    # standardize操作，并在第一列加1
    images = cf.standard(images)
    test_images = cf.standard(test_images)

    # NN计算
    step = 20
    alpha = 2.1
    str = [784, 100, 10]
    nn = cf.NN(str)
    labels = sparse.coo_matrix((np.ones(60000), (np.arange(0,  60000), labels.reshape(60000,))), shape=(60000, 10)).toarray()
    nn.train(images, labels, step, alpha)
    test_labels = test_labels.flatten()
    test_rate = nn.right_rate(test_images, test_labels)
    print(test_rate)






