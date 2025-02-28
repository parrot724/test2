视频下载：

为了读者复现本项目，需要读者在 “链接:https://pan.baidu.com/s/13LNcWPTdwOEweUSdP2UQqQ  密码:96dx“ 下载students.mov和teacher.mov视频，并将两个视频放于”emotion/video/“目录中



文件说明：

1. atlas_mic: 为调用开发板板载麦克风，并录制音频代码。在MindSpore平台运行

2. mic: 为语音识别代码，在华为开发板上运行

3. emotion：为情绪识别代码，在华为开发板上运行

4. data_integration：为数据整合代码，在华为开发板上运行

5. run_noteapp.sh：读者可直接在华为开发板终端中运行该代码，即可自动运行智能语音课堂笔记程序，并最终输出识别结果

6. 待run_noteapp.sh运行完成后，将data_integration文件中的voice_results和emotion_results两个文件夹从开发板传回到本地服务器的“huawei/tmp/classes/student/”目录下，用于最终的网页展示。

7. test: 测试文件，用于测试语音识别和情绪识别的准确率

8. train: 训练文件，用于训练语音识别和情绪识别的模型


运行流程：

1. 在华为开发板终端中输入如下代码，来运行智能语音课堂笔记。
   bash run_noteapp.sh

2. 运行结束后，将data_integration文件夹中的voice_results和emotion_results传回本地服务器的 huawei/tmp/classes/student/ 目录下

3. 在本地服务搭建好web所需环境，可参考”命令行模式部署“文档。

4. 在本地服务器终端中打开虚拟环境运行huawei/server.py文件
   python server.py

5. 再在本地服务器终端中新打开一个窗口，并打开虚拟环境，运行huawei/static.py
   python static.py

6. 在本地服务器打开浏览器，输入 http://localhost:5500/teacher/ 即可登录教师端页面，进行课件编辑。（本项目已完成整体匹配。因此读者无需重新编辑课件，可跳过此步！否则，可能导致结果匹配混乱）
   
   教师姓名、工号可均输入：1
   
   进入后，选择要上传的pdf课件。课件位置在 huawei/tmp/演示课件.pdf

   上传成功后，点击右上角，即可编辑课件。

7. 在本地服务器打开浏览器，输入 http://localhost:5500/student/ 即可登录学生端页面
   
   学生姓名、学号可均输入：001

   进入后，选择“你要观看的课程”，并选择“nUH-大学计算机基础”。（该为实际匹配结果）

   然后，选择ppt中任意知识点听取对应授课音频
