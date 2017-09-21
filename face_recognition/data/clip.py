#!/usr/bin python
# coding:utf-8

import cv2
import matplotlib.pyplot as plt
import os
import re
import dlib

# face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
front_path = '/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml'
profile_path = '/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_profileface.xml'
face_cascade = cv2.CascadeClassifier(front_path)

# 正面顔
# for dir_name in ['./正面顔', './右顔', './左顔']: # 横顔のトリミング成功率が低い、、、
for dir_name in ['./photo/']:
    for user in ['goda', 'tada', 'yasumitsu', 'fujita', 'shishido', 'takahashi']:
        _dir = dir_name + '/' + user
        file_list = [jpg for jpg in os.listdir(_dir) if '.JPG' in jpg or '.jpg' in jpg]
        for img_f in file_list:
            name = img_f
            img_f = _dir + '/' + img_f
            img = cv2.imread(img_f, cv2.IMREAD_COLOR)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # facerect = face_cascade.detectMultiScale(gray, 1.3, 2)

            detector = dlib.get_frontal_face_detector()
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces = detector(img_rgb, 1)

            # for (x, y, w, h) in facerect:
                # cliped_img = img[y:y + h, x:x + w]
                # # 120 * 120 の画像にリサイズ
                # cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)
                # cv2.imwrite(_dir + '/faces/' + name, cliped_img)
            for face in faces:
                top = face.top()
                bottom = face.bottom()
                left = face.left()
                right = face.right()
                height, width = img.shape[:2]
                # イレギュラーな顔領域は無視
                if not top < 0 and left < 0 and bottom > height and right > width:
                    break
                img = img[top:bottom, left:right]
                img = cv2.resize(img, (120, 120), interpolation=cv2.INTER_AREA)
                cv2.imwrite(_dir + '/faces/' + name, img)
        #         plt.imshow( cv2.cvtColor(cliped_img, cv2.COLOR_BGR2RGB))
        # plt.show()
