# -*- coding:UTF-8 -*-
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


audiopath = "speech_voice/test.wav"
audiotype = 'wav' #pcm改成pcm

"""
# 读入音频
print('读入音频')
sound = AudioSegment.from_wav(audiopath)
print(sound.dBFS)
#sound = sound[:3*60*1000] #如果文件较大，先取前3分钟测试，根据测试结果，调整参数
# 分割

chunks = split_on_silence(sound,min_silence_len=760,silence_thresh=-40,keep_silence=730)#min_silence_len: 拆分语句时，静默�?.3秒则拆分。silence_thresh：小�?70dBFS以下的为静默�?

for i in range(len(chunks)):
    new = chunks[i]
    save_name = 'wav_seg/'+'%d.%s'%(i,audiotype)
    new.export(save_name, format=audiotype)
    print('%d'%i,len(new))
"""


def wav_seg(audiopath,audiotype = 'wav'):
    """ 将整段语音进行分割，并将分割结果保存。默认传入音频格式为wav，也可传入pcm格式音频，函数调用时直接将audiotype改为'pcm' """

    print 'Start to load the whole speech data'
    sound = AudioSegment.from_wav(audiopath)

    print 'Start speech segmentation'
    # 开始将整段语音分割为小段
    chunks = split_on_silence(sound,min_silence_len=760,silence_thresh=-40,keep_silence=730)

    # 将分割后的小段音频依次保存
    for i in range(len(chunks)):
        new = chunks[i]
        save_name = 'results/' + '%d.%s'%(i,audiotype)
        new.export(save_name, format=audiotype)

    print ('Success，toatlly saved：%d speech data'%(len(chunks)))

    return len(chunks)


if __name__ == '__main__':
    total = wav_seg(audiopath)