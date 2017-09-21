# coding: utf-8

import pickle
import chainer
import net


def copy_model(src, dst):
    '''copy parameter of source model(caffe) to that of destination model(chainer)
    '''
    assert isinstance(src, chainer.link.Chain)
    assert isinstance(dst, chainer.link.Chain)
    for child in src.children():
        if child.name not in dst.__dict__: continue
        dst_child = dst[child.name]
        if type(child) != type(dst_child): continue
        if isinstance(child, chainer.link.Chain):
            copy_model(child, dst_child)
        if isinstance(child, chainer.link.Link):
            match = True
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                if a[0] != b[0]:
                    match = False
                    break
                if a[1].data.shape != b[1].data.shape:
                    match = False
                    break
            if not match:
                print('Ignore %s because of parameter mismatch' % child.name)
                continue
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                b[1].data = a[1].data
            print('Copy %s' % child.name)


# copy parameter of caffe model to chainer model
src_model = pickle.load(open('vgg_face.chainermodel', 'rb'))
dst_model = net.Vgg_face(4)
copy_model(src_model, dst_model)
chainer.serializers.save_npz('caffePrams_copied_forChainer.model', dst_model)
