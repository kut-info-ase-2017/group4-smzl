# coding: utf-8

import os
FILE_PATH = os.path.dirname(__file__)
if len(FILE_PATH) == 0:
    FILE_PATH = ''
else:
    FILE_PATH += '/'

import cv2
from PIL import Image
import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import Variable


import sys
sys.path.append(FILE_PATH + 'cnn')
from net_model import AlexNet
from net_model import VggFaceNet
from image2TrainAndTest import image2TrainAndTest
from image2TrainAndTest import getValueDataFromPath
from image2TrainAndTest import getValueDataFromImg



class CNN_FaceRecognizer():
    '''This class recognize human face using like alex net
    '''
    def __init__(self, neural_net, model):
        '''
        @param neural_net: class of defined neural network
        @param model: path of model file
        '''
        # extract number of classes from model's file name
        # file name of model is 'XXX_[class num].YYY'
        outNumStr = model.split(".")[0].split("_")
        outnum = int(outNumStr[ len(outNumStr)-1 ])
        self.model = L.Classifier(neural_net(outnum))
        chainer.serializers.load_npz(model, self.model)

        # get labels
        self.label2user_dict = [""] * outnum
        for line in open(FILE_PATH +'whoiswho.txt', 'r'):
            user = line.split(",")[0]
            label = line.split(",")[1]
            self.label2user_dict[int(label)] = user

    def predict(self, img):
        '''Predict the human identification from image
        @param img: a face image of 3 channels
        @return user identification
        '''
        user, prob = '', 0.0
        pil_img = self._cv2pil_converter(img)
        valData = getValueDataFromImg(pil_img)
        # pred = alexLike.predict(self.model, valData)

        with chainer.no_backprop_mode(), chainer.using_config('train', False):
            x = Variable(valData)
            y = F.softmax(self.model.predictor(x.data[0]))
        pred =  [i for i in y.data[0]]

        predR = np.round(pred, 2)
        tmp = predR.tolist()
        prob = max(tmp)
        idx = tmp.index(prob)
        user = self.label2user_dict[idx]

        print('probability of {} is {:.2f}'.format(user, prob))
        # 認識確率 0.9未満は unknownとする
        if prob < 0.9:
            user = 'unknown'
        return user

    def _cv2pil_converter(self, cv_img):
        '''Transform from BGR to RGB.
        @param cv_img: opencv image chanel of which is BGR
        @return pil_img: PIL image channel of which is RGB
        '''
        pil_img = None
        cv_img_RGB = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # cv_img_RGB = cv_img[::-1, :, ::-1].copy()
        cv2.flip(cv_img_RGB, 0)
        pil_img = Image.fromarray(cv_img_RGB)
        return pil_img


class Eigen_FaceRecognizer():
    '''This class recognize human face and predicts identification from movie.
    '''

    def __init__(self, init_model, user_dict, threshold=85):
        '''
        @param cascade_path: this file is used for face detection.
        @param init_model: serialized model path which has been aleady learned.
        @param user_dict: dictionary object(key:user name, value:numerical label).
        '''

        self.user_dict = user_dict
        self.rev_user_dict = {v:k for k,v in user_dict.items()}
        self.recognizer = cv2.face.createLBPHFaceRecognizer()
        self.recognizer.load(init_model)
        self.threshold=threshold


    def predict(self, img):
        '''Predict the human identification from movie.
        @return human_name predicted human's name
        '''
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # recognition
        predicted, confidence = self.recognizer.predict(img)

        print(confidence)
        user = ''
        if confidence > self.threshold:
            user = 'unknown'
        else:
            # find predicted human identification
            user = self.rev_user_dict[predicted]
            cv2.imshow("user", img)
        return user

import sys
import camera
if __name__ == '__main__':

    if len(sys.argv) == 1:
        raise Exception('引数指定してください[eigen or alexnet or vggfacenet]')

    recognizer = None
    if sys.argv[1] == 'eigen':
        #### 固有顔法 ####

        # データ準備
        ## トレーニング時のラベル割り当てと揃える
        user_dict = {'goda':0, 'tada':1, 'yasumitsu':2, 'unknown':3}
        eigen_model = FILE_PATH + 'model/recognizer.face'

        # モデル準備
        recognizer = Eigen_FaceRecognizer(eigen_model, user_dict)

    elif sys.argv[1] == 'alexnet':
        #### CNN (AlexNet) ####

        # データ準備
        cnn_model = FILE_PATH + 'model/alexnet9_4.model'
        net = AlexNet

        # モデル準備
        recognizer = CNN_FaceRecognizer(net, cnn_model)

    elif sys.argv[1] == 'vggfacenet':
        #### CNN (VggFaceNet) ####
        # データ準備
        cnn_model = FILE_PATH + 'model/vggfacenet33_4.model'
        net = VggFaceNet

        # モデル準備
        recognizer = CNN_FaceRecognizer(net, cnn_model)


    cascade = '/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    cam = camera.Camera(cascade=cascade)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        face = cam.get_face()
        user = 'no user'
        if face is not None:
            user = recognizer.predict(face)
        print(user)

    cam.close()
