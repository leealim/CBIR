
import csv
from operator import itemgetter
import numpy as np
import cv2

from Property import *
from FeatureExtra import FeatureExtra

colorEps=1e-10

class Search:
    def __init__(self,mi) -> None:
        self.methodID=mi

    def searchImgMostCloestPath(self, ip, cp):
        if self.methodID==colorInt:
            result=self._disSearch(ip,cp)
        if self.methodID==vggnetInt:
            result=self._scoreSearch(ip,cp)
        if self.methodID==hashInt:
            result=self._hammingSearch(ip,cp)
        if self.methodID==siftInt:
            result=self._siftMatcherSearch(ip,cp)


        resPaths = [x[0] for x in result[0:displayImgaeNum]]
        # print(resPaths)
        return resPaths

    def _disSearch(self,ip, cp):
        eps=colorEps
        result = []
        fe=FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                feature = [float(x) for x in row[1:]]
                dis = 0.5*np.sum([((a-b)**2)/(a+b+eps) for (a, b) in zip(seaFeature, feature)])
                result.append((row[0], dis))
        result=sorted(result, key=itemgetter(1))
        return result

    def _scoreSearch(self,ip, cp):
        result = []
        fe=FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                feature = [float(x) for x in row[1:]]
                score = np.dot(np.array(seaFeature),np.array(feature).T)
                result.append((row[0], score))
        result=sorted(result, key=itemgetter(1),reverse=True)
        return result

    def _hammingSearch(self,ip, cp):
        result = []
        fe=FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            # testlist=['data/myData/fitness/282004.jpg', 'data/myData/fitness/280027.jpg', 'data/myData/fitness/282045.jpg', 'data/myData/fitness/282074.jpg', 'data/myData/fitness/282002.jpg', 'data/myData/fitness/280006.jpg', 'data/myData/fitness/282023.jpg', 'data/myData/bld_castle/612063.jpg', 'data/myData/bld_castle/612006.jpg', 'data/myData/bld_castle/856000.jpg']
            for row in reader:
                dis=0
                feature = [int(x) for x in row[1:]]
                for i in range(0,len(seaFeature)):
                    dis=dis+seaFeature[i]^feature[i]
                result.append((row[0], dis))
                # if row[0] in testlist:
                #     print(dis)
        result=sorted(result, key=itemgetter(1))
        return result

    def _siftMatcherSearch(self,ip, cp):
        result = []
        matcher = cv2.BFMatcher()
        fe=FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        seaDescribes=seaFeature[1:].reshape(int(seaFeature[0]),siftDescribeLengeh)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                feature = [float(x) for x in row[1:]]
                describes=np.array(feature[1:],dtype='float32').reshape(int(feature[0]),siftDescribeLengeh)
                matches = matcher.knnMatch(seaDescribes, describes,k=knnMatcheNum)
                niceNum=0
                for m1, n1 in matches:
                    if m1.distance < siftMatcheRatio * n1.distance:
                        niceNum=niceNum+1
                result.append((row[0], niceNum))
        result=sorted(result, key=itemgetter(1),reverse=True)
        return result
