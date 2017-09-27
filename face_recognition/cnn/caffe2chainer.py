#!/usr/bin/env python
from __future__ import print_function
import sys
from chainer.links.caffe import CaffeFunction
import pickle

if __name__ == '__main__':
    param = sys.argv
    if (len(param) != 3):
        print ("Usage: $ python " + param[0] + " modelname.caffemodel chainermodel.pkl")
        quit()

    print('Loading Caffe model file %s...' % param[1], file=sys.stderr)
    model = CaffeFunction(param[1])
    print('Loaded', file=sys.stderr)

    print('Converting from Caffe to Chainer model file %s...' % param[2], file=sys.stderr)
    pickle.dump(model, open(param[2], 'wb'), -1)
    print('Convert is done')
