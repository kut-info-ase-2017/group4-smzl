
import numpy as np
from PIL import Image
import glob
from chainer.datasets import tuple_dataset

def image2TrainAndTest(pathsAndLabels, size=128, channels=1):

    allData = []
    for pathAndLabel in pathsAndLabels:
        path = pathAndLabel[0]
        label = pathAndLabel[1]
        imagelist = glob.glob(path + "*")
        for imgName in imagelist:
            allData.append([imgName, label])
    allData = np.random.permutation(allData)

    if channels == 1:
        imageData = []
        labelData = []
        for pathAndLabel in allData:
            img = Image.open(pathAndLabel[0])
            imgData = np.asarray([np.float32(img)/255.0])
            imageData.append(imgData)
            labelData.append(np.int32(pathAndLabel[1]))

        threshold = np.int32(len(imageData)/8*7)
        train = tuple_dataset.TupleDataset(imageData[0:threshold], labelData[0:threshold])
        test = tuple_dataset.TupleDataset(imageData[threshold:], labelData[threshold:])
    else:
        imageData = []
        labelData = []
        print('sd normalization')
        for pathAndLabel in allData:
            img = Image.open(pathAndLabel[0])
            r,g,b = img.split()
            np_r = np.float32(r)
            np_g = np.float32(g)
            np_b = np.float32(b)
            sd_r = np.sqrt((np_r - np_r.mean())**2)
            sd_g = np.sqrt((np_g - np_r.mean())**2)
            sd_b = np.sqrt((np_b - np_r.mean())**2)
            rImgData = np.asarray((np_r - np_r.mean()) / sd_r)
            gImgData = np.asarray((np_g - np_g.mean()) / sd_g)
            bImgData = np.asarray((np_b - np_b.mean()) / sd_b)
            # rImgData = np.asarray(np.float32(np_r / sd_r))
            # gImgData = np.asarray(np.float32(np_g / sd_g))
            # bImgData = np.asarray(np.float32(np_b / sd_b))

            # rImgData = np.asarray(np.float32(r)/255.0)
            # gImgData = np.asarray(np.float32(g)/255.0)
            # bImgData = np.asarray(np.float32(b)/255.0)
            imgData = np.asarray([rImgData, gImgData, bImgData])
            imageData.append(imgData)
            labelData.append(np.int32(pathAndLabel[1]))

        threshold = np.int32(len(imageData)/8*7)
        train = tuple_dataset.TupleDataset(imageData[0:threshold], labelData[0:threshold])
        test  = tuple_dataset.TupleDataset(imageData[threshold:],  labelData[threshold:])
        print('train num: %d' %len(train))
        print('validation num: %d' %len(test))

    return train, test

def getValueDataFromPath(imagePath):
    img = Image.open(imagePath)
    # img.show()
    r,g,b = img.split()
    rImgData = np.asarray(np.float32(r)/255.0)
    gImgData = np.asarray(np.float32(g)/255.0)
    bImgData = np.asarray(np.float32(b)/255.0)
    imgData = np.asarray([[[rImgData, gImgData, bImgData]]])
    return imgData

def getValueDataFromImg(img):
    # img.show()
    r,g,b = img.split()
    rImgData = np.asarray(np.float32(r)/255.0)
    gImgData = np.asarray(np.float32(g)/255.0)
    bImgData = np.asarray(np.float32(b)/255.0)
    imgData = np.asarray([[[rImgData, gImgData, bImgData]]])
    return imgData

if __name__=='__main__':
    pathsAndLabels = []
    pathsAndLabels.append(np.asarray(["./images/tada/", 0]))
    train, test = image2TrainAndTest(pathsAndLabels, channels=3)
    print(len(train))
    print(train[10])
