import os
import math
import random
import glob
import numpy as np
from scipy import misc
from PIL import Image
import cv2
import argparse

#　左右反転
def flip_left_right(image):
    return image[:, -1::-1]

# 輝度の変更
def random_brightness(image, max_delta=63, seed=None):
    img = np.array(image)
    delta = np.random.uniform(-max_delta, max_delta)
    image = Image.fromarray(np.uint8(img + delta))
    return image

# コントラスト変更
def random_contrast(image, lower, upper, seed=None):
    factor = np.random.uniform(-lower, upper)
    mean = (image[0] + image[1] + image[2]).astype(np.float32) / 3
    img = np.zeros(image.shape, np.float32)
    for i in range(0, 3):
        img[i] = (img[i] - mean) * factor + mean
    return img

# 画像切り抜き
def crop(image, name, crop_size, padding_size):
    (width, height) = image.shape
    cropped_images = []
    for i in xrange(0, width, padding_size):
        for j in xrange(0, height, padding_size):
            box = (i, j, i+crop_size, j+crop_size) #left, upper, right, lower
            cropped_name = name + '_' + str(i) + '_' + str(j) + '.jpg'
            cropped_image = image[i:i+crop_size, j:j+crop_size]
            resized_image = cv2.resize(cropped_image, (IMAGE_SIZE, IMAGE_SIZE))
            cropped_images.append(resized_image)

    return cropped_images

# データ拡張
# data_numに指定した値になるまで「左右反転」「輝度の変更」「コントラストの変更」「切り抜き」する
def data_augmentation(image_files, data_num):
    image_list = []
    file_num = len(image_files)

    for image_file in image_files:
        image_list.append(misc.imread(image_file))

    if file_num >= data_num:
        return image_list

    # flip left right
    random.shuffle(image_list)
    for image in image_list:
        flipped_image = flip_left_right(image)
        image_list.append(flipped_image)
        if len(image_list) == data_num:
            return image_list

    # random brightness
    random.shuffle(image_list)
    for image in image_list:
        brightness_image = random_brightness(image)
        image_list.append(brightness_image)
        if len(image_list) == data_num:
            return image_list

    # random contrast
    random.shuffle(image_list)
    for image in image_list:
        contrast_image = random_contrast(image)
        image_list.append(contrast_image)
        if len(image_list) == data_num:
            return image_list

    # cropping
    random.shuffle(image_list)
    image_list.clear()
    cropped_size = int(IMAGE_SIZE * 0.75)
    padding_size = IMAGE_SIZE - cropped_size
    for image in image_list:
        cropped_image_list = crop(image, 'image', cropped_size, padding_size)
        for cropped_image in cropped_image_list:
            image_list.append(cropped_image)
            if len(image_list) == data_num:
                return image_list

    return image_list


def whitening(img):
    img = img.astype(np.float32)
    d, w, h = img.shape
    num_pixels = d * w * h
    mean = img.mean()
    variance = np.mean( (img - mean)**2 )
    stddev = np.sqrt(variance)
    min_stddev = 1.0 / np.sqrt(num_pixels)
    scale = max(stddev, min_stddev)
    img -= mean
    img /= scale
    return img

# dir_list = os.listdir(INPUT_DIR)
#
# for dir in dir_list:
#     image_files = glob.glob(os.path.join(input_dir, dir, "*.jpg"))
#     if len(image_files) == 0:
#         continue
#
#
#     image_list = data_augmentation(image_files, 1000)
#
#     for i, image in enumerate(image_list):
#         image = whitening(image)
#         misc.imsave(os.path.join(OUTPUT_DIR, dir, str(i) + '.jpg'), image)

if __name__ == '__main__':
    perser = argparse.ArgumentParser()
    perser.add_argument('--un_normalization', dest='un_norm', action='store_false', default=True, help='dosen\'t execute normalization.')
    perser.add_argument('--dir', dest='dir', type=str, default='', help='specify directory stored augumented images')
    perser.add_argument('--num', dest='num', type=int, default=300, help='specify the number of dupplicating images')
    args = perser.parse_args()
    isUn_norm = args.un_norm
    arg_dir = args.dir
    dup_num = args.num

    for dir_name in ['./photo']:
        for user in ['goda', 'tada', 'yasumitsu', 'tech-no-tan']:
            try:
                _dir = dir_name + '/' + user

                _dir_faces = _dir + '/faces'
                _dir_augmented = _dir + '/augmented'
                if not os.path.exists(_dir_augmented):
                    os.mkdir(_dir_augmented)

                file_list = [_dir_faces + '/' + jpg for jpg in os.listdir(_dir_faces) if '.JPG' in jpg or '.jpg' in jpg]
                img_list = data_augmentation(file_list, dup_num)
                for i, img in enumerate(img_list):
                    # normalized_img = whitening(img)
                    # 例えば、テスト用画像のみを作成するときに下のif文を実行
                    if arg_dir != '':
                        misc.imsave(arg_dir + user + '_' + str(i) + '.JPG', img)
                    else:
                        misc.imsave(_dir + '/augmented/' + user + '_' + str(i) + '.JPG', img)

            except Exception as e:
                print(e)
                print('error in user %s' %user)
