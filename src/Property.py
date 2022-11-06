#
# 
# 属性类
#
#
methodNames=["Hash","Color","SIFT","VggNet"]
methodNum=len(methodNames)
colorInt=methodNames.index("Color")+1
vggnetInt=methodNames.index("VggNet")+1
hashInt=methodNames.index("Hash")+1
siftInt=methodNames.index("SIFT")+1
displayImgaeNum=10 

mw_default_seaImg="testdata/193003.jpg"
mw_default_dataset="testdata"
mw_default_method=1

dn_pathBatchSize=100

se_colorEps=1e-10

colorhistSize=[8,12,3]

siftDescribeLengeh=128
siftMatcheRatio = 0.5
knnMatcheNum=2

#VGG
batchSize=32
input_shape = (224, 224, 3)
weight = 'imagenet'
poolingType = 'max'
isInclude_top=False