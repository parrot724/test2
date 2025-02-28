#!/bin/bash
if [ -x "emotion" ];then   #这个emotion是情绪识别文件名，之后可以改

# 开始情绪识别
cd emotion
python main.py
else
echo "emotion文件不存在"
fi

# 开始语音识别
cd ../mic   #ASR是语音识别文件名，根据需求修改
python main.py

# 开始数据整合
cd ../data_integration
python data_integration.py
#scp  /out  HwHiAiUser@192.168.1.2:/home/HwHiAiUser

echo "程序运行完成，请将'data_integration/emotion_results'和'data_integration/voice_results'两个文件夹传回Ubuntu服务器，进行web结果显示"
