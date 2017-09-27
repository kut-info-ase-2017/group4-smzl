

import numpy as np

import chainer
import chainer.functions as F
from chainer import initializers
from chainer import Chain, Variable
import chainer.links as L

class AlexNet(chainer.Chain):

    """AlexNet without partition toward the channel axis."""

    insize = 120

    def __init__(self, n_out):
        super(AlexNet, self).__init__(
            conv1=L.Convolution2D(None,  96, 11, stride=4),
            conv2=L.Convolution2D(None, 256,  5, pad=2),
            conv3=L.Convolution2D(None, 384,  3, pad=1),
            conv4=L.Convolution2D(None, 384,  3, pad=1),
            conv5=L.Convolution2D(None, 256,  3, pad=1),
            fc6=L.Linear(None, 4096),
            fc7=L.Linear(None, 1024),
            fc8=L.Linear(None, n_out),
        )

    def __call__(self, x):
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv1(x))), 3, stride=2)
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv2(h))), 3, stride=2)
        h = F.relu(self.conv3(h))
        h = F.relu(self.conv4(h))
        h = F.max_pooling_2d(F.relu(self.conv5(h)), 3, stride=2)
        if chainer.config.train:
            h = F.dropout(F.relu(self.fc6(h)))
            h = F.dropout(F.relu(self.fc7(h)))
        else:
            h = F.relu(self.fc6(h))
            h = F.relu(self.fc7(h))
        h = self.fc8(h)
        return h

class VggFaceNet(chainer.Chain):
    '''definition of VggFaceNetwork from caffe model
    '''
    insize = 120
    channel = 3

    def __init__(self, n_out):
        super(VggFaceNet, self).__init__(
            conv1_1=L.Convolution2D(self.channel,  64, ksize=3, pad=1),
            conv1_2=L.Convolution2D(64, 64,  ksize=3, pad=1),
            conv2_1=L.Convolution2D(64, 128,  ksize=3, pad=1),
            conv2_2=L.Convolution2D(128, 128,  ksize=3, pad=1),
            conv3_1=L.Convolution2D(128, 256,  ksize=3, pad=1),
            conv3_2=L.Convolution2D(256, 256,  ksize=3, pad=1),
            conv3_3=L.Convolution2D(256, 256,  ksize=3, pad=1),
            conv4_1=L.Convolution2D(256, 512,  ksize=3, pad=1),
            conv4_2=L.Convolution2D(512, 512,  ksize=3, pad=1),
            conv4_3=L.Convolution2D(512, 512,  ksize=3, pad=1),
            my_conv5_1=L.Convolution2D(512, 512,  ksize=3, pad=1),
            my_conv5_2=L.Convolution2D(512, 512,  ksize=3, pad=1),
            my_conv5_3=L.Convolution2D(512, 512,  ksize=3, pad=1),
            my_fc6=L.Linear(8192, 1024),
            my_fc7=L.Linear(1024, 256),
            my_fc8=L.Linear(256, n_out),
        )

    def __call__(self, x):
        h = F.relu(self.conv1_1(x))
        h = F.max_pooling_2d(F.local_response_normalization(
                F.relu(self.conv1_2(h))), 2, stride=2)
        h = F.relu(self.conv2_1(h))
        h = F.max_pooling_2d(F.local_response_normalization(
                F.relu(self.conv2_2(h))), 2, stride=2)
        h = F.relu(self.conv3_1(h))
        h = F.relu(self.conv3_2(h))
        h = F.max_pooling_2d(F.local_response_normalization(
                F.relu(self.conv3_3(h))), 2, stride=2)
        h = F.relu(self.conv4_1(h))
        h = F.relu(self.conv4_2(h))
        h = F.max_pooling_2d(F.local_response_normalization(
                F.relu(self.conv4_3(h))), 2, stride=2)
        h = F.relu(self.my_conv5_1(h))
        h = F.relu(self.my_conv5_2(h))
        h = F.max_pooling_2d(F.local_response_normalization(
                F.relu(self.my_conv5_3(h))), 2, stride=2)
        h = F.dropout(F.relu(self.my_fc6(h)), ratio=0.5)
        h = F.dropout(F.relu(self.my_fc7(h)), ratio=0.5)
        h = self.my_fc8(h)

        return h
