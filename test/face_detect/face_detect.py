# coding=utf-8
import numpy as np 
import cv2 as cv 
import sys
import time
import math

from common import face_detect

# 测试图片数量
imgs_num = 3
imgs_path_front = 'face_imgs/'
imgs_path_front2 = 'results/'


for i in range(imgs_num):
    # 读取图像
    imgs_path = imgs_path_front + str(i) + '.jpg'
    img = cv.imread(imgs_path)

    # 人脸检测
    rect = face_detect(img)

    # 画出人脸框
    if rect != []:
        #print 'ok'
        for x,y,w,h in rect:
            cv.rectangle(img, (x,y), ((x+w),(y+h)), (0,255,0), 2)

            save_path = imgs_path_front2 + str(i) + '.jpg'
            cv.imwrite(save_path, img)
            print 'finished ' + str(i) +'.jpg'

print 'sucessfully!'



