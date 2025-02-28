#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform as plat
import os
import keras as kr 
import random

#from SpeechModel251 import ModelSpeech
#from LanguageModel2 import ModelLanguage

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input, Reshape, BatchNormalization # , Flatten
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


AUDIO_LENGTH = 1600
AUDIO_FEATURE_LENGTH = 200
MS_OUTPUT_SIZE = 1424

def CreateNewModel():
    input_data = Input(name='the_input', batch_shape=(1,1600,200,1))

    layer_h1 = Conv2D(32, (3,3), use_bias=False, activation='relu', padding='same', kernel_initializer='he_normal')(input_data)
    layer_h2 = Conv2D(32, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h1)
    layer_h3 = MaxPooling2D(pool_size=2, strides=None, padding="valid")(layer_h2)

    layer_h4 = Conv2D(64, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h3)
    layer_h5 = Conv2D(64, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h4)
    layer_h6 = MaxPooling2D(pool_size=2, strides=None, padding="valid")(layer_h5)

    layer_h7 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h6)
    layer_h8 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h7)
    layer_h9 = MaxPooling2D(pool_size=2, strides=None, padding="valid")(layer_h8)

    layer_h10 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h9)
    layer_h11 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h10)
    layer_h12 = MaxPooling2D(pool_size=1, strides=None, padding="valid")(layer_h11)

    layer_h13 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h12)
    layer_h14 = Conv2D(128, (3,3), use_bias=True, activation='relu', padding='same', kernel_initializer='he_normal')(layer_h13)
    layer_h15 = MaxPooling2D(pool_size=1, strides=None, padding="valid")(layer_h14)

    #layer_h16 = Reshape((200,3200))(layer_h15)
    layer_h16 = tf.reshape(layer_h15, [200,3200])

    layer_h17 = Dense(128, activation="relu", use_bias=True, kernel_initializer='he_normal', name='dense1')(layer_h16)
    layer_h18 = Dense(MS_OUTPUT_SIZE, use_bias=True, kernel_initializer='he_normal', name='dense2')(layer_h17)

    y_pred = Activation('softmax', name='Activation0')(layer_h18)

    model_data = Model(inputs=input_data, outputs=y_pred)

    model_data.summary()

    return model_data


new_model = CreateNewModel()

model_weights_path = 'model_speech/speech_model251_e_0_step_625000.model.base'

new_model.load_weights(model_weights_path)

print(new_model.outputs)


#new_model.save('new_model_h5/new_base_model.h5')

#print('save h5 model finished')
#temp_model = load_model('new_model_h5/new_base_model.h5')

"""
def GetDataSet2(speech_voice_path):
    features, in_len = RecognizeSpeech_FromFile(speech_voice_path)

    #input_tensor = make_input_tensor(features)
    return features, in_len


#keras_model_file = 'keras_model/base_model.h5'

#keras_model = load_model(keras_model_file)

speech_voice_path2 = 'speech_voice/A11_0.wav'

input_tensor, in_len = GetDataSet2(speech_voice_path2)

batch_size = 1 
x_in = np.zeros((batch_size, 1600, 200, 1), dtype=np.float)
x_in[0,0:len(input_tensor)] = input_tensor
"""

#base_pred = temp_model.predict(x=x_in)

#print(base_pred)


# 尝试保存为pb文件
sess = K.get_session()

frozen_graph_def = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, output_node_names=["Activation0/Softmax"]) # output_node_names: 为模型输出张量名称

tf.train.write_graph(frozen_graph_def, 'pb_model', 'test_model.pb', as_text=False)

print("save pb file finished!")

"""
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
            out_tensor = sess.graph.get_tensor_by_name("Activation0/Softmax:0")

            out = sess.run([out_tensor],feed_dict = {input_vioce_tensor: inputs})

            return out

pb_path = 'pb_model/test_model.pb'

out = freeze_graph_test(pb_path, x_in)
print('###################')
print(out)
"""

























