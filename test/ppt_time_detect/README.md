# 测试ppt翻页检测功能，当视频中ppt翻页时，将记录翻页的时间

# 输入为文件夹video中的teacher.mov视频,需要读者在 “链接:https://pan.baidu.com/s/13LNcWPTdwOEweUSdP2UQqQ  密码:96dx“ 下载teacher.mov视频，并将视频放于”video/“目录中

# 运行程序 python main.py

# 输出为文件夹results中的ppt_time.txt文件，其中记录了ppt翻页时所对应的视频帧序号

# 注意：输入视频中的PPT封面页翻动，将不记录，从正文PPT开始记录，编号从0开始。共三页PPT，检测到两个翻页时间节点