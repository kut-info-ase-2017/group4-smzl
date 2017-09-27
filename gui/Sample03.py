#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import threading
import time
import random
import socket
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont

SEAT_FILE_NAME = 'current_seat.txt'


class Example(QWidget, threading.Thread):

    def __init__(self):
        super().__init__()
        self.list_x = []
        self.list_y = []
        self.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        random.shuffle(self.index)
        self.save = []
        self.namelist = ["合田", "多田", "藤田", "安光"]
        random.shuffle(self.namelist)
        self.text = "ここにテキストを入力"
        # QPixmapオブジェクト作成
        self.pixmap = QPixmap("layout_2017.jpg")
        self.win = QMainWindow()
        self.initUI()

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
        button01 = QPushButton("Start", self)
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

    # スタートボタンの設定
    def button01Clicked(self):
        self.setUI()

    # 一つ前に戻るボタンの設定
    def button02Clicked(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to undo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
            "Are you sure you want to reset?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Yesが押されたときの処理
        if reply == QMessageBox.Yes:
            self.pixmap = QPixmap("layout_2017.jpg")
            self.lbl.setPixmap(self.pixmap)
            self.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            random.shuffle(self.index)
            self.save = []
        else:
            pass

    def setUI(self):
        rnd = random.randint(0,3)
        self.text = self.namelist[rnd]
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
            # 文字の色指定 QColor(R, G, B)
            qp.setPen(QColor(0, 0, 0))
            # フォントと文字の大きさを指定
            qp.setFont(QFont('Fantasy', 15))
            # 第一引数はx座標, 第二引数はy座標
            # 第三引数は挿入するテキスト
            qp.drawText(int(self.list_x[num-1]), int(self.list_y[num-1]), self.text)
        except:
            reply = QMessageBox.information(self, 'Message',"おめぇの席ねぇから！", QMessageBox.Cancel)

    def drawRectangles(self, qp):
        try:
            # 配列の最後を取得
            num = self.save[-1]
            self.index.append(num)
            random.shuffle(self.index)
            del self.save[-1]
            
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
            reply = QMessageBox.warning(self, 'Message',"戻れません", QMessageBox.Cancel)

    #マルチスレッドで行う処理
    def run(self):
        self.show()

class MySocket(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        host = "172.21.32.85" #server ip
        port = 8080 #port  same client
        
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #bind ip and port
        serversock.listen(10) #connect listen（Max queue）
        
        print('Waiting for connections...')
        clientsock, client_address = serversock.accept()
    
        while True:
            rcvmsg = clientsock.recv(1024)
            if rcvmsg != b'':
    	        print('Received -> %s' % (rcvmsg))
                #print('Wait...')
            elif rcvmsg == b'detect':
                #ex.setUI()
                break
                
        clientsock.close()
        
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.start()
    ex.join()
    msoc = MySocket()
    msoc.start()
    
    
    sys.exit(app.exec_())
