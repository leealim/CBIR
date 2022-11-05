import numpy as np
import cv2

from Property import *
from VGGNet import VGGNet
from Color import Color
from Hash import Hash

class FeatureExtra:

    def __init__(self,mi):
        self._methodID=mi

        if self._methodID==colorInt:
            self.cl=Color()

        if self._methodID==vggnetInt:
            self.vg=VGGNet()

        if self._methodID==hashInt:
            self.ha=Hash()   
        
    def img2feature_batch(self,imgPaths):
        
        feas=[]
        for imgPath in imgPaths:
            feas.append(self.img2feature(imgPath))
        return feas

    def img2feature(self, imgPath):

        if self._methodID==colorInt:
            return self.cl.colorFeaExt(imgPath)

        if self._methodID==vggnetInt:
            return self.vg.extract_feat(imgPath)

        if self._methodID==hashInt:
            return self.ha.hashFeaExt(imgPath)

        print("impossible")
 

if __name__ == "__main__":
    testImg = np.zeros((10,10,3),dtype='uint8')
    for i in range(0,10):
        testImg[i][i]=[0,0,200]        
    print(testImg)
    hist=cv2.calcHist([testImg],[0,1,2],None, [2,2,2],[0,180,0,256,0,256])
    print(hist)
    cv2.normalize(hist,hist)
    print(hist)
    t_hist=FeatureExtra().histogram(testImg)
    print(t_hist)