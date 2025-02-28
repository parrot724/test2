# coding=utf-8
import hiai
from hiai.nn_tensor_lib import DataType

import numpy as np 
import cv2 as cv 
import sys
import time
import math

from common import face_detect, make_input_tensor, emotion_postprocess, color_compute, save_emotion, show_label


# 情绪识别模型文件路径
emotion_model = 'emotion_model/emotion_model_gray.om'

imgs_path = 'imgs_test/'

emotion = ['生气','失落','担心','开心','伤心','好奇','中性']


def CreateGraph(model):
    """创建图"""

    # 调用get_default_graph获取默认Graph，再进行流程编排
    myGraph = hiai.hiai._global_default_graph_stack.get_default_graph()

    if myGraph is None:
        print 'Get default graph failed'
        return None

    nntensorList = hiai.NNTensorList()

    # 不实用DVPP缩放图像，使用opencv缩放图片
    resultInference = hiai.inference(nntensorList, model, None)

    if (hiai.HiaiPythonStatust.HIAI_PYTHON_OK == myGraph.create_graph()):
        #print 'create graph ok !'
        return myGraph
    else:
        print 'create graph failed, please check log.'
        return None

def GraphInference(graphHandle, inputTensorList):
    """定义推理图"""
    if not isinstance(graphHandle, hiai.Graph):
        print 'graphHandle is not Graph object'
        return None

    resultList = graphHandle.proc(inputTensorList)
    return resultList

def emotion_recog1(myGraph,img):
    """ 针对输入视频中的学生个数和位置，来特定情绪识别 """

    # 根据视频中学生的位置，将学生头像位置截取出来，剔除无用像素位置。不同的输入视频，该处需要根据视频自行设置
    person1 = img[145:245,140:240]
    person2 = img[135:235,340:440]

    # 人脸检测，返回人脸坐标位置
    rect1 = face_detect(person1)
    rect2 = face_detect(person2)

    # 定义学生1，2的情绪结果
    result1 = '-'
    result2 = '-'

    # 识别第一个学生的情绪
    if rect1 != []:
        for x,y,w,h in rect1:
            face1 = person1[y:(y+h),x:(x+w)]

            # 将人脸图像尺寸修改为网络模型所需的输入尺寸
            face_img = cv.resize(face1,(48,48))
            face_img = face_img.reshape(1,3,48,48)

            # 进行情绪识别推理
            input_tensor = make_input_tensor(face_img) # 将人脸图像转换为HIAI支持的张量形式
            resultList = GraphInference(myGraph, input_tensor) # 开始推理

            if resultList is None:
                print "Inferece failed"

            # 对推理结果进行后处理，即输出情绪识别结果
            result1 = emotion_postprocess(resultList)

    # 识别第二个学生的情绪
    if rect2 != []:
        for x,y,w,h in rect2:
            face2 = person2[y:(y+h),x:(x+w)]

            # 将人脸图像尺寸修改为网络模型所需的输入尺寸
            face_img = cv.resize(face2,(48,48))
            face_img = face_img.reshape(1,3,48,48)

            # 进行情绪识别推理
            input_tensor = make_input_tensor(face_img) # 将人脸图像转换为HIAI支持的张量形式
            resultList = GraphInference(myGraph, input_tensor) # 开始推理

            if resultList is None:
                print "Inferece failed"

            # 对推理结果进行后处理，即输出情绪识别结果
            result2 = emotion_postprocess(resultList)

    return result1, result2

def all_recog():
    """ 识别所有图像 """

    # 读取label文件
    f = open('imgs_test/label.txt','r')
    lists = f.readlines()
    label_list = lists[0]
    #print label_list[7]

    #print 'Start load emotion model'
    # 加载情绪识别模型
    inferenceModel = hiai.AIModelDescription('emotion',emotion_model)

    if inferenceModel is None:
        print 'Load model failed'
        return None

    #print 'Start init Graph'
    # 初始化Graph
    myGraph = CreateGraph(inferenceModel)

    count = 0

    for i in range(7):
        for j in range(6):
            if i == 4 and j >= 3:
                continue
            else:
                img_path = imgs_path + str(i) + str(j+1) + '.jpg'
                face_img = cv.imread(img_path)
                face_img = face_img.reshape(1,3,48,48)

                input_tensor = make_input_tensor(face_img) # 将人脸图像转换为HIAI支持的张量形式
                resultList = GraphInference(myGraph, input_tensor) # 开始推理

                if resultList is None:
                    print "Inferece failed"

                # 对推理结果进行后处理，即输出情绪识别结果
                result2, index = emotion_postprocess(resultList)

                print '-'*25 + str(i) + str(j) + '.jpg Result' + '-'*25
                print '分类编号结果：' + str(index) + ', 情绪结果：' + str(result2)
                print '-'*25 + str(i) + str(j) + '.jpg Label' + '-'*25
                print '分类编号：' + str(label_list[(i*6+j)]) + ', 情绪：' + str(emotion[int(label_list[(i*6+j)])])
                print '\n'*2
                

                if index == int(label_list[(i*6+j)]):
                    #print 1
                    count += 1

    acc = count/42.0

    print '识别准确率：' + str(acc)

    hiai.hiai._global_default_graph_stack.get_default_graph().destroy()


def single_recog(file_name):
    """识别单张图像"""

    #print 'Start load emotion model'
    # 加载情绪识别模型
    inferenceModel = hiai.AIModelDescription('emotion',emotion_model)

    if inferenceModel is None:
        print 'Load model failed'
        return None

    #print 'Start init Graph'
    # 初始化Graph
    myGraph = CreateGraph(inferenceModel)

    #file_name = sys.argv[1]

    #print 'Start load image'
    img_path = imgs_path + file_name + '.jpg'

    face_img = cv.imread(img_path)

    face_img = face_img.reshape(1,3,48,48)

    # 进行情绪识别推理
    input_tensor = make_input_tensor(face_img) # 将人脸图像转换为HIAI支持的张量形式
    resultList = GraphInference(myGraph, input_tensor) # 开始推理

    if resultList is None:
        print "Inferece failed"

    # 对推理结果进行后处理，即输出情绪识别结果
    result2, index = emotion_postprocess(resultList)

    index0 = int(file_name[0])*6 + int(file_name[1])

    label, emotion_l = show_label(index0)

    print '-'*25 + file_name + '.jpg Result' + '-'*25
    print '分类编号结果：' + str(index) + ', 情绪结果：' + str(result2)
    print '-'*25 + file_name + '.jpg Label' + '-'*25
    print '分类编号：' + str(label) + ', 情绪：' + emotion_l

    hiai.hiai._global_default_graph_stack.get_default_graph().destroy()



if __name__ == "__main__":
    if sys.argv[1] == 'all':
        print '识别所有图像'
        all_recog()
    else:
        print '识别单张图像'
        single_recog(sys.argv[1])








