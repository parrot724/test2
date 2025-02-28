# coding=utf-8
import hiai
from hiai.nn_tensor_lib import DataType

import numpy as np 
import cv2 as cv 
import sys
import time
import math

from common import face_detect, make_input_tensor, emotion_postprocess, color_compute, save_emotion


# 情绪识别模型文件路径
emotion_model = 'emotion_model/emotion_model_gray.om'

# 视频来源
video1_path = 'video/teacher.mov' # 读取已保存视频，该线路为录制教师课件
video2_path = 'video/students.mov' # 读取已保存视频,该线路为录制学生
#video_path = 'http://xxxx.xx' #将网址改为网络摄像头直播地址，即可读取网络摄像头视频

# 定义参数
size_rate = 1.4 # 图像缩小比例
total0 = 291 # 初始rgb
total1 = 0
time0 = time.time()
tt0 = time.time()
t1 = 0
n = 0

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
        print 'create graph ok !'
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


def main():
    """定义主函数"""
    print 'Start load video'
    # 通过opencv中的类获取视频流操作对象
    cap1 = cv.VideoCapture(video1_path) # 录制教师课件线路
    cap2 = cv.VideoCapture(video2_path) # 录制学生线路

    # 检查视频读取状态
    if cap1.isOpened():
        #rval1, frame1 = cap1.read()
        print '>>>视频1_加载成功'
    else:
        #rval1 = False
        print '>>>视频1_加载失败'
        sys.exit(0)

    if cap2.isOpened():
        #rval2, frame2 = cap2.read()
        print '>>>视频2_加载成功'
    else:
        #rval2 = False
        print '>>>视频2_加载失败'
        sys.exit(0)

    """
    # 定义保存视频对象相关参数
    fps = int(cap1.get(cv.CAP_PROP_FPS)) # 视频帧数
    size = (1174,660) # 视频尺寸
    fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G') # 定义视频编码器
    outVideo = cv.VideoWriter(video_save_path, fourcc,fps, size)
    """

    print 'Start load emotion model'
    # 加载情绪识别模型
    inferenceModel = hiai.AIModelDescription('emotion',emotion_model)

    if inferenceModel is None:
        print 'Load model failed'
        return None

    print 'Start init Graph'
    # 初始化Graph
    myGraph = CreateGraph(inferenceModel)

    print 'Start read video'
    index = 0
    # 开始读取视频，通过设置视频路径，来更改视频来源
    while True:
        # 开始读取视频
        rval1, frame1 = cap1.read()
        rval2, frame2 = cap2.read()

        if rval1 == False or rval2 == False:
            print 'Emotion finshed'
            break

        # 缩小图像尺寸
        vis1 = cv.resize(frame1, (int(frame1.shape[1]*size_rate/2),int(frame1.shape[0]*size_rate/2))) # 教师课件图像
        vis2 = cv.resize(frame2, (int(frame2.shape[1]*size_rate/2),int(frame2.shape[0]*size_rate/2))) # 学生图像

        # 识别学生1，2的情绪，并返回结果
        emotion1,emotion2 = emotion_recog1(myGraph,vis2)

        # 保存学生的情绪状态
        save_emotion(index,emotion1,emotion2)


        # 检测PPT翻页时间
        ppt_img = vis1[235:245,300:350] # 选择PPT中合适位置作为翻页标记检测点
        r,g,b = color_compute(ppt_img) # 计算图像rgb值
        total1 = r+g+b
        global total0,tt0,n

        if (abs(total1-total0)>20):
            time1 = time.time()
            tt1 = time.time()

            t1 = time1 - time0

            if tt1 - tt0 > 4:
                tt0 = time.time()

                # 记录ppt翻页对应的视频帧数序号
                with open('ppt_time.txt','a+b') as f:
                    data = str(n) + '-' + str(index) + '\n'
                    f.write(data)
                    f.close()
                    n += 1
                
        total0 = total1
        
        print 'finished: %d.'%(index)
        index += 1

    hiai.hiai._global_default_graph_stack.get_default_graph().destroy()

if __name__ == "__main__":
    main()








