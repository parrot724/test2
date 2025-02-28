 # coding=utf-8
import numpy as np 
import cv2 as cv 
import sys
import time
import math

from common import color_compute

# 定义参数
size_rate = 1.4 # 图像缩小比例
total0 = 291 # 初始rgb
total1 = 0
time0 = time.time()
tt0 = time.time()
t1 = 0
n = 0

def main():

    video1_path = 'video/teacher.mov'

    cap1 = cv.VideoCapture(video1_path)
    print 'read video successfully!'

    print 'Start to detect ...'

    index = 0
    res = True
    while True:
        rval1, frame1 = cap1.read()

        if rval1 == False:
            break

        vis1 = cv.resize(frame1, (int(frame1.shape[1]*size_rate/2),int(frame1.shape[0]*size_rate/2))) # 教师课件图像

        # 检测PPT翻页时间
        ppt_img = vis1[235:245,300:350] # 选择PPT中合适位置作为翻页标记检测点
        r,g,b = color_compute(ppt_img) # 计算图像rgb值
        total1 = r+g+b
        global total0,tt0,n

        if (abs(total1-total0)>15):
            time1 = time.time()
            tt1 = time.time()

            t1 = time1 - time0

            if tt1 - tt0 > 2:
                tt0 = time.time()

                # 记录ppt翻页对应的视频帧数序号
                with open('results/ppt_time.txt','a+b') as f:
                    data = str(n) + '-' + str(index) + '\n'
                    f.write(data)
                    f.close()    
                    print 'frame_index: ' + str(index) + ', ppt_index: ' + str(n)   
                    n += 1
                    

                
                
        total0 = total1
        
        #print 'finished: %d.'%(index)
        index += 1

        print 'Finished'


if __name__ == '__main__':
    main()