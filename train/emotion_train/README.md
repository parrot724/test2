# 情绪模型训练

1. 在链接:https://pan.baidu.com/s/1x5qvwUn1M0eDsQWy4qQrgQ  密码:jjyh 下载情绪训练数据集。下载后将dataset文件放在本目录下

2. 训练情绪模型，运行main.py文件
python main.py

3. 训练完后，模型将被保存在model_emotion文件夹中。
也可以通过 链接:https://pan.baidu.com/s/1vHEo30hzd_IndjdPTV_Ubg  密码:rgyr 下载 情绪模型，并放在model_emotion文件夹中

4. 将训练好的模型，转为pb格式的模型，运行save_h5_pb.py文件
python save_h5_pb.py

5. 转换后的pb模型将保存于pb_model文件夹中

6. 将pb模型在MindStudio平台上转换为om格式模型

7. MindStudio平台模型转换时的参数设置

Mode Name填写为模型名称：emoton_model_test
nput Format选择NCHW。
Input Node 为1，1，48，48
Image Preprocess请设为on
Image Preprocess Mode 选择Static
Input Image Format选择RGB888_U8
Input Image Size设置为48，48
Image Format Conversion 设置为on
Model Image Format选择Gray
其他配置选择默认

