#
# 
# 搜索类，根据使用方法的不同选择不同的比较方法
#
#
import csv
from operator import itemgetter
import numpy as np
import cv2
from annoy import AnnoyIndex

from Property import *
from FeatureExtra import FeatureExtra

class Search:
    def __init__(self, mi) -> None:
        self.methodID = mi

    def searchImgMostCloestPath(self, ip, cp):
        ifSortReverse=False if self.methodID==colorInt or self.methodID==hashInt else True
        result = []
        tmpList = []
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                if self.methodID==colorInt:
                    result.append((row[0],self._disSearch(seaFeature,row[1:]))) 
                if self.methodID==vggnetInt:
                    result.append((row[0],self._scoreSearch(seaFeature,row[1:])))
                if self.methodID==hashInt:
                    result.append((row[0],self._hammingSearch(seaFeature,row[1:])))
                if self.methodID==siftInt:
                    result.append((row[0],self._siftMatcherSearch(seaFeature,row[1:])))
        result=sorted(result, key=itemgetter(1),reverse=ifSortReverse)
        resPaths = [x[0] for x in result[0:displayImgaeNum]]
        return resPaths

    def _disSearch(self,sf, row):
        eps=se_colorEps
        feature = [float(x) for x in row]
        dis = 0.5*np.sum([((a-b)**2)/(a+b+eps) for (a, b) in zip(sf, feature)])
        return dis

    def _scoreSearch(self,sf, row):
        feature = [float(x) for x in row]
        score = np.dot(np.array(sf),np.array(feature).T)
        return score


    def _hammingSearch(self,sf, row):
        dis=0
        feature = [int(x) for x in row]
        for i in range(0,len(sf)):
            dis=dis+sf[i]^feature[i]
        return dis

    def _siftMatcherSearch(self,sf, row):
        matcher = cv2.BFMatcher()
        feature = [float(x) for x in row]
        describes=np.array(feature[1:],dtype='float32').reshape(int(feature[0]),siftDescribeLengeh)
        matches = matcher.knnMatch(sf, describes,k=knnMatcheNum)
        niceNum=0
        for m1, n1 in matches:
            if m1.distance < siftMatcheRatio * n1.distance:
                niceNum=niceNum+1
        return niceNum

        
