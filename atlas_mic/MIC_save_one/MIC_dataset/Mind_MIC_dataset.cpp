/**
*
* Copyright(c)<2018>, <Huawei Technologies Co.,Ltd>
*
* @version 1.0
*
* @date 2018-5-19
*/
#include "Mind_MIC_dataset.h"
#include "hiaiengine/log.h"
#include "BatchImageParaWithScale.h"
#include <memory>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <string.h>
#include <chrono>
extern "C"
{
#include "driver/peripheral_api.h"
}

using hiai::Engine;
using namespace hiai;


#define MAX_AUDIO_DATA_SIZE (2048*4*2*2)

std::string Mind_MIC_dataset::Mind_MIC_datasetConfig::ToString() const{
    char msg[MAX_CONFIG_LOG_LENGTH];
    std::string ret;

    int retCode = sprintf_s(msg, MAX_CONFIG_LOG_LENGTH,
            "soundMode:%d, samplerate:%d, sampleNumPerFrame:%d, bitwidth:%d",
            this->soundMode, this->samplerate,
            this->sampleNumPerFrame, this->bitwidth);

    // If an error occurred sprintf_s return -1
    if (retCode != -1)
    {
        ret = msg;
    }
    return ret;
}


Mind_MIC_dataset::Mind_MIC_dataset(){
    config = NULL;
    frameId = 0;
    exit = MICDATASETS_INIT;
    InitConfigParams();
}

Mind_MIC_dataset::~Mind_MIC_dataset(){
}

HIAI_StatusT Mind_MIC_dataset::Init(const hiai::AIConfig& conf,
        const std::vector<hiai::AIModelDescription>& model_desc){

    HIAI_ENGINE_LOG(HIAI_IDE_INFO, "start init!");

    if (NULL == config){

        config = std::shared_ptr<Mind_MIC_datasetConfig>(new(std::nothrow) Mind_MIC_datasetConfig);
        //check config validate
        if (config == nullptr)
        {
            HIAI_ENGINE_LOG(HIAI_IDE_INFO, "allocate config buffer failed");
            HIAI_ENGINE_LOG(HIAI_IDE_INFO, "end init!");
        }
    }

    for (int index = 0; index < conf.items_size(); ++index){
        const ::hiai::AIConfigItem& item = conf.items(index);
        std::string name = item.name();
        std::string value = item.value();

        if (name == "samplerate")
        {
            config->samplerate = CommonParseParam(value);
        }
        else if (name == "sampleNumPerFrame")
        {
            config->sampleNumPerFrame = CommonParseParam(value);
        }
        else if (name == "bitwidth")
        {
            config->bitwidth = CommonParseParam(value);
        }
        else if (name == "datasource")
        {
            config->soundMode = CommonParseParam(value);
        }else{
            // unused name.
            HIAI_ENGINE_LOG(HIAI_IDE_INFO, "unused config name: %s", name.data());
        }

    }

    HIAI_StatusT ret = HIAI_OK;
    bool faildflag = (PARSEPARAM_FAIL == config->samplerate ||
                    PARSEPARAM_FAIL == config->sampleNumPerFrame ||
                    PARSEPARAM_FAIL == config->bitwidth);

    if (faildflag){
        std::string msg = config->ToString();
        msg.append(" config data failed");
        HIAI_ENGINE_LOG(HIAI_IDE_ERROR, msg.data());

        ret = HIAI_ERROR;
    }

    HIAI_ENGINE_LOG(HIAI_IDE_INFO, "end init!");
    return ret;
}


