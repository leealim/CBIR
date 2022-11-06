import numpy as np
from numpy import linalg as LA
import cv2
from keras.applications.vgg19 import VGG19
from keras.utils import image_utils
from keras.applications.vgg19 import preprocess_input
from Property import *


class VGGNet:
    def __init__(self):
        self.model = VGG19(weights = weight, input_shape = input_shape, pooling = poolingType, include_top = isInclude_top)

    def extract_feat_batch(self, imgPaths):
        imgs=[]
        for imgPath in imgPaths:
            img = image_utils.load_img(imgPath, target_size=input_shape[0:2])
            img = image_utils.img_to_array(img)
            img = np.transpose(img, (1, 0, 2)).astype('float32')
            imgs.append(img)
        imgs = np.array(imgs) / 255    
        feas=self.model.predict(imgs,batch_size=batchSize)
        feas=[cv2.normalize(x,x) for x in feas]
        return feas


    def extract_feat(self, imgPath):
        img = image_utils.load_img(imgPath, target_size=input_shape[0:2])
        img = image_utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feature = self.model.predict(img)
        feature=feature[0] / LA.norm(feature[0])
        return feature


if __name__ == "__main__":
    vg=VGGNet()
    ip="193003.jpg"
    # fea=vg.extract_feat(ip)
    ips=[ip,ip,ip]
    feas=vg.extract_feat_batch(ips)
    print(feas)
    