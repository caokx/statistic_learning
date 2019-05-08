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


class NN:
    def __init__(self, nn_str):
        self.layers = len(nn_str)
        self.weight = [np.random.randn(x, y) for x, y in zip(nn_str[:-1], nn_str[1:])]
        self.biases = [np.random.randn(1, y) for y in nn_str[1:]]

    def backprop(self, x, y):
        nabla_b = self.biases[:]
        nabla_w = self.weight[:]
        # forward pass
        a = []
        prime = []
        a.append(x)
        a_next = x
        for b, w in zip(self.biases, self.weight):
            a_next = sigmoid(a_next.dot(w)+b)
            a.append(a_next)
            prime.append(a_next*(1-a_next))

        # backward pass
        delta = (a[-1] - y) * prime[-1]
        nabla_b[-1] = np.ones((1, len(y))).dot(delta)/len(y)
        nabla_w[-1] = a[-2].T.dot(delta)/len(y)
        for i in range(self.layers-2, 0, -1):
            delta = delta.dot(self.weight[i].T)*prime[i-1]
            nabla_b[i-1] = np.ones((1, len(y))).dot(delta)/len(y)
            nabla_w[i-1] = a[i-1].T.dot(delta)/len(y)
        return nabla_b, nabla_w

    def gd_bp(self, step, alpha, x, y):
        for i in range(step):
            nabla_b, nabla_w = self.backprop(x, y)
            self.biases = [b - alpha*nb for b, nb in zip(self.biases, nabla_b)]
            self.weight = [w - alpha*nw for w, nw in zip(self.weight, nabla_w)]

    def forward(self, x):
        output = x
        for b, w in zip(self.biases, self.weight):
            output = sigmoid(output.dot(w) + b)
        return output

    def right_rate(self, x, yvec):
        output = self.forward(x)
        idx = output.argmax(1)
        rate = (idx == yvec).sum()/len(yvec)*100
        return rate

    def train(self, x, y, step, alpha):
        num_sample = y.shape[0]
        size_batch = 300
        num_batch = int(num_sample / size_batch)



        for i in range(num_batch):
            x_b = x[i*size_batch:((i+1)*size_batch), :]
            y_b = y[i*size_batch:((i+1)*size_batch), :]
            self.gd_bp(step, alpha, x_b, y_b)



