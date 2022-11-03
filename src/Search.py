
import csv
from operator import itemgetter
import numpy as np
import cv2

from FeatureExtra import FeatureExtra

class Search:
    def __init__(self) -> None:
        pass

    def searchImgMostCloestTen(self, ip, cp,mi):
        result = []
        fe=FeatureExtra(mi)
        seaImg = cv2.imread(ip)
        seaFeature = fe.img2feature(seaImg)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                feature = [float(x) for x in row[1:]]
                dis = self._computeDistace(seaFeature, feature)
                result.append((row[0], dis))
        result=sorted(result, key=itemgetter(1))
        resPaths = [x[0] for x in result[0:10]]
        return resPaths

    def _computeDistace(self, comFea, Fea, eps=1e-10):
        d = 0.5*np.sum([((a-b)**2)/(a+b+eps) for (a, b) in zip(comFea, Fea)])
        return d
