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
        result = []
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)

            if self.methodID==siftInt:
                for row in reader:
                    result.append((row[0],self._siftMatcherSearch(seaFeature,row[1:])))
                result=sorted(result, key=itemgetter(1),reverse=True)
            else:                     
                pathList = []
                feaDimNum = len(next(reader))-1
                if self.methodID==colorInt:annoyDisMethod='euclidean'
                if self.methodID==vggnetInt:annoyDisMethod='dot'
                if self.methodID == hashInt:annoyDisMethod='hamming'
                annoyIndexList = AnnoyIndex(feaDimNum, annoyDisMethod)
                for i, row in enumerate(reader):
                    feature=None
                    if self.methodID==colorInt:feature = [float(x) for x in row[1:]]
                    if self.methodID==vggnetInt:feature = [float(x) for x in row[1:]]
                    if self.methodID == hashInt:feature = [int(x) for x in row[1:]]
                    annoyIndexList.add_item(i, feature)
                    pathList.append(row[0])
                annoyIndexList.build(-1)
                result_index = annoyIndexList.get_nns_by_vector(vector=seaFeature,n=20)
                result = [[pathList[i], i] for i in result_index]

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
        seadescribes=sf[1:].reshape(int(sf[0]),siftDescribeLengeh)
        describes=np.array(feature[1:],dtype='float32').reshape(int(feature[0]),siftDescribeLengeh)
        # matches = matcher.knnMatch(seadescribes, describes,k=knnMatcheNum)
        # niceNum=0
        # for m1, n1 in matches:
        #     if m1.distance < siftMatcheRatio * n1.distance:
        #         niceNum=niceNum+1
        # return niceNum
        matches = matcher.Match(seadescribes, describes)
        niceNum=0
        for m1, n1 in matches:
            if m1.distance < siftMatcheRatio * n1.distance:
                niceNum=niceNum+1
        return niceNum

        
