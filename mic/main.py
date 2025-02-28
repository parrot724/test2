# coding=utf-8
import hiai
from hiai.nn_tensor_lib import DataType
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()
import os
import numpy as np
import time
from ctc_func import greedy_decode
import pcm2wav as L
from pcm2wav import pcm2wav
from get_features import RecognizeSpeech_FromFile
from make_input_tensor import make_input_tensor
from get_symbol_list import GetSymbolList
from language_model_func import ModelLanguage
from wav_seg import wav_seg


# 定义文件获取路径
speech_recog_model = 'speech_recog_model/speech_model.om' # 语音识别的声学模型
speech_voice_path =  'speech_voice/teacher.wav'
speech_voice_path2 = 'speech_voice/teacher.pcm' # 开发板保存的语音路径
wav_seg_path = 'wav_seg/' # 语音分割后保存的路径

audiotype = 'wav' # 定义输入音频文件的格式。也可设置为pcm


def GetDataSet(speech_voice_path):
    """ 读取pcm格式音频数据 """

    # 将pcm数据转换为wav
    wave_path = L.pcm2wav(speech_voice_path) 

    # 读取wav音频特征
    features, in_len = RecognizeSpeech_FromFile(wave_path) 
    #print features

    # 将wav音频特征转换为模型输入向量
    input_tensor = make_input_tensor(features) 

    return input_tensor, in_len

def GetDataSet2(speech_voice_path):
    """ 直接读取wav格式音频数据 """

    features, in_len = RecognizeSpeech_FromFile(speech_voice_path) #1,1600,200,1  in_len=122 全0矩阵
    features1=np.reshape(features,[1,1600,200,1])

    features1=np.transpose(features1,(0,3,1,2)).copy()
    #print(features1.shape)
    #print("tensor输入张量")
    input_tensor = make_input_tensor(features1)
    return input_tensor, in_len


def CreateGraph(model):

    # 调用get_default_graph获取默认Graph，再进行流程编排
    myGraph = hiai.hiai._global_default_graph_stack.get_default_graph()

    if myGraph is None:
        print 'Get default graph failed'
        return None

    nntensorList = hiai.NNTensorList()

    # 不实用DVPP缩放图像，使用opencv缩放图片
    resultInference = hiai.inference(nntensorList, model, None) # 不确定其功能

    if (hiai.HiaiPythonStatust.HIAI_PYTHON_OK == myGraph.create_graph()):
        print 'create graph ok !'
        return myGraph
    else:
        print 'create graph failed, please check log.'
        return None


def GraphInference(graphHandle, inputTensorList):
    if not isinstance(graphHandle, hiai.Graph):
        print 'graphHandle is not Graph object'
        return None

    resultList = graphHandle.proc(inputTensorList)
    return resultList


def SpeechPostProcess(resultList, in_len): 
    resultList1 = resultList[0]
    resultArray = resultList[0]
    batchNum = resultArray.shape[0]  
    confidenceNum = resultArray.shape[1]  

    confidenceList = resultArray[:, 0, 0, :]
    resultArray1=np.swapaxes(resultArray,0,2)
    resultArray2 = np.swapaxes(resultArray1, 0, 1)
    confidenceList = resultArray2[0]

    confidenceArray = np.array(confidenceList)

    resultList = confidenceArray

    # 将三维矩阵转为二维
    dets = np.reshape(resultList, (200,1424))

    # 进行解码，将结果转为拼音序列
    rr, ret1 = greedy_decode(dets)

    # 去除拼音序列中的blank
    for i in range(len(ret1)):
        if i % 2 == 0:
            try:
                ret1.remove(1423)
            except:
                pass

    list_symbol_dic = GetSymbolList()

    r_str = []
    for i in ret1:
        r_str.append(list_symbol_dic[i])

    #print "拼音序列识别结果：" + str(r_str)
    string_pinyin = str(r_str)

    ml = ModelLanguage('language_model')

    ml.LoadModel()

    str_pinyin = r_str

    r = ml.SpeechToText(str_pinyin)

    # 保存语音识别的结果
    with open('results/asr_results.txt','a+b') as f:
        data = ' ' + string_pinyin[1:-1] + '-' + r + '\n'
        f.write(data)
        f.close()

    return r


def main():

    # 将整段语音进行分割
    speech_num = wav_seg(speech_voice_path)

    # 加载语音识别的声学模型
    print "Start load speech model"
    inferenceModel = hiai.AIModelDescription('asr', speech_recog_model)
    if inferenceModel is None:
        print 'Load model failed'
        return None

    # 初始化Graph
    print "Start init Graph"
    myGraph = CreateGraph(inferenceModel)

    # 开始识别分割后的所有语音
    print "Start inference"
    for i in range(speech_num):
        speech_path = wav_seg_path + str(i) + '.' + audiotype

        # 开始读取音频数据
        # 输入音频为pcm格式，即直接读取开发板录制的pcm格式音频，如输入音频为wav格式，请使用下行代码
        #Input_tensor, in_len = GetDataSet(speech_path)

        # 输入音频为wav格式，如输入音频为pcm，请注释掉上述代码
        Input_tensor, in_len = GetDataSet2(speech_path)

        # 判断Input_data是否正确获取
        if (Input_tensor == None):
            print 'Get input data failed'
            continue

        # 开始模型推理
        resultList = GraphInference(myGraph, Input_tensor)
        list_shape = np.array(resultList).shape

        # 判断模型推理结果是否成功
        if resultList is None:
            print "Inference failed"
            continue

        # 对结果进行后处理
        final_result = SpeechPostProcess(resultList,in_len)

        #print str(i) + '. 文本识别结果： ' + str(final_result)
        print 'finished ' + str(i)


    hiai.hiai._global_default_graph_stack.get_default_graph().destroy()

    print 'Speech Recognizition Finished !'


if __name__ == "__main__":
    main()