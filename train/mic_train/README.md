# 语音识别模型训练

1. 下载相关训练数据集，下载以下Thchs30和ST-CMDS数据集
THCHS30中文语音数据集 http://cn-mirror.openslr.org/resources/18
Free ST Chinese Mandarin Corpus http://cn-mirror.openslr.org/resources/38

2. 将两个数据集解压到dataset文件夹中

3. 开始训练模型，运行main.py
python main.py

4. 训练完成后，模型将保存于model_speech文件夹中

5. 将训练好的模型转为pb格式，运行save_h5_pb.py
python save_h5_pb.py

6. 转换后的pb模型将保存在pb_model文件夹中

7. 将转换好的pb模型，在MindStudio平台上转为om格式模型

8. MindStudio平台模型转换的具体参数设置如下

Model Name填写为模型名称：test_model
Input Format选择NCHW
Input Node 默认不变
Image Preprocess请设为off
