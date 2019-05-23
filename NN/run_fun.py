import struct
import numpy as np

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
    # images = np.c_[np.ones([rows, 1]), images]
    return images


def sigmoid(x):
    return 1/(1+np.exp(-x))

class NN(object):
    def __init__(self, parameters_list, X):
        self.layers = len(parameters_list)
        self.weights = [np.random.randn(x+1, y) for (x, y) in zip(parameters_list[:-1], parameters_list[1:])
        self.X = np.r_[np.ones([1, X.shape[1]]), X]


    def forward(self):
        A = []
        A[0] = self.X.dot(self.weights[0])
        A[1] = np.r_[np.ones([1, A[0].shape[1]]), sigmoid(A[0])].dot(self.weights[1])
        return A





