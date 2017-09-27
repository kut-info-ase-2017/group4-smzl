#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2, os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse

# トレーニング画像
train_path = '/Users/hirto/Desktop/Advanced_SE/implementation/eigenface/train'

# テスト画像
test_path = '/Users/hirto/Desktop/Advanced_SE/implementation/eigenface/test'

# Haar-like特徴分類器
cascadePath = "/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# 顔認識器の構築 for OpenCV 2
#   ※ OpenCV3ではFaceRecognizerはcv2.faceのモジュールになります
# EigenFace
#recognizer = cv2.createEigenFaceRecognizer()
# FisherFace
#recognizer = cv2.createFisherFaceRecognizer()
# LBPH
recognizer = cv2.face.createLBPHFaceRecognizer()
label_dict = {'goda':0, 'tada':1, 'yasumitsu':2, 'tech-no-tan':3}
# 指定されたpath内の画像を取得
def get_images_and_labels(path):
    # 画像を格納する配列
    images = []
    # ラベルを格納する配列
    labels = []
    # ファイル名を格納する配列
    files = []
    for f in os.listdir(path):
        if '.JPG' not in f:
            if '.jpg' not in f:
                continue
        # 画像のパス
        image_path = os.path.join(path, f)

        # # グレースケールで画像を読み込む
        # image_pil = Image.open(image_path).convert('L')
        #
        # # NumPyの配列に格納
        # image = np.array(image_pil, 'uint8')

        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.imshow( cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        # plt.show()
        image = np.array(gray, 'uint8')

        # Haar-like特徴分類器で顔を検知
        faces = faceCascade.detectMultiScale(image)
        # 検出した顔画像の処理
        for (x, y, w, h) in faces:
            # 顔を 120x120 サイズにリサイズ
            roi = cv2.resize(image[y: y + h, x: x + w], (120, 120), interpolation=cv2.INTER_LINEAR)
            # 画像を配列に格納
            images.append(roi)
            # ファイル名からラベルを取得
            user = f.split('_')[0]
            labels.append(label_dict[user])
            # ファイル名を配列に格納
            files.append(f)

    return images, labels, files

if __name__ == '__main__':

    perser = argparse.ArgumentParser()
    perser.add_argument('--model', dest='model', type=str, default='', help='model file')
    args = perser.parse_args()
    model = args.model

    if model == '':
        # トレーニング画像を取得
        images, labels, files = get_images_and_labels(train_path)

        # トレーニング実施
        recognizer.train(images, np.array(labels))

        # モデルの保存
        recognizer.save('recognizer.face')
    else:
        recognizer.load(model)
    # テスト画像を取得
    test_images, test_labels, test_files = get_images_and_labels(test_path)

    i = 0
    while i < len(test_labels):
        # テスト画像に対して予測実施
        label, confidence = recognizer.predict(test_images[i])
        # 予測結果をコンソール出力
        print("Test Image: {}, Predicted Label: {}, Confidence: {}".format(test_files[i], label, confidence))
        # テスト画像を表示
        cv2.imshow("test image", test_images[i])
        cv2.waitKey(300)

        i += 1
    # 終了処理
    cv2.destroyAllWindows()
