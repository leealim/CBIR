import csv
from operator import itemgetter
import numpy as np
import cv2
from annoy import AnnoyIndex

from Property import *
from FeatureExtra import FeatureExtra

colorEps = 1e-10


class Search:
    def __init__(self, mi) -> None:
        self.methodID = mi

    def searchImgMostCloestPath(self, ip, cp):
        if self.methodID == colorInt:
            result = self._disSearch(ip, cp)
        if self.methodID == vggnetInt:
            result = self._scoreSearch(ip, cp)
        if self.methodID == hashInt:
            result = self._hammingSearch(ip, cp)
        if self.methodID == siftInt:
            result = self._siftMatcherSearch(ip, cp)

        resPaths = [x[0] for x in result[0:displayImgaeNum]]
        # print(resPaths)
        return resPaths

    def _disSearch(self, ip, cp):
        eps = colorEps
        result = []
        tmpList = []
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            featureCnt = len(next(reader)) - 1
            print(featureCnt)
            a = AnnoyIndex(featureCnt, 'euclidean')
            for index, row in enumerate(reader):
                feature = [float(x) for x in row[1:]]
                a.add_item(index, feature)
                tmpList.append(row[0])
        a.build(-1)
        result_index = a.get_nns_by_vector(vector=seaFeature,
                                           n=20)
        result = [[tmpList[i], i] for i in result_index]
        print(result)
        return result

    def _scoreSearch(self, ip, cp):
        eps = colorEps
        result = []
        tmpList = []
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            featureCnt = len(next(reader)) - 1
            print(featureCnt)
            a = AnnoyIndex(featureCnt, 'dot')
            for index, row in enumerate(reader):
                feature = [float(x) for x in row[1:]]
                a.add_item(index, feature)
                tmpList.append(row[0])
        a.build(-1)
        result_index = a.get_nns_by_vector(vector=seaFeature,
                                           n=20)
        result = [[tmpList[i], i] for i in result_index]
        print(result)
        return result

    def _hammingSearch(self, ip, cp):
        eps = colorEps
        result = []
        tmpList = []
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        with open(cp) as f:
            reader = csv.reader(f)
            featureCnt = len(next(reader)) - 1
            print(featureCnt)
            a = AnnoyIndex(featureCnt, 'hamming')
            for index, row in enumerate(reader):
                feature = [float(x) for x in row[1:]]
                a.add_item(index, feature)
                tmpList.append(row[0])
        a.build(-1)
        result_index = a.get_nns_by_vector(vector=seaFeature,
                                           n=20)
        result = [[tmpList[i], i] for i in result_index]
        print(result)
        return result

    # def _siftMatcherSearch(self, ip, cp):
    #     result = []
    #     matcher = cv2.BFMatcher()
    #     fe = FeatureExtra(self.methodID)
    #     seaFeature = fe.img2feature(ip)
    #     seaDescribes = seaFeature[1:].reshape(int(seaFeature[0]), siftDescribeLengeh)
    #     with open(cp) as f:
    #         reader = csv.reader(f)
    #         for row in reader:
    #             feature = [float(x) for x in row[1:]]
    #             describes = np.array(feature[1:], dtype='float32').reshape(int(feature[0]), siftDescribeLengeh)
    #             matches = matcher.knnMatch(seaDescribes, describes, k=knnMatcheNum)
    #             niceNum = 0
    #             for m1, n1 in matches:
    #                 if m1.distance < siftMatcheRatio * n1.distance:
    #                     niceNum = niceNum + 1
    #             result.append((row[0], niceNum))
    #     result = sorted(result, key=itemgetter(1), reverse=True)
    #     return result

    def _siftMatcherSearch(self, ip, cp):
        result = []
        matcher = cv2.BFMatcher()
        fe = FeatureExtra(self.methodID)
        seaFeature = fe.img2feature(ip)
        seaDescribes = seaFeature[1:].reshape(int(seaFeature[0]), siftDescribeLengeh)
        with open(cp) as f:
            reader = csv.reader(f)
            for row in reader:
                feature = [float(x) for x in row[1:]]
                describes = np.array(feature[1:], dtype='float32').reshape(int(feature[0]), siftDescribeLengeh)
                matches = matcher.knnMatch(seaDescribes, describes, k=knnMatcheNum)
                niceNum = 0
                for m1, n1 in matches:
                    if m1.distance < siftMatcheRatio * n1.distance:
                        niceNum = niceNum + 1
                result.append((row[0], niceNum))
        result = sorted(result, key=itemgetter(1), reverse=True)
        return result