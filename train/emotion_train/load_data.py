import os 
from PIL import Image
from numpy import *
import cv2 as cv 

#data_path是标签文件夹的上一级绝对目录，num_classes是分类数
def load_data(data_path, num_classes):
    num_classes = num_classes

    x_train = []
    y_trian = []

    n = [] #统计每个标签文件夹中的数据个数
    sum_num = 0 #统计加载的图像总数 
    k = 0 #中间变量

    for i in range(num_classes):
        #每个标签一个文件夹，将标签文件夹路径赋给file_path
        file_path = data_path + str(i)

        #获取标签文件夹中的图像数据
        data_file = [os.path.join(file_path, f) for f in os.listdir(file_path)]

        n.append(len(data_file))

        for img in data_file:
            im = array(Image.open(img))
            x_train.append(array(im))
            #im = cv.imread(img)

            #if (im.shape[0] == 48) and (im.shape[1]==48):
             #   x_train.append(array(im))
                #print(x_train, end='\r')
            #else:
             #   im = cv.resize(im, (48,48))
              #  x_train.append(array(im))

    #将x_train数据化
    x_train = array(x_train)

    #计算图像总数
    for i in range(num_classes):
        sum_num += n[i]

    #初始化标签向量
    y_trian = zeros(sum_num, dtype=int)

    #对标签向量赋值
    for i in range(num_classes):
        for j in range(n[i]):
            y_trian[k + j] = i

        k += n[i]

    return x_train, y_trian


