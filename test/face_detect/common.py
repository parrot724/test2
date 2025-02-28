# coding=utf-8
import cv2 as cv 
import hiai
from hiai.nn_tensor_lib import DataType
import numpy as np 
import sys 


#加载opencv训练好的人脸识别模型
cascade = cv.CascadeClassifier("./haarcascades/haarcascade_frontalface_alt.xml")

#设置情绪模型中所对应的情绪名称
emotion = ['生气','失落','担心','开心','伤心','好奇','中性']

def detect(img, cascade):
    """利用Opencv提供的人脸检测函数，输入包含人脸的图像，返回人脸框坐标"""
    
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=2, minSize=(5,5), flags=cv.CASCADE_SCALE_IMAGE)

    # 如果为检测到，则返回空列表
    if len(rects) == 0:
        return []
    # 返回人脸位置坐标
    return rects

def face_detect(img):
    """利用opencv对图像进行预处理，包括灰度转换，人脸检测操作，最终返回人脸位置信息"""

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #gray = cv.cvtColor(yuv, cv.COLOR_YUV2GRAY)

    # 获取人脸坐标
    rects = detect(gray,cascade)

    return rects

def make_input_tensor(img):
    """ 将输入图像转换为HIAI所需要的张量状态 """

    height = img.shape[2]
    width = img.shape[3]
    input_tensor = hiai.NNTensor(img,height,width,3,"img",DataType.FLOAT32_T,img.size)

    #print input_tensor.width
    #print input_tensor.height
    #print input_tensor.channel

    nntensorList = hiai.NNTensorList(input_tensor)

    return nntensorList

def emotion_postprocess(resultList):
    """ 针对模型推理后的结果进行后处理 """

    #设置情绪模型中所对应的情绪名称
    emotion = ['生气','失落','担心','开心','伤心','好奇','中性']
    
    if resultList is not None:
        resultArray = resultList[0]
        confidenceList = resultArray[0,0,0,:]

        result = confidenceList.tolist()
        index = result.index(max(result))

        return emotion[index]
        #return emotion[index]

def save_emotion(index,emotion1,emotion2):
    """ 将两个学生的情绪状态随视频每帧进行保存，并保存消极情绪状态时间 """

    # 打开情绪结果文件
    f = open('emotion_results/results.txt', 'a+b')
    data = '帧数:' + str(index) + ',学生1:' + emotion1 + ',学生2:' + emotion2 + '\n'
    
    f.write(data)
    f.close()

    if emotion1 == '生气' or emotion1 == '失落' or emotion1 == '伤心':
        # 记录学生1的消极情绪状态
        f1 = open('emotion_results/negative1.txt', 'a+b')
        data1 = str(index) + '\n'
        f1.write(data1)
        f1.close()

    if emotion2 == '生气' or emotion2 == '失落' or emotion2 == '伤心':
        # 记录学生1的消极情绪状态
        f2 = open('emotion_results/negative2.txt', 'a+b')
        data2 = str(index) + '\n'
        f2.write(data2)
        f2.close()

def color_compute(img):
    """计算图像RGB各纬度的均值"""
    r_mean = int(np.mean(img[:,:,0]))
    g_mean = int(np.mean(img[:,:,1]))
    b_mean = int(np.mean(img[:,:,2]))

    return r_mean, g_mean, b_mean































    