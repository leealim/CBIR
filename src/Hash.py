
from functools import reduce
import cv2
import numpy as np

class Hash:
    def __init__(self) -> None:
        pass

    def hashFeaExt(self, imgPath):
        
        imgae = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        imgae = cv2.resize(imgae, (8, 8), interpolation=cv2.INTER_AREA)
        avg = np.mean(imgae)
        imgaeList=imgae.flatten()
        return [1 if x>=avg else 0 for x in imgaeList]