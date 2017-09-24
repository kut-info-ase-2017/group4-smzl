# -*- coding:utf-8 -*-
import socket
import sys
sys.path.append('./face_recognition')
import camera
import face_recognize

def main(method='eigen'):
    recognizer = None
    if method == 'eigen':
        #### 固有顔法 ####

        # データ準備
        ## トレーニング時のラベル割り当てと揃える
        user_dict = {'goda':0, 'tada':1, 'yasumitsu':2, 'unkown':3}
        eigen_model = '/Users/hirto/Desktop/Advanced_SE/implementation/eigenface/recognizer.face'

        # モデル準備
        recognizer = Eigen_FaceRecognizer(eigen_model, user_dict)

    elif method == 'alexnet':
        #### CNN (AlexNet) ####

        # データ準備
        cnn_model = '/Users/hirto/Desktop/Advanced_SE/implementation/example/face_prediction-master/cnn_4.model'
        net = AlexNet

        # モデル準備
        recognizer = CNN_FaceRecognizer(net, cnn_model)

    elif method == 'vggfacenet':
        #### CNN (VggFaceNet) ####
        # データ準備
        cnn_model = '/Users/hirto/Desktop/Advanced_SE/implementation/example/oxford/finetuning_4.model'
        net = VggFaceNet

        # モデル準備
        recognizer = CNN_FaceRecognizer(net, cnn_model)

    # while True:
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    face = cam.get_face()
    user = 'no user'
    if face is not None:
        user = recognizer.predict(face)
    return user



if __name__ == '__main__':
    cascade = '/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    cam = camera.Camera(cascade=cascade)

    # 座席表示用の名前辞書
    index = {'goda': '合田', 'tada':'多田', 'yasumitsu':'安光', 'unkown':'I am tada (^^)/'}


    host = "172.21.32.101" #server ip
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
            # gui側の名前セット用関数を呼び出したい
        	print(index[main()])
        #print('Wait...')

    clientsock.close()
    cam.close()
