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


def connect_wav():
    """ 将多个wav音频拼接在一起 """

    cbn = sox.Combiner()
    #x,y = out_name
    out = 'voice_results/connect_wav.wav'
    wav_list = []
    wav_num = 3

    for j in range(wav_num):
        wav_name = 'wav_seg/' + str(j) + '.wav'
        wav_list.append(wav_name)

    cbn.build(wav_list,out,'concatenate')

    print 'connect voice successfully!'

if __name__ == '__main__':
    connect_wav()