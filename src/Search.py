
import csv
from operator import itemgetter
import numpy as np
import cv2

from FeatureExtra import FeatureExtra

colorEps=1e-10

class Search:
    def __init__(self,mi) -> None:
        self.methodID=mi

    def searchImgMostCloestTenPath(self, ip, cp):
        if self.methodID==1:
            result=self._colorSearch(ip,cp)
        elif self.methodID==2:
            result=self._vggnetSearch(ip,cp)
        elif self.methodID==3:
            pass
        else:
            pass 
        resPaths = [x[0] for x in result[0:10]]
        return resPaths

    def _colorSearch(self,ip, cp):
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

    def _vggnetSearch(self,ip, cp):
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
