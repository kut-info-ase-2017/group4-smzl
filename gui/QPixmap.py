#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import random
import re
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QPixmap

SEAT_FILE_NAME = 'current_seat.txt'


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.list_x = []
        self.list_y = []
        self.initUI()


    def initUI(self):

        #ファイルの読み込み
        file = open(SEAT_FILE_NAME)
        lines_data = file.readlines()
        file.close()

        line_count = 0
        for line in lines_data:
            self.list_x.append(line.split(',')[1])
            self.list_y.append(line.split(',')[2])
            line_count += 1
        #ファイルの読み込み終了
        
        #ボタン作成
        button01 = QPushButton("Start", self)
        button01.clicked.connect(self.button01Clicked)
        button02 = QPushButton("Reset", self)
        #button02.clicked.connect(self.button02Clicked)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        # QPixmapオブジェクト作成
        pixmap = QPixmap("layout_2017.jpg")
        #pixmap2 = QPixmap("kurage.jpg")

        # ラベルを作ってその中に画像を置く
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(button01)
        hbox.addWidget(button02)
        vbox.addLayout(hbox)
        vbox.addWidget(lbl)
        
        self.setLayout(vbox)
        #これで画像の更新できるーーーー！！
        #lbl.setPixmap(pixmap2)

        #self.move(300, 200)
        self.setWindowTitle('Sample')
        self.show()        

    def button01Clicked(self):
        rnd = random.randint(0,len(self.list_x)-1)
        name = "goda"
        #print(rnd)
        #print("x: " + str(self.list_x[rnd]) + ", y: " + str(self.list_y[rnd]))
        

    def updatingImage(self):
        print("hello")
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
