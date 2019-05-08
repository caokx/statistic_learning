import numpy as np
import class_fun as cf

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

    theta = cf.calculate(images, labels)

    accu = cf.accurate(theta, test_images, test_labels)
    print(accu)
