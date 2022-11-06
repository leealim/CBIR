import cv2
import numpy as np

from Property import *

class Sift:
    def __init__(self) -> None:
        self.sift=cv2.SIFT_create()

    def siftFeaExt(self, imgPath):
        img = cv2.imread(imgPath)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, describes = self.sift.detectAndCompute(img_gray, None)
        describeLength=describes.shape[0]
        describeFlat=describes.flatten()
        describeFlat=np.insert(describeFlat, 0, describeLength)
        return describeFlat


if __name__ == "__main__":
    fea1=Sift().siftFeaExt("193003.jpg")
    fea2=Sift().siftFeaExt("280000.jpg")
    describes1=fea1[1:].reshape(int(fea1[0]),128)
    describes2=fea2[1:].reshape(int(fea2[0]),128)
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(describes1, describes1, k=2)
    niceNum=0
    for m1, n1 in matches:
        if m1.distance < siftMatcheRatio * n1.distance:
            niceNum=niceNum+1
    print(matches)

