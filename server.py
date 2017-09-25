# -*- coding:utf-8 -*-
import socket
import sys
sys.path.append('./face_recognition')
sys.path.append('./face_recognition/cnn')
import camera
import face_recognize
from net_model import AlexNet
from net_model import VggFaceNet
from image2TrainAndTest import image2TrainAndTest
from image2TrainAndTest import getValueDataFromPath
from image2TrainAndTest import getValueDataFromImg

import os
FILE_PATH = os.path.dirname(__file__)
if len(FILE_PATH) == 0:
    FILE_PATH = ''
else:
    FILE_PATH += '/'

def main(method='alexnet'):
    recognizer = None
    if method == 'eigen':
        #### 固有顔法 ####

        # データ準備
        ## トレーニング時のラベル割り当てと揃える
        user_dict = {'goda':0, 'tada':1, 'yasumitsu':2, 'unkown':3}
        eigen_model = FILE_PATH + 'face_recognition/model/recognizer.face'

        # モデル準備
        recognizer = face_recognize.Eigen_FaceRecognizer(eigen_model, user_dict, threshold=90)

    elif method == 'alexnet':
        #### CNN (AlexNet) ####

        # データ準備
        cnn_model = FILE_PATH + 'face_recognition/model/alexnet9_4.model'
        net = AlexNet

        # モデル準備
        recognizer = face_recognize.CNN_FaceRecognizer(net, cnn_model)

    elif method == 'vggfacenet':
        #### CNN (VggFaceNet) ####
        # データ準備
        cnn_model = FILE_PATH + 'face_recognition/model/vggfacenet33_4.model'
        net = VggFaceNet

        # モデル準備
        recognizer = face_recognize.CNN_FaceRecognizer(net, cnn_model)

    # while True:
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    face = cam.get_face()
    user = 'no user'
    if face is not None:
        user = recognizer.predict(face)
    return user



if __name__ == '__main__':

    cam = camera.Camera()

    # 座席表示用の名前辞書
    index = {'goda': '合田', 'tada':'多田', 'yasumitsu':'安光', 'unknown':'I am tada (^^)/'}


    host = "172.21.32.54" #server ip
    port = 8080 #port  same client

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #bind ip and port
    serversock.listen(10) #connect listen（Max queue）

    print('Waiting for connections...')
    clientsock, client_address = serversock.accept()

    while True:
        rcvmsg = clientsock.recv(1024)
        if rcvmsg == b'detect':
            try:
                # gui側の名前セット用関数を呼び出したい
            	print(index[main()])
                #print('Wait...')
            except Exception as e:
                print(e)

    clientsock.close()
    cam.close()
