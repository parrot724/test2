# 使用方法：
#
# 1.在web的教师端，针对每页ppt标准知识点。并将标注的知识点，以如下格式保存到 knowledge.txt文件中。
# 内容格式：ppt页数-当前ppt页中第几个知识点:知识点:(知识点坐标)，例如：1-1:图灵测试:(10,10,10,10)
# 
# 2.将knowledge.txt文件上传至开发板'Atlas/data_integration/'目录中
#
# 3.在开发板中，执行data_integration.py程序，进行数据整合
#
# 4.程序执行完成后，输出结果分别保存在voice_results和emotion_results文件夹中。
# voice_results文件夹中，保存了每个知识点所对应的语音。语音文件命名规则：ppt页数-当前ppt页中第几个知识点.wav，例如：1-1.wav
#
# emotion_results文件夹中，保存了每个学生消极情绪时间所对应的知识点。文件命名规则：ppt页数-当前ppt页中第几个# 知识点:negative
#
# 5.将voice_results, emotion_results两个文件夹从开发板传回到本地服务端
#
# 6.打开web学生端，web服务器加载voice_results, emotion_results两个文件夹的数据，并呈现在网页中。