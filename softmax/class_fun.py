import struct
import numpy as np
from scipy import sparse

def read_images(file):
    with open(file, 'rb') as f:
        buf = f.read()
    fmt_header = '>IIII'
    offset = 0
    (magic, imgNum, rows, cols) = struct.unpack_from(fmt_header, buf, offset)
    img_size = rows*cols
    fmt_img = '>'+str(img_size)+'B'
    offset += struct.calcsize(fmt_header)
    images = np.empty([imgNum, img_size])
    for i in range(imgNum):
        img = struct.unpack_from(fmt_img, buf, offset)
        offset += img_size
        images[i] = np.array(img).reshape(1, -1)
    return images


def read_labels(file):
    with open(file, 'rb') as f:
        buf = f.read()
    fmt_header = '>II'
    offset = 0
    (magic, labNum) = struct.unpack_from(fmt_header, buf, offset)
    fmt_label = '>'+str(labNum)+'B'
    offset += struct.calcsize(fmt_header)
    labels = np.array(struct.unpack_from(fmt_label, buf, offset)).reshape([labNum, -1])
    return labels


def standard(images):
    (rows, cols) = images.shape
    mean = np.mean(images, axis=1).reshape([rows, -1])
    mean = np.repeat(mean, cols, axis=1)
    std = np.std(images, axis=1).reshape([rows, -1])+0.1
    std = np.repeat(std, cols, axis=1)
    images = (images-mean)/std
    images = np.c_[np.ones([rows, 1]), images]
    return images


def calculate(X, Y):
    K = 10  # 分类个数
    (rows, cols) = X.shape  # 60000, 785
    Y = sparse.coo_matrix((np.ones(rows), (np.arange(0,  rows), Y.reshape(rows,))), shape=(rows, K))

    theta = np.zeros([K, cols])
    cycle = 300
    alpha = 0.18
    for i in range(cycle):
        numerator = np.exp(X.dot(theta.T))
        (a, b) = numerator.shape
        denominator = np.repeat(np.sum(numerator, axis=1).reshape([a, 1]), b, axis=1)
        P = numerator/denominator
        J = -1/rows * (Y-P).T.dot(X)
        theta = theta - alpha*J
    return theta


def accurate(theta, images, labels):
    numerator = np.exp(images.dot(theta.T))
    (a, b) = numerator.shape
    denominator = np.repeat(np.sum(numerator, axis=1).reshape([a, 1]), b, axis=1)
    P = numerator / denominator
    Y = np.argmax(P, axis=1).reshape([P.shape[0], 1])

    accu = sum(Y == labels)/len(labels)

    return accu






