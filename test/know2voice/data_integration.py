# coding=utf-8
from __future__ import division
from common import read_file, split_knowledge, match, connect_wav, check_voice, ne_emotion_time, emotion_to_knowledge
import sys
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 定义文件路径
knowledge_path = 'knowledge.txt' # PPT课件中知识点文件
asr_path = 'asr_results/asr_results.txt' # 语音识别结果文件
#emotion1_path = '../emotion/emotion_results/negative1.txt' # 学生1消极情绪节点文件
#emotion2_path = '../emotion/emotion_results/negative2.txt' # 学生2消极情绪节点文件

# 读取相关文件
knowledge_num,knowledge = read_file(knowledge_path)
asr_num, asr_results = read_file(asr_path)
#emotion1_num, emotion1 = read_file(emotion1_path)
#emotion2_num, emotion2 = read_file(emotion2_path)

# 定义视频FPS
fps = 15 # 用于计算时间

knowledge_index,knowledge_list= split_knowledge(knowledge)

# 查找每个知识点所在句子的序号
index_list = [] # 用于存放知识点对应的句子序号

for i in range(len(knowledge_list)):
    #print knowledge_index[i]
    #print knowledge[i]
    index = match(knowledge_list[i])
    index_list.append(index)

    # 记录每个知识点所对应的语音序号
    f = open('knowledge_results/results.txt','a+b')
    data = str(knowledge_index[i]) + '-' + str(knowledge_list[i]) + '-' + str(index) + '\n'
    f.write(data.encode())
    f.close()

#print(index_list)

# 统计wav_seg文件夹中，一共分割了多少语音
path = 'wav_seg'
count = 0
for file in os.listdir(path):
    count += 1
#print count



print 'Start to match speech and knowledge'
# 开始拼接各知识对应的所有音频。
for j in range(len(index_list)):
    voice_index_list = []
    if (j+1) < len(knowledge_list):
        for k in range(index_list[j+1] - index_list[j]):
            voice_index_list.append(index_list[j]+k)
    else:
        for m in range((count-1) - index_list[j]):
            voice_index_list.append(index_list[j]+m)

    if len(voice_index_list) > 0:
        connect_wav(knowledge_index[j],voice_index_list)

# 检查是否所有知识点都有对应的语音
check_voice(knowledge_index)

"""
print 'Start to match emotion and knowledge'
# 将消极情绪节点与知识点匹配
# 读取学生1,2的消极情绪结果
num1,negative_list1 = read_file('../emotion/emotion_results/negative1.txt')
num2,negative_list2 = read_file('../emotion/emotion_results/negative2.txt')

# 计算两个学生消极情绪时间节点
ne_emotion_time1 = ne_emotion_time(negative_list1)
ne_emotion_time2 = ne_emotion_time(negative_list2)

# 将两个学生每个消极情绪时间节点与知识点相匹配
emotion_to_knowledge('student1',knowledge_index,ne_emotion_time1)
emotion_to_knowledge('student2',knowledge_index,ne_emotion_time2)
"""

print 'Successfully finished'














