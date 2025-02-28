# coding=utf-8
from __future__ import division
import os
import sox
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import shutil
import wave

def read_file(file_path):
    """ 读取txt文件 """

    with io.open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return len(lines), lines

def split_knowledge(lines):
    """ 针对相应的字符，对输入的字符串进行分割 """
    knowledge_list = []
    knowledge_index = []

    for i in range(len(lines)):
        list_string = lines[i].split('-')
        #print(list_string)
        for j in range((len(list_string)-1)):
            temp = list_string[j+1]
            list_string2 = temp.split(':')
            #print (list_string2)
            knowledge_list.append(list_string2[1])
            knowledge_index.append((i+1,j+1))
    #print knowledge_list

    return knowledge_index, knowledge_list


def word2pinyin(word):
    """ 将单文字转为拼音 """
    with io.open('dict.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    pinyin = None

    for i in range(len(lines)):
        words = lines[i]
        if word != words[0]:
            continue
        else:
            pinyin_string = words[2:-1]
            pinyin = pinyin_string.split(',')
            break

    #print(pinyin[1])
    return pinyin

def word_is_pinyin(pinyin,word):
    """ 判断给定的拼音是否和给定的汉字相同 """

    word_pinyin = word2pinyin(word)

    result = False
    for i in range(len(word_pinyin)):
        if pinyin == word_pinyin[i]:
            result = True
            break

    return result

def knowledge_in_sentence(knowledge,sentence_list):
    """ 判断知识点是否在给定句子中 """
    #ret = False
    sentence = sentence_list.split(',')
    #print(len(sentence))
    n = 0
    #print(len(sentence))
    for i in range(len(sentence) - len(knowledge)+1):
        for j in range(len(knowledge)):
            #print(sentence[i+j])
            #print(knowledge[j])
            r = word_is_pinyin(sentence[i+j][2:-1],knowledge[j])
            #print(sentence[i+j][2:-1])

            if r == True:
                n += 1
        if n == len(knowledge):
            return True
        else:
            n = 0

    return False

def match(knowledge):
    """ 返回知识点所在句子的序号 """

    asr_num, asr = read_file('../mic/results/asr_results.txt')

    pinyin_list = []
    for i in range(asr_num):
        asr_line = asr[i]
        temp = asr_line.split('-')
        pinyin_list.append(temp[0])


    for j in range(len(pinyin_list)):
        #print(pinyin_list[j])
        ret = knowledge_in_sentence(knowledge,pinyin_list[j])

        if ret == True:
            return j # 返回当前句子序号，起始序号为0

    return None

def next_point(index,index_list,x1,x2):

    for i in range(len(list)-index-1):
        if index_list[i+index+1] == index_list[i+index+2]:
            return i+index+1

def connect_wav(out_name,index_list):
    """ 将多个wav音频拼接在一起 """

    cbn = sox.Combiner()
    x,y = out_name
    out = 'voice_results/' + str(x) + '-' + str(y) + '.wav'
    wav_list = []

    for j in index_list:
        wav_name = '../mic/wav_seg/' + str(j) + '.wav'
        wav_list.append(wav_name)

    cbn.build(wav_list,out,'concatenate')

def check_voice(knowledge_index):
    """ 检查是否所有的知识点都有了对应的语音。如果两个相邻知识知识点起始的语音相同，则两个知识点对应相同整段语音，
    但结果上不会被匹配上。为解决该问题，做如下操作 """

    for i in range(len(knowledge_index)):

        if i == (len(knowledge_index)-1):
            break

        x1,y1 = knowledge_index[len(knowledge_index)-i-1]
        x2,y2 = knowledge_index[len(knowledge_index)-i-2]

        wav_path1 = 'voice_results/' + str(x1) + '-' + str(y1) + '.wav'
        wav_path2 = 'voice_results/' + str(x2) + '-' + str(y2) + '.wav'

        # 判断前一个语音是否存在
        ret = os.path.exists(wav_path2)

        if ret:
            continue
        else:
            shutil.copy(wav_path1,wav_path2) #复制该语音，并命名为前一个语音

def wav_time_count(wav_file):
    """ 计算wav音频时长 """
   
    time = 0
    #with wave.open(wav_file,'rb') as f:
    f = wave.open(wav_file,'rb')
    #print float(f.getparams()[3]/f.getparams()[2])
    time = f.getparams()[3]/f.getparams()[2]
    f.close()

    return float(time)

def ne_emotion_time(negative_list):
    """ 计算消极情绪对应的时间节点 """

    fps = 15 # 视频的fps为15
    ne_time_list = []
    for index in negative_list:
        time = 1/fps*float(index) # 计算相应帧对应的时间
        #print(time)
        ne_time_list.append(time)

    return ne_time_list

def emotion_to_knowledge(student_num,knowledge_index,ne_time_list):
    """ 将消极情绪时间节点与知识点进行匹配 """

    ne_list = []
    k = 0
    time = 0
    total = 0
    for j in range(len(knowledge_index)):
        ne_list.append(0)

    for x,y in knowledge_index:

        # 计算知识点对应音频的时间
        wav_file = 'voice_results/' + str(x) + '-' + str(y) + '.wav'
        time = wav_time_count(wav_file)
        
        for i in ne_time_list:
            if (total<=float(i)) and (float(i)<(total+time)):
                #print(k)
                ne_list[k] += 1
                
            else:
                continue
        #print ne_list
        k += 1
        total += time

    #print(ne_list)
    for m in range(len(ne_list)):
        if ne_list[m] > 5: # 设定消极情绪阈值，即针对一个知识点，消极情绪帧数超过阈值，则认为学生在该知识点时处于消极情绪
            file_path = 'emotion_results/' + str(student_num) + '.txt'
            with open(file_path,'a+b') as f:
                x,y = knowledge_index[m]
                data = str(x) + '-' + str(y) + ':' + 'negative' + '\n'
                f.write(data.encode())
                f.close()






if __name__ == '__main__':
    #file_path = '../emotion/emotion_results/negative2.txt'

    #num = read_file(file_path)
    #print (num)

    #string = '1-1:图灵测试:(10,10,10,10)'
    #knowledge_path = 'knowledge.txt' # PPT课件中知识点文件
    #knowledge_num,knowledge = read_file(knowledge_path)

    #list2 = split_data(string,'-')

    #print (split_knowledge(knowledge))

    #word = '图'

    #print(word2pinyin(word))

    #print(match('补码'))
    #print(match2())
    #print(word_is_pinyin('zhun3','整'))
    #print(knowledge_in_sentence('图灵测试',['tu2','ling2','ce4','shi4','ni2']))

    #connect_wav()

    #print(wav_time_count('voice_results/1-1.wav'))

    """
    # 读取学生1,2的消极情绪结果
    num1,negative_list1 = read_file('../emotion/emotion_results/negative1.txt')
    num2,negative_list2 = read_file('../emotion/emotion_results/negative2.txt')

    # 计算两个学生消极情绪时间节点
    ne_emotion_time1 = ne_emotion_time(negative_list1)
    ne_emotion_time2 = ne_emotion_time(negative_list2)

    #print (ne_emotion_time1)
    
    knowledge_path = 'knowledge.txt' # PPT课件中知识点文件
    knowledge_num,knowledge = read_file(knowledge_path)
    knowledge_index,knowledge_list= split_knowledge(knowledge)

    #print(ne_emotion_time1)

    emotion_to_knowledge('student1',knowledge_index,ne_emotion_time1)
    """
