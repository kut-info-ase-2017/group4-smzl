# coding:utf-8

import cv2, os
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt
import argparse

import RPi.GPIO as GPIO
import time
import socket
import facePrediction

# set BCM_GPIO 17(GPIO 0) as PIR pin
PIRPin = 17

#print message at the begining ---custom function
def print_message():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    #GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(PIRPin,GPIO.IN)

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off buzzer
    ##GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()

class FaceRecognizer():
    '''
    This class recognize human face and predicts identification from movie.
    '''

    def __init__(self, init_model, user_dict):
        '''
        @param cascade_path: this file is used for face detection.
        @param init_model: serialized model path which has been aleady learned.
        @param user_dict: dictionary object(key:user name, value:numerical label).
        '''

        self.user_dict = user_dict
        self.rev_user_dict = {v:k for k,v in user_dict.items()}
        self.recognizer = cv2.createLBPHFaceRecognizer()
        self.recognizer.load(init_model)


    def predict(self, img):
        '''Predict the human identification from movie.
        @return human_name predicted human's name
        '''
        # recognition
        predicted, confidence = self.recognizer.predict(img)

        print(confidence)
        user = ''
        if confidence > 90:
            user = 'unknown'
        else:
            # find predicted human identification
            user = self.rev_user_dict[predicted]
            #cv2.imshow("user", img)
        return user


if __name__ == '__main__':

    print_message()
    parser = argparse.ArgumentParser()
    parser.add_argument('--cascade', '-c', dest='cascade_path', type=str, default='~/face.xml', help='cascade file path for face detection by opencv')
    parser.add_argument('--model', '-m', dest='model_path', type=str, default='recognizer.face', help='model file path for face recognition')
    args = parser.parse_args()
    model = args.model_path
    cascade_path = args.cascade_path
    print(cascade_path)

    setup()
    try:

        host = '172.21.32.101'
        port = 8080

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



        # 認識処理のための準備
        user_dict = {'goda':0, 'tada':1, 'yasumitsu':2, 'tech-no-tan':3}
        #recognizer = FaceRecognizer(model, user_dict)
        recognizer = facePrediction.alexnet_faceRecognizer(model, 100, 3)


        # 内蔵カメラを起動
        cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

        # カスケード分類器の特徴量を取得する
        cascade = cv2.CascadeClassifier(cascade_path)
        print(cascade)

        # 顔に表示される枠の色を指定（白色）
        color = (255,255,255)

        client.connect((host, port))

        while True:

            # 内蔵カメラから読み込んだキャプチャデータを取得

            # モノクロで表示する
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            while True:
                #print(PIRPin)
                if(GPIO.input(PIRPin)!=0):
                    print('HUMAN EXIST')
                    #client.connect((host, port))
                    ret, frame = cap.read()

                    # 顔認識の実行
                    facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10,10))

                    # 顔が見つかったらcv2.rectangleで顔に白枠を表示する
                    print(len(facerect))
                    if len(facerect) > 0:
                        for (x, y, w, h) in facerect:

                            cliped_img = frame[y:y + h, x:x + w]

                            ## 120 * 120 の画像にリサイズ
                            cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)
                            if model == 'recognizer.face':
                               cliped_img = cv2.cvtColor(cliped_img, cv2.COLOR_BGR2GRAY)

                            # 認識処理
                            user_id = recognizer.predict(cliped_img)
                            print(user_id)
                            client.send(user_id)
                            client.close()

                    # 表示
                    cv2.imshow("frame", frame)

                    time.sleep(1)
                else:
                    print ('====================')
                    print ('=     no human     =')
                    print ('====================')
                    print ('\n')
                    time.sleep(1)

    except KeyboardInterrupt:
        destroy()
        # 内蔵カメラを終了
        cap.release()
        cv2.destroyAllWindows()
        pass
