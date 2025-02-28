#! /usr/bin/python
# -*- coding: utf-8 -*-
#encoding:utf-8
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import io

def show_label(j):
    """ 测试语音识别的准确性 """

    # 定义label的文件路径
    label_path = 'test_voice/label.txt'

    # 读取相关文件数据
    label_file = open(label_path,'r')

    label_lists = label_file.readlines()

    word_l = []
    pinyin_l = []
    for i in range(len(label_lists)):
        label_list = label_lists[i]

        label_tmp = label_list.split('-')

        pinyin_l.append(label_tmp[0].decode('utf-8'))
        word_l.append(label_tmp[1].decode('utf-8'))

    return pinyin_l[j],word_l[j]

def test_acc():
    """ 测试语音识别的准确性 """

    # 定义label和results的文件路径
    label_path = 'test_voice/label.txt'
    results_path = 'results/asr_results.txt'

    # 读取相关文件数据
    label_file = open(label_path,'r')
    results_file = open(results_path,'r')

    label_lists = label_file.readlines()
    results_lists = results_file.readlines()

    word_l = []
    pinyin_l = []
    for i in range(len(label_lists)):
        label_list = label_lists[i]

        label_tmp = label_list.split('-')

        pinyin_l.append(label_tmp[0].decode('utf-8'))
        word_l.append(label_tmp[1].decode('utf-8'))

    word_r = []
    pinyin_r = []
    for j in range(len(results_lists)):
        results_list = results_lists[j]

        results_tmp = results_list.split('-')

        pinyin_r.append(results_tmp[0].decode('utf-8'))
        word_r.append(results_tmp[1].decode('utf-8'))

    #print word_l
    #print pinyin_l

    #print word_r
    #print pinyin_r
    count = 0
    s = 0
    count1 = 0
    s1 = 0
    p_l = []
    p_r = []

    # 判断汉字识别准确率
    t = 3
    for k in range(20):
        tmp1 = word_l[k]
        tmp2 = word_r[k]

        tmp3 = pinyin_l[k]

        tmp3 = tmp3.split(' ')
        for ss in range(len(tmp3)):
            p_l.append(tmp3[ss].decode('utf-8'))


        tmp4 = pinyin_r[k]
        tmp4 = tmp4.split(', ')
        for mm  in range(len(tmp4)):
            if tmp4[mm].decode('utf-8') != '':
                p_r.append(tmp4[mm].decode('utf-8'))


        # 计算汉字准确度
        for m in range(len(tmp2)):
            if tmp2[m] in tmp1:
                count1 += 1
            s1 += 1
        
        # 计算拼音准确度
        for m in range(len(p_r)):

            if p_r[m][1:-1] in p_l:
                count +=1
            s += 1

    print '拼音识别准确度：' + str(count/float(s))
    print '汉字识别准确度：' + str(count1/float(s1))

if __name__ == '__main__':
    test_acc()

