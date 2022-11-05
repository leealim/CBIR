import cv2
import os

from FeatureExtra import FeatureExtra
from Property import *

pathBatchSize=100

class DataBase:

    def __init__(self,mi) -> None:
        self.methodID=mi
    
    def getDatasetCsv(self,dsp:str):
        setName=None
        if '/' in dsp :
            setName=dsp[dsp.rfind('/')+1:]
        else :
            setName=dsp
        csvPath="index/%s_%s.csv" %(setName,methodNames[self.methodID-1])
        if os.path.exists(csvPath):
            return csvPath
        else:
            self._imageSet2indexSet(dsp,csvPath)
            return csvPath

    def _imageSet2indexSet(self,dsp,cp):
        
        paths=[]
        fe = FeatureExtra(self.methodID)
        with open(cp, 'w', encoding='UTF-8') as f:
            for curDir, _, files in os.walk(dsp):
                for file in files:
                    if not file.endswith('.jpg'):
                        continue
                    imgPath = os.path.join(curDir, file)
                    paths.append(imgPath)
                    if len(paths)==pathBatchSize:
                        features = fe.img2feature_batch(paths)
                        for i,fea in enumerate(features):
                            strFea=[str(x) for x in fea]
                            f.write("%s,%s\n" % (paths[i],",".join(strFea)))
                        paths.clear()
            if len(paths)!=0:             
                features = fe.img2feature_batch(paths)
                for i,fea in enumerate(features):
                    strFea=[str(x) for x in fea]
                    f.write("%s,%s\n" % (paths[i],",".join(strFea)))


if __name__ == "__main__":
    # Corel101_data_path = 'data/CorelDB'
    # DataBase(1)._imageSet2indexSet(Corel101_data_path)
    # setName="aaaa"
    # mi=3
    # print("index/%s_%d.csv" %(setName,mi))
    pass
