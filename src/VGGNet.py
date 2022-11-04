# -*- coding: utf-8 -*-
# Author: yongyuan.name

import numpy as np
import cv2

from keras.applications.vgg19 import VGG19
from keras.utils import image_utils
from keras.applications.vgg19 import preprocess_input

input_shape = (224, 224, 3)
weight = 'imagenet'
poolingType = 'max'
isInclude_top=False

class VGGNet:
    def __init__(self):
        self.model = VGG19(weights = weight, input_shape = input_shape, pooling = poolingType, include_top = isInclude_top)

    def extract_feat(self, imgPath):
        img = image_utils.load_img(imgPath, target_size=input_shape[0:2])
        img = image_utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feature = self.model.predict(img)
        feature=feature[0]
        cv2.normalize(feature,feature)
        return feature


if __name__ == "__main__":
    ip="193003.jpg"
    fea=VGGNet().extract_feat(ip)
    