void Mind_MIC_dataset::InitConfigParams(){
    params.insert(
            std::pair<std::string, std::string>("8K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_8000)));
    params.insert(
            std::pair<std::string, std::string>("12K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_12000)));
    params.insert(
            std::pair<std::string, std::string>("11.025K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_11025)));
    params.insert(
            std::pair<std::string, std::string>("16K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_16000)));
    params.insert(
            std::pair<std::string, std::string>("22.05K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_22050)));
    params.insert(
            std::pair<std::string, std::string>("24K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_24000)));
    params.insert(
            std::pair<std::string, std::string>("32K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_32000)));
    params.insert(
            std::pair<std::string, std::string>("44.1K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_44100)));
    params.insert(
            std::pair<std::string, std::string>("48K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_48000)));
    params.insert(
            std::pair<std::string, std::string>("64K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_64000)));
    params.insert(
            std::pair<std::string, std::string>("96K",
                    IntToString(MIC_AUDIO_SAMPLE_RATE_96000)));

    params.insert(
            std::pair<std::string, std::string>("80",
                    IntToString(MIC_SAMPLE_NUM_80)));
    params.insert(
            std::pair<std::string, std::string>("160",
                    IntToString(MIC_SAMPLE_NUM_160)));
    params.insert(
            std::pair<std::string, std::string>("240",
                    IntToString(MIC_SAMPLE_NUM_240)));
    params.insert(
            std::pair<std::string, std::string>("320",
                    IntToString(MIC_SAMPLE_NUM_320)));
    params.insert(
            std::pair<std::string, std::string>("480",
                    IntToString(MIC_SAMPLE_NUM_480)));
    params.insert(
            std::pair<std::string, std::string>("1024",
                    IntToString(MIC_SAMPLE_NUM_1024)));
    params.insert(
            std::pair<std::string, std::string>("2048",
                    IntToString(MIC_SAMPLE_NUM_2048)));


//    params.insert(
//            std::pair<std::string, std::string>("8 bit",
//                    IntToString(MIC_AUDIO_BIT_WIDTH_8)));
    params.insert(
            std::pair<std::string, std::string>("16-bit",
                    IntToString(MIC_AUDIO_BIT_WIDTH_16)));
    params.insert(
            std::pair<std::string, std::string>("24-bit",
                    IntToString(MIC_AUDIO_BIT_WIDTH_24)));

    params.insert(
            std::pair<std::string, std::string>("MONO",
                    IntToString(MIC_AUDIO_SOUND_MODE_MONO)));
    params.insert(
            std::pair<std::string, std::string>("STEREO",
                    IntToString(MIC_AUDIO_SOUND_MODE_STEREO)));

}

std::string Mind_MIC_dataset::IntToString(int value){
    char msg[MAX_VALUESTRING_LENGTH];
    std::string ret;

    int retCode = sprintf_s(msg, MAX_VALUESTRING_LENGTH, "%d", value);

    // If an error occurred sprintf_s return -1
    if (retCode != -1)
    {
        ret = msg;
    }

    return ret;
}


int Mind_MIC_dataset::CommonParseParam(const std::string& val) const{
    std::map<std::string, std::string>::const_iterator it = params.find(val);
    if (it != params.end())
    {
       return atoi((it->second).c_str());
    }
    return -1;
}


Mind_MIC_dataset::MicOperationCode Mind_MIC_dataset::PreCapProcess(){
    MediaLibInit();

    MICStatus  status = QueryMICStatus();
    if (status != MIC_STATUS_CLOSED){
        HIAI_ENGINE_LOG(HIAI_IDE_ERROR,
                "PreCapProcess.QueryMICStatus {status:%d} failed.",
                status);
        return MIC_NOT_CLOSED;
    }

    //Open MIC
    int ret = OpenMIC();
    if (ret == 0){
        HIAI_ENGINE_LOG(HIAI_IDE_ERROR, "PreCapProcess OpenMIC  failed.");
        return MIC_OPEN_FAILED;
    }


    MICProperties  prop;
    prop.bit_width = (AudioBitWidth) config->bitwidth;
    prop.sample_rate = (AudioSampleRate) config->samplerate;
    prop.frame_sample_rate =
            (AudioSampleNumPerFrame) config->sampleNumPerFrame;
    prop.sound_mode = (AudioMode) config->soundMode;
    prop.cap_mode = MIC_CAP_ACTIVE;

    //set property.
    ret  = SetMICProperty(&prop);
    if (ret == 0){
        HIAI_ENGINE_LOG(HIAI_IDE_ERROR,
                "PreCapProcess SetMICProperty %s failed.",
                config->ToString().c_str());
        return MIC_SET_PROPERTY_FAILED;
    }

    return MIC_OK;
}


std::shared_ptr<Mind_MIC_dataset::BatchAudioPara<uint8_t>>
 Mind_MIC_dataset::CreateBatchAudioParaObj(){
    std::shared_ptr<Mind_MIC_dataset::BatchAudioPara<uint8_t>> pObj =
            std::shared_ptr<Mind_MIC_dataset::BatchAudioPara<uint8_t>>(
                    new(std::nothrow) Mind_MIC_dataset::BatchAudioPara<uint8_t>()
    );

    // check shared_ptr empty.
    if (pObj == nullptr)
    {
        return pObj;
    }

    pObj->info.isFirst = (frameId == 0);
    pObj->info.isLast = false;
    pObj->info.batchSize = 1;
    pObj->info.maxBatchSize = 1;
    pObj->info.batchId = 0;
    pObj->info.frameId.push_back(frameId++);
    pObj->info.timestamp.push_back(time(NULL));

    AudioData<uint8_t> audioData;
    audioData.encode = PCM_SIGNED;
    audioData.depth = config->bitwidth;

    //calc bitwidth.
    const int towBytes = 2;
    const int threeBytes = 3;

    uint32_t bitwidth = towBytes;

    if (config->bitwidth == (int) MIC_AUDIO_BIT_WIDTH_24){
        bitwidth = threeBytes;
    }else{
        bitwidth = 2;
    }

    // calc channel.
    uint32_t channelcount = 1;

    if (config->soundMode == (int) MIC_AUDIO_SOUND_MODE_STEREO){
        channelcount = 2;
    }


    audioData.size = config->sampleNumPerFrame * bitwidth * channelcount;
    uint8_t * audio_buffer_ptr1_  = nullptr;

    // check buff size.
    if (audioData.size < MAX_AUDIO_DATA_SIZE && audioData.size > 0)
    {
        audio_buffer_ptr1_ =  new(std::nothrow) uint8_t[audioData.size];
    }

    std::shared_ptr < uint8_t > data(audio_buffer_ptr1_);

    audioData.data = data;
    pObj->audio.push_back(audioData);

    return pObj;
}




bool Mind_MIC_dataset::DoCapProcess(){
    MicOperationCode retCode = PreCapProcess();

    if (retCode != MIC_OK){
        if (retCode == MIC_SET_PROPERTY_FAILED){
             CloseMIC();
        }

        HIAI_ENGINE_LOG(HIAI_IDE_ERROR, "DoCapProcess.PreCapProcess failed");

        return false;
    }


    SetExitFlag(MICDATASETS_RUN);

    int readSize = 0;
    int readRet = 0;
    int readFlag = false;

    HIAI_StatusT hiai_ret = HIAI_OK;
    
    int file_name_num = 0;
    int fps_num = 0;
    while (MICDATASETS_RUN == GetExitFlag()){
        std::shared_ptr<BatchAudioPara<uint8_t>> pObj =\
                CreateBatchAudioParaObj();

        //check share_ptr empty
        if (pObj == nullptr)
        {
            continue;
        }

        AudioData<uint8_t>* pAudio = &pObj->audio[0];
        uint8_t* pData = pAudio->data.get();

        //check buffer validate.
        if (pData == nullptr)
        {
            continue;
        }

        readSize = (int) pAudio->size;

        // do cap procedure.
        readRet = ReadMicSound((void*) pData, &readSize);
        readFlag = ((readRet == 1) && ((int) pAudio->size == readSize));
        if (!readFlag){
            HIAI_ENGINE_LOG(HIAI_IDE_ERROR,
                    "DoCapProcess.ReadMicSound failed \
                     {readSize:%d, expect size:%d}",
                    readSize,
                    pAudio->size);
            break;
        }
        /*
        hiai_ret = SendData(0, "BatchAudioPara_uint8_t",
                std::static_pointer_cast<void>(pObj));

        if (HIAI_OK != hiai_ret){

            HIAI_ENGINE_LOG(HIAI_IDE_ERROR, "send data failed! {frameid:%d, timestamp:%lu}",
                   pObj->info.frameId[0],
                    pObj->info.timestamp[0]);
            break;
        }*/
        char *mic_file_name = new char[50];
        char *path1 = "/home/HwHiAiUser/atlas/mic/speech_voice/";
        char *path2 = ".pcm";
        sprintf(mic_file_name,"%s%d%s",path1,file_name_num,path2);
        
        FILE *file = fopen(mic_file_name,"a+b");
        if (file){
            fwrite(pData,readSize,1,file);
            fclose(file);
        }
    }

    CloseMIC();

    if (HIAI_OK != hiai_ret){
        return false;
    }

    return true;

}


void Mind_MIC_dataset::SetExitFlag(int flag){
    TLock lock(mutex);
    exit = flag;
}

int Mind_MIC_dataset::GetExitFlag(){
    TLock lock(mutex);
    return exit;
}


HIAI_IMPL_ENGINE_PROCESS("Mind_MIC_dataset", Mind_MIC_dataset, INPUT_SIZE)
{
    HIAI_ENGINE_LOG(HIAI_IDE_INFO, "start process!");
    bool flag = DoCapProcess();
    if (flag == false){
        hiai::Graph::DestroyGraph(GetGraphId());
    }
    HIAI_ENGINE_LOG(HIAI_IDE_INFO, "end process!");
    return HIAI_OK;
}
