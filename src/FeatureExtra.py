#
# 
# 特征提取的分流类，具体实现在引入类中，其实这个做成抽象类更好，
# 特征提取的要求是，输入一个图片或一批图片的路径，返回这一个或者
# 一批图片的特征向量，必须flatten到1*m维
#
#
from Property import *
from VGGNet import VGGNet
from Color import Color
from Hash import Hash
from Sift import Sift

class FeatureExtra:

    def __init__(self,mi):
        self._methodID=mi

        if self._methodID==colorInt:
            self.cl=Color()

        if self._methodID==vggnetInt:
            self.vg=VGGNet()

        if self._methodID==hashInt:
            self.ha=Hash()  

        if self._methodID==siftInt:
            self.sf=Sift()   
        
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

        if self._methodID==siftInt:
            return self.sf.siftFeaExt(imgPath)


        print("impossible")