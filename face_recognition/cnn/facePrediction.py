# coding: utf-8
from image2TrainAndTest import image2TrainAndTest
from image2TrainAndTest import getValueDataFromPath
from image2TrainAndTest import getValueDataFromImg
import alexLike

import argparse
import numpy as np
from PIL import Image
import sys
import cv2

import chainer
import chainer.functions as F
import chainer.links as L
import chainer.serializers
from chainer.datasets import tuple_dataset
from chainer import Chain, Variable, optimizers
from chainer import training
from chainer.training import extensions

class alexnet_faceRecognizer():
    '''This class recognize human face using like alex net
    '''
    def __init__(self, model, batch, channel):
        '''
        @param batch: data batch size
        @param model: path of model file
        @param channel: grayscal imagesc: channel=1, color images: channel=3
        '''
        self.batch = batch
        self.channel = channel

        # extract number of classes from model's file name
        outNumStr = model.split(".")[0].split("_")
        outnum = int(outNumStr[ len(outNumStr)-1 ])
        self.model = L.Classifier(alexLike.AlexLike(outnum))
        chainer.serializers.load_npz(model, self.model)

        # get labels
        self.label2user_dict = [""] * outnum
        for line in open("whoiswho.txt", "r"):
            user = line.split(",")[0]
            label = line.split(",")[1]
            self.label2user_dict[int(label)] = user

    def predict(self, img):
        '''Predict the human identification from image
        '''
        user, prob = '', 0.0
        pil_img = self._cv2pil_converter(img)
        valData = getValueDataFromImg(pil_img)
        pred = alexLike.predict(self.model, valData)
        predR = np.round(pred)
        for pre_i in np.arange(len(predR)):
            if predR[pre_i] == 1:
                # print("he/she is {}".format(ident[pre_i]))
                user = self.label2user_dict[pre_i]
                prob = pred[pre_i]*100
        return user, prob

    def _cv2pil_converter(self, cv_img):
        pil_img = None
        print(cv_img.shape)
        cv_img_RGB = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # cv_img_RGB = cv_img[::-1, :, ::-1].copy()
        cv2.flip(cv_img_RGB, 0)
        pil_img = Image.fromarray(cv_img_RGB)
        return pil_img



# def main():
#     parse = argparse.ArgumentParser(description='face detection')
#     parse.add_argument('--batchsize', '-b', type=int, default=100)
#     parse.add_argument('--gpu', '-g', type=int, default=-1)
#     parse.add_argument('--model','-m', default='')
#     parse.add_argument('--size', '-s', type=int, default=128)
#     parse.add_argument('--channel', '-c', default=3)
#     parse.add_argument('--testpath', '-p', default="./images/test/output/inputImage_0.png")
#     args = parse.parse_args()
#
#     if args.model == '':
#         sys.stderr.write("Tom's Error occurred! ")
#         sys.stderr.write("You have to designate the path to model")
#         return
#
#     outNumStr = args.model.split(".")[0].split("_")
#     outnum = int(outNumStr[ len(outNumStr)-1 ])
#
#     model = L.Classifier(alexLike.AlexLike(outnum))
#     chainer.serializers.load_npz(args.model, model)
#
#     ident = [""] * outnum
#     for line in open("whoiswho.txt", "r"):
#         dirname = line.split(",")[0]
#         label = line.split(",")[1]
#         ident[int(label)] = dirname
#
#     # fetch value data to predict who is he/she
#     faceImgs = faceDetectionFromPath(args.testpath, args.size)
#     for faceImg in faceImgs:
#         valData = getValueDataFromImg(faceImg)
#         pred = alexLike.predict(model, valData)
#         print(pred)
#         predR = np.round(pred)
#         for pre_i in np.arange(len(predR)):
#             if predR[pre_i] == 1:
#                 print("he/she is {}".format(ident[pre_i]))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='face detection')
    parse.add_argument('--batchsize', '-b', type=int, default=100)
    parse.add_argument('--gpu', '-g', type=int, default=-1)
    parse.add_argument('--model','-m', dest='model_path', default='')
    parse.add_argument('--size', '-s', type=int, default=120)
    parse.add_argument('--channel', '-c', default=3)
    parse.add_argument('--testpath', '-p', default="./images/test/output/inputImage_0.png")
    parse.add_argument('--cascade', dest='cascade_path', type=str, default='/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml', help='cascade file path for face detection by opencv')

    args = parse.parse_args()
    batch = args.batchsize
    model = args.model_path
    channel = args.channel
    cascade_path = args.cascade_path


    # 内蔵カメラを起動
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    # モデル取得
    recognizer = alexnet_faceRecognizer(model, batch, channel)

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)

    # 顔に表示される枠の色を指定（白色）
    color = (255,255,255)

    while True:

        # 内蔵カメラから読み込んだキャプチャデータを取得
        ret, frame = cap.read()

        # モノクロで表示する
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔認識の実行
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(150,150))

        # 顔が見つかったらcv2.rectangleで顔に白枠を表示する
        if len(facerect) > 0:
            for (x, y, w, h) in facerect:

                cliped_img = frame[y:y + h, x:x + w]

                ## 120 * 120 の画像にリサイズ
                cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)

                # alex net では カラー画像を扱う
                # gray_img = cv2.cvtColor(cliped_img, cv2.COLOR_BGR2GRAY)

                # 認識処理
                user_id, prob = recognizer.predict(cliped_img)

                if prob < 0.9:
                    user_id = 'unkown'
                    prob = 'nan'

                # テキスト、枠の設定
                text = '{0}: {1}%'.format(user_id, prob)
                cv2.putText(frame, text, (int(x), int(y)),
                    0, 1, (0, 0, 255), 3)
                cv2.rectangle(frame, (x, y), (x+w, y+w), color, thickness=2)

        # 表示
        cv2.imshow("frame", frame)

        # qキーを押すとループ終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 内蔵カメラを終了
    cap.release()
    cv2.destroyAllWindows()
