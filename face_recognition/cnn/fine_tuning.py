#!/usr/bin/env python
# coding:utf-8

from __future__ import print_function
import sys
from chainer.links.caffe import CaffeFunction

import argparse
import numpy as np
from PIL import Image
import glob

import pickle
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.serializers
from chainer.datasets import tuple_dataset
from chainer import Chain, Variable, optimizers
from chainer import training
from chainer.training import extensions
import re

import net
import image2TrainAndTest


from chainer import cuda
class DelGradient(object):
    name = 'DelGradient'
    def __init__(self, delTgt):
        self.delTgt = delTgt

    def __call__(self, opt):
        for name,param in opt.target.namedparams():
            for d in self.delTgt:
                if d in name:
                    grad = param.grad
                    with cuda.get_device(grad):
                        grad = 0


# class FaceRecognizer_oxfordModel():
#     """docstring for ."""
#     def __init__(self, pickle_path):
#         with open(pickle_path, 'rb') as f:
#             self.model = pickle.load(f)
#     def __call__(self):

def main():
    parse = argparse.ArgumentParser(description='face detection train')
    parse.add_argument('--batchsize','-b',type=int, default=64,
                       help='Number if images in each mini batch')
    parse.add_argument('--epoch','-e',type=int, default=100,
                       help='Number of sweeps over the dataset to train')
    parse.add_argument('--gpu','-g',type=int, default=-1,
                       help='GPU ID(negative value indicates CPU')
    parse.add_argument('--out','-o', default='result',
                       help='Directory to output the result')
    parse.add_argument('--resume','-r', default='',
                       help='Resume the training from snapshot')
    parse.add_argument('--unit','-u', type=int, default=1000,
                       help='Number of units')
    parse.add_argument('--model','-m', default='caffePrams_copied_forChainer.model')
    parse.add_argument('--optimizer','-O', default='')
    parse.add_argument('--size','-s', type=int, default=128,
                       help='image size')
    parse.add_argument('--path','-p', default='')
    parse.add_argument('--channel','-c', default=3)
    parse.add_argument('--caffemodelpath','-cmp', default="")

    args = parse.parse_args()

    print('GPU: {}'.format(args.gpu))
    print('# unit: {}'.format(args.unit))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('')

    # データ取得
    train, test = image2TrainAndTest.load()

    # モデルの準備 （caffeモデルをchainerモデルへのコピーは事前に済ませている）
    model = net.Vgg_face(4)
    chainer.serializers.save_npz(args.model, model)

    ### something must be done here

    model = L.Classifier(model)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    # 重みを固定（学習させない）
    optimizer.add_hook(DelGradient(['conv1_1', 'conv1_2', 'conv2_1', 'conv2_2', 'conv3_1', 'conv3_2', 'conv3_3', 'conv4_1', 'conv4_2', 'conv4_3']))

    # get iterator of train and test
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)

    updater = training.StandardUpdater(train_iter, optimizer, device=args.gpu)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)

    trainer.extend(extensions.Evaluator(test_iter, model, device=args.gpu))
    trainer.extend(extensions.dump_graph('main/loss'))
    trainer.extend(extensions.LogReport(trigger=(1, 'epoch'), log_name="log"))
    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'validation/main/loss',
         'main/accuracy', 'validation/main/accuracy']))
    trainer.extend(extensions.ProgressBar())
    trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))

    trainer.run()

    outputname = "vgg_face" + str(len(pathsAndLabels))
    modelOutName = outputname + ".model"
    OptimOutName = outputname + ".state"

    chainer.serializers.save_npz(modelOutName, model)
    chainer.serializers.save_npz(OptimOutName, optimizer)

if __name__ == '__main__':
    main()
