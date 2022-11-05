import cv2
import numpy as np

colorhistSize=[8,12,3]

class Color:
    def __init__(self):
        pass

    #计算颜色直方图特征    
    def colorFeaExt(self, imgPath):
        
        image = cv2.imread(imgPath)
        #转到HSV空间
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #以2*2分割图片
        (h,w) = hsv_image.shape[:2]
        (cx,cy) = (int(w*0.5), int(h*0.5))
        segments =[(0,0,cx,cy),(cx,0,w,cy),(cx,cy,w,h),(0,cy,cx,h)]
 
        #构造一个椭圆Mask来表示中心区域
        (axesX, axesY) =(int(w*0.75/2), int(h*0.75/2))
        ellipMask = np.zeros(image.shape[:2],dtype='uint8')
        cv2.ellipse(ellipMask,[cx,cy],[axesX,axesY],0,0,360,255,-1)

        #计算四个矩形的颜色直方图，添加到总的特征里
        feature =[]    
        for(x0, y0,x1, y1) in segments:
            recMask = np.zeros((h,w),dtype='uint8')
            cv2.rectangle(recMask,(x0,y0),(x1,y1),255,-1)
            recMask = cv2.subtract(recMask, ellipMask)
            hist = self._histogram(hsv_image, recMask)
            feature.extend(hist)
 
        #计算椭圆的颜色直方图，添加到总的特征里
        hist = self._histogram(hsv_image, ellipMask)
        feature.extend(hist)

        

        return feature
        
    #func::对图片的一个特定区域计算颜色直方图
    def _histogram(self, image, mask=None):
    
        hist = cv2.calcHist([image],[0,1,2],mask, colorhistSize,[0,180,0,256,0,256])
        cv2.normalize(hist,hist)
        hist=hist.flatten()

        return hist 