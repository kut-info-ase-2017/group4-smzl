#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import signal
import threading
from multiprocessing import Process
from queue import Queue
import time
import random
import socket
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont

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

SEAT_FILE_NAME = './gui/current_seat.txt'
data_q = Queue()

FILE_PATH = os.path.dirname(__file__)
if len(FILE_PATH) == 0:
    FILE_PATH = ''
else:
    FILE_PATH += '/'

class SeatGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.list_x = []
        self.list_y = []
        self.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        random.shuffle(self.index)
        self.save = []
        #self.namelist = ["合田", "多田", "藤田", "安光"]
        self.namelist = []
        random.shuffle(self.namelist)
        self.text = "ここにテキストを入力"
        # QPixmapオブジェクト作成
        self.pixmap = QPixmap("./gui/layout_2017.jpg")
        self.initUI()
        
        #プロセスの作成と開始
        self.process = Process(target=self.target)
        self.process.start()
        
        self.msoc = MySocket(self)
        #self.msoc.start()
        signal.signal(signal.SIGINT, self.msoc.stop)

    def initUI(self):
        # ファイルの読み込み
        file = open(SEAT_FILE_NAME)
        lines_data = file.readlines()
        file.close()

        line_count = 0
        for line in lines_data:
            self.list_x.append(line.split(',')[1])
            self.list_y.append(line.split(',')[2])
            line_count += 1
        # ファイルの読み込み終了
       
        # ボタン作成
        button01 = QPushButton("Exit", self)
        #button01.setToolTip('Push!!')
        button01.clicked.connect(self.button01Clicked)
        button02 = QPushButton("Undo", self)
        button02.clicked.connect(self.button02Clicked)
        button03 = QPushButton("Reset", self)
        button03.clicked.connect(self.button03Clicked)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # ラベルを作ってその中に画像(QPixmapオブジェクト)を置く
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        hbox.addWidget(button01)
        hbox.addWidget(button02)
        hbox.addWidget(button03)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl)
        
        self.setLayout(vbox)

        self.setGeometry(0, 0, 300, 200)
        self.setWindowTitle('Sample')
        self.show()

    # 閉じるボタンの設定
    def button01Clicked(self):
        #self.setUI()
        #self.msoc.stop()
        sys.exit()

    # 一つ前に戻るボタンの設定
    def button02Clicked(self):
        reply = QMessageBox.question(self, 'Message',
            "やり直しますか？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Yesが押されたときの処理
        if reply == QMessageBox.Yes:
            qp = QPainter()        
            qp.begin(self.pixmap)
            self.drawRectangles(qp)
            qp.end()
            self.lbl.setPixmap(self.pixmap)
            
        else:
            pass
        

    # リセットボタンの設定
    def button03Clicked(self):
        reply = QMessageBox.question(self, 'Message',
            "リセットしていいんですね？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Yesが押されたときの処理
        if reply == QMessageBox.Yes:
            self.pixmap = QPixmap("layout_2017.jpg")
            self.lbl.setPixmap(self.pixmap)
            self.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            random.shuffle(self.index)
            self.save = []
            self.namelist = []
        else:
            pass

    def setUI(self):        
        # 動的に座席決定
        global data_q
        self.text = data_q.get()
        data_q.task_done()

        if self.text in self.namelist:
            pass
        else:        
            # テキストを画像に書き込み
            qp = QPainter()        
            # beginとendメソッドの間にペイントするためのメソッドを書く
            qp.begin(self.pixmap)
            self.drawText(qp)
            qp.end()
            self.lbl.setPixmap(self.pixmap)
            

            
    def drawText(self, qp):
        try:
            #座席を取得
            num = self.index[0]
            self.save.append(num)
            del self.index[0]
            self.namelist.append(self.text)

            # 文字の色指定 QColor(R, G, B)
            qp.setPen(QColor(0, 0, 0))
            # フォントと文字の大きさを指定
            qp.setFont(QFont('Fantasy', 15))
            # 第一引数はx座標, 第二引数はy座標
            # 第三引数は挿入するテキスト
            qp.drawText(int(self.list_x[num-1]), int(self.list_y[num-1]), self.text)
        except:
            reply = QMessageBox.warning(self, 'Message',"席が空いていません！", QMessageBox.Ok)

    def drawRectangles(self, qp):
        try:
            # 配列の最後を取得
            num = self.save[-1]
            self.index.append(num)
            random.shuffle(self.index)
            del self.save[-1]
            del self.namelist[-1]
            
            # Qcolor(Red, Green, Blue, Alpha) Alphaは透明度
            col = QColor(255, 255, 255)
            # ペンの色をセット
            qp.setPen(col)            
            # 図形の色をセット
            qp.setBrush(col)
            # drawRect(x, y, width, height)
            # drawRect(x座標-10, y座標-15, 50, 16)がちょうどよい感じ
            qp.drawRect(int(self.list_x[num-1])-10, int(self.list_y[num-1])-15, 50, 16)
        except:
            reply = QMessageBox.warning(self, 'Message',"戻れません", QMessageBox.Ok)

    def target(self):
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.msoc.stop()
            event.accept()
        else:
            event.ignore() 
        

class MySocket():
    def __init__(self, seat):
        threading.Thread.__init__(self)
        self.cam = camera.Camera()
        # 座席表示用の名前辞書
        self.index = {'goda': '合田', 'tada':'多田', 'yasumitsu':'安光', 'unknown':'unknown'}
        self.stop_event = threading.Event() #停止させるかのフラグ
        self.thread = threading.Thread(target=self.target)
        self.thread.daemon = True
        self.thread.start()
        #self.process = Process(target=self.target)
        #self.process.start()
        

    def main(self, method='alexnet'):
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
            
        face = self.cam.get_face()
        user = 'unknown'
        if face is not None:
            user = recognizer.predict(face)
        return user

    def target(self):
        host = "172.21.32.85" #server ip
        port = 8080 #port  same client
        
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #bind ip and port
        serversock.listen(10) #connect listen（Max queue）
        
        print('Waiting for connections...')
        clientsock, client_address = serversock.accept()

        
        while not self.stop_event.is_set():
            rcvmsg = clientsock.recv(1024)
            if rcvmsg == b'detect':
                print('Received -> %s' % (rcvmsg))
                userId = self.main()
                if userId is not None and self.index[userId] != 'unknown':
                    print(self.index[userId])
                    global data_q
                    data_q.put(self.index[userId])
                    seat.setUI()
                else:
                    print("判別できませんでした")
                self.stop_event.wait(timeout=3)

        clientsock.close()
        self.cam.close()

    def stop(self):
        self.stop_event.set()
        
        
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    seat = SeatGUI()
        
    sys.exit(app.exec_())
