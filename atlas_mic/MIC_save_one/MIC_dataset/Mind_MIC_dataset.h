/**
*
* Copyright(c)<2018>, <Huawei Technologies Co.,Ltd>
*
* @version 1.0
*
* @date 2018-5-19
*/
#ifndef MIC_ENGINE_H
#define MIC_ENGINE_H
#include "hiaiengine/engine.h"
#include "hiaiengine/data_type.h"
#include "hiaiengine/multitype_queue.h"
#include <iostream>
#include <string>
#include <dirent.h>
#include <memory>
#include <unistd.h>
#include <vector>
#include <map>
#include <stdint.h>
#include <stdio.h>
#include <mutex>





#define INPUT_SIZE 1
#define OUTPUT_SIZE 1

#define PARSEPARAM_FAIL (-1)

#define MICDATASETS_INIT (0)
#define MICDATASETS_RUN  (1)
#define MICDATASETS_STOP (2)
#define MICDATASETS_EXIT (3)

#define MAX_CONFIG_LOG_LENGTH (255)
#define MAX_VALUESTRING_LENGTH (25)

class Mind_MIC_dataset : public hiai::Engine
{
public:

    enum MicOperationCode {
            MIC_OK = 0,
            MIC_NOT_CLOSED = -1,
            MIC_OPEN_FAILED = -2,
            MIC_SET_PROPERTY_FAILED = -3,
        };

    struct AudioBatchInfo{
        bool isFirst;   // first batch or not.
        bool isLast;    // last batch or not
        uint32_t batchSize; //size of batch
        uint32_t maxBatchSize;  //max size of batch
        uint32_t batchId;   //batch ID
        std::vector<uint32_t> frameId;  //frame id.
        std::vector<uint64_t> timestamp;//time stamp
    };

    template<class Archive>
    void serialize(Archive& ar, AudioBatchInfo& data){
        ar(data.isFirst, data.isLast, data.batchSize, data.maxBatchSize,
                data.batchId, data.frameId, data.timestamp);
    }

    enum AUDIOENCODING{
        PCM_SIGNED = 1, // PCM
        PCM_RESERVED
    };

    //voice data.
    template<class T>
    struct AudioData{
        AUDIOENCODING encode;   //audio format
        uint32_t depth; //bit depth
        uint32_t size;  //size of data
        std::shared_ptr<T> data; //data
    };

    template<class Archive, class T>
    void serialize(Archive& ar, AudioData<T>& data){
        ar(data.encode, data.depth, data.size);

        if (data.size > 0 && data.data.get() == nullptr){
            data.data.reset(new T[data.size]);
        }

        ar(cereal::binary_data(data.data.get(), data.size * sizeof(T)));
    }



    template<class T>
    struct BatchAudioPara{
        AudioBatchInfo info;
        std::vector<AudioData<T>> audio;   //voice data.
    };

    template<class Archive, class T>
    void serialize(Archive& ar, BatchAudioPara<T>& data){
        ar(data.info, data.audio);
    }

public:
    struct Mind_MIC_datasetConfig{
        int soundMode;          // mono or stereo
        int samplerate;          // sample rate
        int sampleNumPerFrame;   // number of sample per frame.
        int bitwidth;            // sample bit depth.

        std::string ToString() const;
    };

public:

    /**
    * @brief   constructor
    */
    Mind_MIC_dataset();

    /**
    * @brief   destructor
    */
    ~Mind_MIC_dataset();

    /**
    * @brief  init config of mic by aiConfig
    * @param [in]  initialized aiConfig
    * @param [in]  modelDesc
    * @return  success --> HIAI_OK ; fail --> HIAI_ERROR
    */
    HIAI_StatusT Init(const hiai::AIConfig& conf,
            const  std::vector<hiai::AIModelDescription>& model_desc) override;


    /**
    * @brief   translate value to string
    * @param [in] value    channel id of camera
    * @return   string translate by value
    */
    static std::string IntToString(int value);

    /**
    * @brief  ingroup hiaiengine
    */
    HIAI_DEFINE_PROCESS(INPUT_SIZE, OUTPUT_SIZE)
private:

    /**
     * create voice object.
     * @return : shared_ptr of data audio
     */
    std::shared_ptr<Mind_MIC_dataset::BatchAudioPara<uint8_t>> CreateBatchAudioParaObj();


    /**
     *  init parameter
     */
    void InitConfigParams();


    /**
    * @brief   preprocess for cap mic
    * @return  mic operation code
    */
    MicOperationCode PreCapProcess();



    /**
     * cap mic
     * @return  success-->true ; fail-->false
     */
    bool DoCapProcess();


    /**
    *  @brief  parse param
    *  @return value of config
    */
    int CommonParseParam(const std::string& val) const;

    /**
     * @brief  get exit flag
     * @return the value of exit
     */
   int GetExitFlag();

    /**
     * set exit flag.
     */
    void SetExitFlag(int flag = MICDATASETS_STOP);

private:
    typedef std::unique_lock<std::mutex> TLock;
    std::shared_ptr<Mind_MIC_datasetConfig> config;
    std::map<std::string, std::string> params;
    uint32_t frameId;
    std::mutex mutex;
    int exit; // 0 -init ,1- exit for exited.
};

#endif
