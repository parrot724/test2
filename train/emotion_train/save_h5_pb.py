#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform as plat
import os
import keras as kr 
import random

#from SpeechModel251 import ModelSpeech
#from LanguageModel2 import ModelLanguage

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input, Reshape, BatchNormalization, Flatten # , Flatten
from tensorflow.keras.layers import Lambda, TimeDistributed, Activation,Conv2D, MaxPooling2D #, Merge
#from keras.layers import Reshape
from tensorflow.keras import backend as K
#from keras.optimizers import SGD, Adadelta, Adam
from tensorflow.keras.models import load_model

#from get_feature import RecognizeSpeech_FromFile

import cv2 as cv
import caffe
import numpy as np 
import tensorflow as tf 

#K.set_learning_phase(0)

datapath = ''
modelpath = 'model_speech'

system_type = plat.system() # 由于不同的系统的文件路径表示不一样，需要进行判断
print(system_type)

if(system_type == 'Windows'):
    datapath = '.'
    modelpath = modelpath + '\\'
elif(system_type == 'Linux'):
    datapath = 'dataset'
    modelpath = modelpath + '/'
else:
    print('*[Message] Unknown System\n')
    datapath = 'dataset'
    modelpath = modelpath + '/'


# 创建新的模型结构
def CreateNewModel():
    input_data = Input(name='the_input', batch_shape=(1,1,48,48))

    layer1 = Conv2D(16, (3,3), activation='relu', kernel_initializer='random_uniform',data_format='channels_first')(input_data)
    layer2 = Conv2D(32, (3,3), activation='relu', kernel_initializer='random_uniform',data_format='channels_first')(layer1)
    layer3 = MaxPooling2D(pool_size=(2,2),data_format='channels_first')(layer2)

    layer4 = Conv2D(64, (3,3), activation='relu', kernel_initializer='random_uniform',data_format='channels_first')(layer3)
    layer5 = Conv2D(64, (3,3), activation='relu', kernel_initializer='random_uniform',data_format='channels_first')(layer4)
    layer6 = MaxPooling2D(pool_size=(2,2),data_format='channels_first')(layer5)

    layer7 = Flatten()(layer6)

    layer8 = Dense(2304, activation='relu', kernel_initializer='random_uniform', bias_initializer='random_uniform')(layer7)
    layer9 = Dense(128, activation='relu', kernel_initializer='random_uniform', bias_initializer='random_uniform')(layer8)
    layer10 = Dense(7, activation='softmax')(layer9)

    model_data = Model(inputs=input_data, outputs=layer10)

    #model_data.summary()
    return model_data

# 初始化新的模型
new_model = CreateNewModel()

# 加载h5的网络模型
model_path = 'model_emotion/emotion_model2.h5'
model_old = load_model(model_path)
model_old.save_weights('model_emotion/emotion_weights.h5') # 将权重单独保存

# 让新模型加载训练好的权重
model_weights_path = 'model_emotion/emotion_weights.h5'
new_model.load_weights(model_weights_path)

# 模型转换时需要知道，h5格式模型的输出张量名称。因此将其输出
print('################' + str(new_model.outputs))



# 尝试保存为pb文件
sess = K.get_session()
frozen_graph_def = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, output_node_names=["dense_2/Softmax"]) # output_node_names: 为模型输出张量名称
tf.train.write_graph(frozen_graph_def, 'pb_model', 'emotion_model.pb', as_text=False)
print("save pb file finished!")

"""
# 用于测试转换后的pb模型准确性
def freeze_graph_test(pb_path, inputs):

    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()

        with open(pb_path, 'rb') as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")

        config = tf.ConfigProto(allow_soft_placement=True)

        with tf.Session(config=config) as sess:
            sess.run(tf.global_variables_initializer())

            input_vioce_tensor = sess.graph.get_tensor_by_name("the_input:0")
            out_tensor = sess.graph.get_tensor_by_name("dense_2/Softmax:0")

            out = sess.run([out_tensor],feed_dict = {input_vioce_tensor: inputs})

            return out

# 测试数据加载：测试图像情绪识别
img = cv.imread('test_imgs/14.jpg',cv.IMREAD_GRAYSCALE)
gray = img
face_img = cv.resize(gray, (48,48))
face_img = face_img.reshape(1,1,48,48)
x_in = face_img

# 以下为测试转换后的模型
pb_path = 'pb_model/emotion_model3.pb' # 加载转换后的pb模型

out = freeze_graph_test(pb_path, x_in)
print('###################')
print(out[0][0])
print('###################')
result = out[0][0]
result = result.tolist()
print(result.index(max(result)))
"""


























