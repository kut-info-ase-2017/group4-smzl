# coding: utf-8

import numpy as np

import chainer
import chainer.functions as F
from chainer import initializers
from chainer import Chain, Variable
import chainer.links as L

class Vgg_face(chainer.Chain):
    '''network definition of the caffe model
    '''
    insize = 120
    channel = 3

    def __init__(self, n_out):
        super(Vgg_face, self).__init__(
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
            my_fc6=L.Linear(8192, 4096),
            my_fc7=L.Linear(4096, 4096),
            my_fc8=L.Linear(4096, n_out),
        )
        self.train = True

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
