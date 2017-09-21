# coding: utf-8

import numpy as np
import cv2
import sys
import time
import glob


print(__doc__)

try:
    fn = sys.argv[1]
    if fn.isdigit() == True:
        fn = int(fn)
except:
    fn = 0
print(fn)

try:
    fps = sys.argv[2]
    fps = int(fps)
except:
    fps = 30
print(fps)

try:
    resize_rate = sys.argv[3]
    resize_rate = int(resize_rate)
except:
    resize_rate = 1
print(resize_rate)

try:
    store_dir = sys.argv[4]
except:
    store_dir = '~/Desktop/Advanced_SE/implementation/data/photo'
if not store_dir.endswith('/'):
    store_dir += '/'
print(store_dir)

try:
    store_name = sys.argv[5]
except:
    store_name = 'user'
print(store_name)

video_input = cv2.VideoCapture(fn)
video_input.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
video_input.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
if (video_input.isOpened() == False):
    exit()


count = 0
exists_files = glob.glob(store_dir + store_name + '*.JPG')
if len(exists_files) > 0:
    max_idx = max([int(i.split('_')[-1].split('.')[0]) for i in exists_files])
    count = max_idx + 1

start = time.time()
sec = 15 # 10秒
while(True):
    count += 1
    count_padded = '%03d' % count

    ret, frame = video_input.read()

    height, width = frame.shape[:2]
    small_frame = cv2.resize(frame, (int(width/resize_rate), int(height/resize_rate)))

    cv2.imshow('frame', small_frame)
    c = cv2.waitKey(int(1000/fps)) & 0xFF

    write_file_name = store_dir + '/' + store_name + '_' + count_padded + ".JPG"
    cv2.imwrite(write_file_name, small_frame)

    if time.time() - start > sec:
        break
    # if c==27: # ESC
    #     break


video_input.release()
cv2.destroyAllWindows()
