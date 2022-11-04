import cv2
import os

from FeatureExtra import FeatureExtra


class DataBase:

    def __init__(self):
        pass
    
    def getDatasetCsv(self,dsp:str,mi):
        setName=None
        if '/' in dsp :
            setName=dsp[dsp.rfind('/')+1:]
        else :
            setName=dsp
        csvPath="index/%s_%d.csv" %(setName,mi)
        if os.path.exists(csvPath):
            return csvPath
        else:
            self._imageSet2indexSet(dsp,mi,csvPath)
            return csvPath

    def _imageSet2indexSet(self,dsp,mi,cp):

        fe = FeatureExtra(mi)
        with open(cp, 'w', encoding='UTF-8') as f:
            for curDir, _, files in os.walk(dsp):
                for file in files:
                    if not file.endswith('.jpg'):
                        continue
                    imgPath = os.path.join(curDir, file)
                    feature = fe.img2feature(imgPath)
                    strFea=[str(x) for x in feature]
                    f.write("%s,%s\n" % (imgPath,",".join(strFea)))


if __name__ == "__main__":
    Corel101_data_path = 'data/CorelDB'
    DataBase()._imageSet2indexSet(Corel101_data_path)
    # setName="aaaa"
    # mi=3
    # print("index/%s_%d.csv" %(setName,mi))
