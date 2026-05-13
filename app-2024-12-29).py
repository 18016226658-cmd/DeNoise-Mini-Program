from flask import Flask, jsonify, request,send_from_directory
from flask_cors import CORS
f = Flask(__name__)

app = f
CORS(app, origins='*')  # 允许所有域的请求，生产环境中应限制为特定的域

# app.config['SERVER_NAME'] = 'test.com:5000'

import datetime
import time
import pymysql.cursors
import pandas as pd
import json
import random
import jieba
from tkinter import _flatten

import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
import warnings
warnings.filterwarnings("ignore")
import requests
import os
from pydub import AudioSegment
from urllib.parse import urlparse
import shutil
import mutagen   #获取音频文件的 标题和艺术集
# import spleeter

data_bj = 0
Upload_bj = 0
RemoteRun_bj = 0
Movies_bj = 0
Download_bj = 0
GPT_bj = 0

JVM_BJ = 0

# 测试用数据
UserID = 1001
UserName = '王小明'
ChatTime =  datetime.datetime.now()
Gender = '男'
Birthday = '2001-10-11'

FaceImg =''
n_channels = ''
# 当前日期：年-月-日
now = datetime.date.today()


# 配置你的服务器以允许更大的文件上传和下载（如果需要的话）
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024  # 16MB

# 用于存储临时文件的目录（确保这个目录存在并且有写权限）
# TEMP_DIR = '/path/to/your/temp/dir'
TEMP_DIR ='Audio\download'   # save 分离的人声和背景声文件
WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a/'
os.makedirs(TEMP_DIR, exist_ok=True)

from tempfile import NamedTemporaryFile

from pydub import AudioSegment  # 用于处理音频文件
import wave  # 用于读取和写入WAV格式的音频文件
import numpy as np  # 用于数值计算
from scipy.signal import butter, filtfilt  # 用于设计数字滤波器和应用滤波器


import openai
import os
from aip import AipSpeech

import subprocess
import shutil

# def butter_bandpass(lowcut, highcut, fs, order=5):
#     # 计算奈奎斯特频率（采样频率的一半）
#     nyquist = 0.5 * fs
#     # 将截止频率转换为归一化频率
#     low = lowcut / nyquist
#     high = highcut / nyquist
#     # 设计带通滤波器，返回滤波器的系数
#     b, a = butter(order, [low, high], btype='band')
#     return b, a

'''
基于巴特沃斯（Butterworth）滤波器时，order（阶数）是一个关键参数，它决定了滤波器的性能特征。阶数越高，
滤波器的滚降特性（即滤波器从通带到阻带的过渡区域）越陡峭，但这也可能导致相位失真增加。因此，在选择阶数时需要权衡这两个因素。
order=5是一个默认参数值，意味着使用五阶巴特沃斯滤波器。这个选择通常是基于经验或者特定的应用需求。在某些情况下，可能需要尝试不同的阶数以找到最佳的滤波效果。
'''

def butter_bandpass(lowcut, highcut, fs, order=5):
    # 计算奈奎斯特频率（采样频率的一半）
    nyquist = 0.5 * fs
    # 将截止频率转换为归一化频率
    low = lowcut / nyquist
    high = highcut / nyquist
    # 设计带通滤波器，返回滤波器的系数
    b, a = butter(order, [low, high], btype='band')  # butter 函数用于设计一个指定阶数、低截止频率和高截止频率的巴特沃斯带通滤波器

    '''
    butter 函数的一般形式
    b, a = butter(N, Wn, btype='low', analog=False, output='ba')
    N：滤波器的阶数。在您的代码中，这个参数由 order 变量提供。阶数越高，滤波器在截止频率处的滚降越陡峭，但相位失真也可能越大。
    Wn：归一化截止频率。在您的代码中，这个参数由 [low, high] 提供，其中 low 和 high 是相对于奈奎斯特频率（Nyquist frequency，即采样频率的一半）的归一化低截止频率和高截止频率。
    btype：滤波器的类型。可以是 'low'（低通）、'high'（高通）、'band'（带通）或 'bandstop'（带阻）。在您的代码中，这个参数被设置为 'band'，表示设计的是一个带通滤波器。
    analog：如果为 True，则返回一个模拟滤波器；如果为 False（默认值），则返回一个数字滤波器。
    output：输出类型。'ba'（默认值）表示返回滤波器的分子（b）和分母（a）系数，这些系数定义了滤波器的传递函数。其他选项可能包括 'zpk'（零极点增益形式）或 'sos'（第二阶节形式）。
    '''

    return b, a  # 返回的是巴特沃斯滤波器的系数。b是分子系数，a是分母系数。这些系数定义了滤波器的传递函数。在数字信号处理中，滤波器的传递函数通常表示为有理函数


# 定义应用滤波器的函数
# def bandpass_filter(data, lowcut, highcut, fs, order=5):
#     # 使用前面定义的函数设计带通滤波器
#     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#     # 应用滤波器到数据上，返回滤波后的数据
#     y = filtfilt(b, a, data)
#     return y

# 定义应用滤波器的函数
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    # 使用前面定义的函数设计带通滤波器
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    # 应用滤波器到数据上，返回滤波后的数据
    y = filtfilt(b, a, data)
    # filtfilt函数通过先对数据进行前向滤波，然后进行后向滤波（即反向通过相同的滤波器），来消除由于滤波器引起的相位失真。
    # 这种方法的一个缺点是它会导致数据边缘的效应，因为数据在边缘处没有被完全对称地滤波。然而，在许多应用中，这种边缘效应是可以接受的，
    # 因为滤波后的数据中心部分通常是最感兴趣的。
    return y #返回的是经过滤波器处理后的数据。y是滤波后的数据数组，它与输入数据data具有相同的形状。这个数组包含了原始数据通过巴特沃斯带通滤波器后的结果

# 能自动检测单声道和立体声，如果是立体声 ，会对左右二个声道分别降噪，再合成
def DeNoise_all(input_file,output_file,new_filename):
    global n_channels
    print("==================== 7-1  DeNoise_all(input_file,output_file)")
    # 使用pydub加载音频文件
    audio = AudioSegment.from_file(input_file, format="wav")

    # 将音频文件导出为临时WAV文件，以便后续使用wave模块读取
    temp_wav_file = "temp_audio.wav"
    temp_wav_file1 = "temp_audio1.wav"
    temp_wav_file2 = "temp_audio2.wav"

    audio.export(temp_wav_file, format="wav")

    # 使用wave模块读取WAV文件
    with wave.open(temp_wav_file, 'rb') as wav_file:

        # 获取音频文件的参数：声道数、采样宽度、采样率、帧数
        params = wav_file.getparams()
        n_channels, sampwidth, fs, n_frames = params[:4]
        # 读取音频帧数据
        audio_bytes = wav_file.readframes(n_frames)
        print("==================== 7-2   n_channels, sampwidth, fs,")
        print(n_channels)
        print(sampwidth)
        print( fs)

        # 根据采样宽度将音频数据转换为NumPy数组
        # 这里假设采样宽度为2（16位PCM），对应的数据类型为np.int16
        if sampwidth == 2:
            dtype = np.int16
        elif sampwidth == 4:  # 虽然这个分支在代码中，但后续并未处理32位PCM的情况
            dtype = np.int32
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth}")
        # 将音频字节数据转换为NumPy数组
        data = np.frombuffer(audio_bytes, dtype=dtype)

        # 完整的文件路径
        full_path = output_file

        # 使用 os.path.split 分离目录和文件名
        directory, file_name_with_extension = os.path.split(full_path)

        # 使用 os.path.splitext 分离文件名和扩展名
        file_name_without_extension, Fextension = os.path.splitext(file_name_with_extension)

        # 重新组合路径（如果需要的话）
        new_path = os.path.join(directory, file_name_without_extension)

        # 输出新的路径
        print(new_path)

        if n_channels == 2:
            print("==================== 7-3  n_channels == 2 ")
            left_channel_data = data[::2]
            right_channel_data = data[1::2]
            print("==================== 7-4   DeNoise_mono(left_channel_data, temp_wav_file2,fs)")
            DeNoise_mono(left_channel_data, temp_wav_file2,fs,dtype)
            print("==================== 7-5   DeNoise_mono(right_channel_data, temp_wav_file1,fs)")
            DeNoise_mono(right_channel_data, temp_wav_file1,fs,dtype)
            print("==================== 7-6   merge_mono_to_stereo(file1, file2, output_file)")



            # 输出新的路径
            new_output_file = new_path + '-stereo.wav'
            mono_stereo_flinename = file_name_without_extension + '-stereo.wav'
            print(new_output_file)

            merge_mono_to_stereo(temp_wav_file1, temp_wav_file2, new_output_file)
            os.remove(temp_wav_file1)
            os.remove(temp_wav_file2)
            print("==================== 7-7   os.remove(temp_wav_file1)  os.remove(temp_wav_file2) ")

        if n_channels == 1:
            # 输出新的路径  mono_to_stereo
            new_output_file = new_path + '-mono.wav'
            mono_stereo_flinename = file_name_without_extension + '-mono.wav'
            print(new_output_file)
            print("==================== 7-8  n_channels == 1 ")
            left_channel_data = data[::2]
            DeNoise_mono(left_channel_data, new_output_file,fs)
            print("==================== 7-9 DeNoise_mono(left_channel_data, new_output_file,fs)  end ")
    os.remove(temp_wav_file)
    # result = {"success": 1, "files": mono_stereo_flinename}
    result = {}
    response = jsonify(result)
    response.data =mono_stereo_flinename
    response.n_channels = n_channels
    response.status_code = 200  # 设置状态码为 200
    return response
    # return 200

# 单个声道降噪 ， 原始数据：data  输出结果：output_file
def DeNoise_mono(data,output_file,fs,dtype):
    try:
        print('===================DeNoise_mono    ============= 1')
        # 将音频文件导出为临时WAV文件，以便后续使用wave模块读取
        # temp_wav_file = "temp_audio.wav"
        # audio.export(temp_wav_file, format="wav")

        # 应用带通滤波器进行降噪处理
        # 注意：这里的lowcut和highcut需要根据实际情况进行调整
        data_filtered = bandpass_filter(data, lowcut=100, highcut=3000, fs=fs)
        print(data_filtered)
        print('===================DeNoise_mono    ============= 2')
        # 将处理后的NumPy数组数据转换回音频字节数据
        # 这里需要将数据类型转换回原始的采样宽度对应的数据类型
        audio_bytes_filtered = data_filtered.astype(dtype).tobytes()

        # 使用wave模块将处理后的音频数据写入新的WAV文件
        # with wave.open("output_audio_reduced_noise.wav", 'wb') as wav_file:
        print('===================DeNoise_mono  output_file  ============= 3')
        print(output_file)
        with wave.open(output_file, 'wb') as wav_file:

            # 设置音频文件的参数：声道数（这里设置为单声道）、采样宽度、采样率、帧数、压缩类型和压缩名称
            # 注意：这里将声道数设置为1，因为前面的处理只保留了一个声道的数据
            n_channels = 1
            sampwidth = 2  # 16位PCM
            n_frames = len(data_filtered)
            comptype = "NONE"  # 不压缩
            compname = "not compressed"

            # 设置音频文件的参数
            wav_file.setparams((n_channels, sampwidth, fs, n_frames, comptype, compname))
            # 写入音频帧数据
            wav_file.writeframes(audio_bytes_filtered)

        # 可选步骤：删除临时文件以节省磁盘空间
        # import os
        # os.remove(temp_wav_file)
        print('===================DeNoise_mono   4    200')
        return 200
    except Exception as e:
        print("====================12 except Exception as e :500")
        print(e)
        return 400


# def DeNoise(input_file,output_file):    #替换为 DeNoise_all
#     try:
#         # 导入必要的库
#         # from pydub import AudioSegment  # 用于处理音频文件
#         # import wave  # 用于读取和写入WAV格式的音频文件
#         # import numpy as np  # 用于数值计算
#         # from scipy.signal import butter, filtfilt  # 用于设计数字滤波器和应用滤波器
#
#         # input_file = r'E:\mp3\mp3\aa1.wav'
#         # input_file = r'九儿_G调_双声道.wav'
#         #
#         # output_file = r'E:\mp3\mp3\output_audio_reduced_noise-九儿.wav'
#
#         # 定义带通滤波器的设计函数
#
#
#         # 使用pydub加载音频文件
#         audio = AudioSegment.from_file(input_file, format="wav")
#
#         # 将音频文件导出为临时WAV文件，以便后续使用wave模块读取
#         temp_wav_file = "temp_audio.wav"
#         audio.export(temp_wav_file, format="wav")
#
#         # 使用wave模块读取WAV文件
#         with wave.open(temp_wav_file, 'rb') as wav_file:
#             # 获取音频文件的参数：声道数、采样宽度、采样率、帧数
#             params = wav_file.getparams()
#             n_channels, sampwidth, fs, n_frames = params[:4]
#
#             # 读取音频帧数据
#             audio_bytes = wav_file.readframes(n_frames)
#
#             # 根据采样宽度将音频数据转换为NumPy数组
#             # 这里假设采样宽度为2（16位PCM），对应的数据类型为np.int16
#             if sampwidth == 2:
#                 dtype = np.int16
#             elif sampwidth == 4:  # 虽然这个分支在代码中，但后续并未处理32位PCM的情况
#                 dtype = np.int32
#             else:
#                 raise ValueError(f"Unsupported sample width: {sampwidth}")
#
#             # 将音频字节数据转换为NumPy数组
#             data = np.frombuffer(audio_bytes, dtype=dtype)
#
#             # 如果音频是立体声（双声道），则只取一个声道（例如左声道）的数据进行处理
#             # 这里通过切片操作取data数组中的偶数索引元素（假设立体声数据是交替存储的）
#             if n_channels == 2:
#                 data = data[::2]
#
#         # 应用带通滤波器进行降噪处理
#         # 注意：这里的lowcut和highcut需要根据实际情况进行调整
#         data_filtered = bandpass_filter(data, lowcut=100, highcut=3000, fs=fs)
#
#         # 将处理后的NumPy数组数据转换回音频字节数据
#         # 这里需要将数据类型转换回原始的采样宽度对应的数据类型
#         audio_bytes_filtered = data_filtered.astype(dtype).tobytes()
#
#         # 使用wave模块将处理后的音频数据写入新的WAV文件
#         # with wave.open("output_audio_reduced_noise.wav", 'wb') as wav_file:
#         with wave.open(output_file, 'wb') as wav_file:
#
#             # 设置音频文件的参数：声道数（这里设置为单声道）、采样宽度、采样率、帧数、压缩类型和压缩名称
#             # 注意：这里将声道数设置为1，因为前面的处理只保留了一个声道的数据
#             n_channels = 1
#             sampwidth = 2  # 16位PCM
#             n_frames = len(data_filtered)
#             comptype = "NONE"  # 不压缩
#             compname = "not compressed"
#
#             # 设置音频文件的参数
#             wav_file.setparams((n_channels, sampwidth, fs, n_frames, comptype, compname))
#             # 写入音频帧数据
#             wav_file.writeframes(audio_bytes_filtered)
#
#         # 可选步骤：删除临时文件以节省磁盘空间
#         # import os
#
#         os.remove(temp_wav_file)
#         return 200
#     except:
#         return 0


# 降噪处理
@app.route('/api/DeNoiseAudio', methods=['POST'])
def DeNoiseAudio():
    global n_channels
    try:
        print("==================== 0 DeNoiseAudio")
        data = request.get_json()  # 解析 JSON 数据
        audioPath = data.get("audioPath")      # http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav
        file_path = data.get("filePath")       # http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav
        fileSize = data.get("fileSize")        # 0.00
        duration = data.get("duration")        # 00:00:00
        orgFileName= data.get("orgFileName")   # 古城之恋-和文军丽江 礼物.wav
        filename = data.get("filename")        # nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07
        extension = data.get("extension")      # wav
        title = data.get("title")              # 空白
        artist = data.get("artist")            # 空白
        album = data.get("album")              # 空白

        print("==================== 1 接收小程序传递过来的信息：")
        print(audioPath)
        print(file_path)
        print(fileSize)
        print(duration)
        print(orgFileName)
        print(filename)
        print(extension)
        print(title)
        print(artist)
        print(album)

        if not file_path:
            print("==================== 2 not file_path")
            return jsonify({"error": "No file path provided"}), 400

        # 解析文件路径（这里假设 filePath 是相对于某个基础路径的）
        # 注意：这里假设 filePath 是服务器上的相对路径，而不是小程序中的路径
        # 你需要根据实际情况调整这部分逻辑
        # WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a/'
        tt = file_path[7:]
        print("==================== 3 DeNoiseAudio tt")
        print(tt)

        input_file = WX_TEMP_DIR + tt
        print("==================== 3 input_file")
        print(input_file)
        if not os.path.exists(input_file):
            print("==================== 4 not os.path.exists(input_file)")
            return jsonify({"error": "File not found"}), 404



        ################################################
        # 使用 os.path.splitext 分离文件名和扩展名
        orgFileName_Main, orgFileName_extension = os.path.splitext(orgFileName)
        myTitle0 = '(DeNoise).wav'

        # 生成降噪后的音频文件名，因为要在微信小程序中用 audio组件播放，不能带中文字符，new_filename能保证不会重复
        new_filename = filename + '-' + myTitle0  # nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07-(DeNoise).wav
        print(new_filename)

        # 下载文件到服务器上的临时位置
        try:
            print(" DeNoise_audio()============================ 2")

            # 使用 os.path.join 构建路径
            output_file = os.path.join(WX_TEMP_DIR, 'usr', 'Audio', 'output', 'DeNoise', new_filename)

            # 打印结果
            print("====================================================================================== 2-3")
            print(output_file)

            # 调用降噪程序
            # res=DeNoise(input_file, output_file)
            res = DeNoise_all(input_file, output_file,new_filename)
            print(" +++++++++++++++++++++++++++++++++++++++  1   ++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(res)
            print( res.data)
            # 如果你知道字节序列的编码（如UTF-8），你可以使用.decode()方法将其转换为字符串
            # combined = bytes_data.decode('utf-8') + str_data
            str_mono_stereo_filename = res.data.decode('utf-8')
            if res.status_code == 200:

            # if res==200:
                print(" ++++++++++++++++++++++++++++++++++++++  2  +++++++++++++++++++++++++++++++++++++++++++++++++++++")
                # result = {"success": 1, "files": str_mono_stereo_filename}

                DeNoisePath = r"http://usr/Audio/output/DeNoise/" + str_mono_stereo_filename
                # 'vYHTMGvvv04b21f6caffe0ef74c97742eef4a3038f07-(DeNoise)-stereo.wav'
                print(DeNoisePath)

                DeNoiseOK = '1'

                # print("==================== 5 result")
                # print(result)

                str_fileSize =str(fileSize)
                str_n_channels = n_channels
                if not isinstance(n_channels, str):
                    str_n_channels =str(n_channels)
                # // 将音频信息保存在mydata 变量中
                mydata = audioPath+"\n"  + file_path + "\n" + str_fileSize+ "\n" + duration + "\n" + orgFileName + "\n"+ filename + "\n"  + extension + "\n" + DeNoisePath+ "\n"  +str_n_channels+ "\n" +   DeNoiseOK
                # // 观察mydata
                print(mydata)

                # 要写入的字符串
                text_to_write = mydata
                AudioInfo_File = WX_TEMP_DIR + '/usr/DeNoiseInfo.txt'
                # 使用 open() 函数打开文件（如果文件不存在，将会创建它）
                # 'w' 模式表示写入（会覆盖文件内容，如果文件已存在）
                # 'a' 模式表示追加（会在文件末尾添加内容，如果文件已存在）
                # 'x' 模式表示创建新文件（如果文件已存在，操作会失败）
                with open(AudioInfo_File, 'w', encoding='utf-8') as file:
                    # 使用 write() 方法将字符串写入文件
                    file.write(text_to_write)
                #########################################
                # 构造一个字典 Dict 型数据
                data = {
                    "success": 1,
                    "files": str_mono_stereo_filename,
                    'n_channels':n_channels,
                }
                print(data)
                # 转为json
                res_json = json.dumps(data)

                # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
                # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
                return res_json, 200, {"Content-Type": "application/json"}

                #########################################
                # result = {"success": 1, "files": str_mono_stereo_filename}
                #
                # response = jsonify(result)
                # response.status_code = 200  # 设置状态码为 200
                # return response
                # return jsonify(result), 200
            else:
                response = jsonify({"error": "0"})
                response.status_code = 401  # 设置状态码为 401
                return response
                # return jsonify({"error": "0"}), 401
        except Exception as e:
            print("==================== 6 except Exception as e")
            print(e)
            response = jsonify({"error": str(e)})
            response.status_code = 402  # 设置状态码为 401
            return response

            # return jsonify({"error": str(e)}), 402

    except Exception as e:
        print("==================== 7 except Exception as e")
        print(e)
        response = jsonify({"error": str(e)})
        response.status_code = 500  # 设置状态码为 500
        return response
        # return jsonify({"error": str(e)}), 500

#下面是将二个单声道的音频合并成一个立体声的音频
# 读取 file_path 路径的音频文件
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        audio_bytes = wav_file.readframes(num_frames)
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)  # Assuming 16-bit samples

        if num_channels != 1:
            raise ValueError("The input WAV file is not mono (single channel).")

        return frame_rate, audio_data

# 将音频文件写到file_path 文件中
def write_wav(file_path, frame_rate, num_channels, sample_width, audio_data):

    print("================== write_wav 1")
    num_frames = len(audio_data) // num_channels
    audio_bytes = audio_data.tobytes()
    print("================== write_wav 2")
    print(file_path)
    print(frame_rate)
    print(num_channels)
    print(sample_width)
    print(audio_data)

    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(audio_bytes)
    print('================== write_wav 3')

# 将2个单声道合并为立体声
def merge_mono_to_stereo(file1, file2, output_file):
    print("============================== erge_mono_to_stereo  1")
    frame_rate1, audio_data1 = read_wav(file1)
    frame_rate2, audio_data2 = read_wav(file2)
    print(frame_rate1)
    print(frame_rate2)
    print("============================== erge_mono_to_stereo  2")
    if frame_rate1 != frame_rate2:
        print("=========================   frame_rate1 != frame_rate2     3")
        raise ValueError("The frame rates of the two WAV files do not match.")

    print("============================== erge_mono_to_stereo  4")
    min_length = min(len(audio_data1), len(audio_data2))
    audio_data1 = audio_data1[:min_length]
    audio_data2 = audio_data2[:min_length]

    # Merge into stereo (L, R)
    stereo_audio_data = np.column_stack((audio_data1, audio_data2))
    stereo_audio_data = stereo_audio_data.flatten()
    print("============================== erge_mono_to_stereo  5")
    # Write the stereo WAV file
    sample_width = 2  # 2 bytes per sample for 16-bit
    write_wav(output_file, frame_rate1, 2, sample_width, stereo_audio_data)
    print("============================== erge_mono_to_stereo  6")
    print(output_file)




@app.route('/api/DownloadDeNoise', methods=['POST'])
def DownloadDeNoise():
    print(" download_audio()============================ 1")
    file_url = request.json.get('file_url')
    print(file_url)
    if not file_url:
        response = jsonify({'success': False, 'message': 'File URL is required'})
        response.status_code = 400  # 设置状态码为 400
        return response

        # return jsonify({'success': False, 'message': 'File URL is required'}), 400

    filename = request.json.get('filename')
    title = request.json.get('title')
    print(filename)
    print(len(filename))
    # 去掉文件名存在非法的特殊不可见，如\n 空格等
    filename = filename.rstrip()
    print(len(filename))
    print(title)
    print(len(filename))


    DeNoiseFile = request.json.get('DeNoiseFile')
    # 'ESxnOW7QiUYFc22f2844135ada275fed69f46d9e4c0b-(DeNoise)-stereo.wav'
    print(DeNoiseFile)

    str2 = DeNoiseFile[55:]  #stereo.wav  or  mono.wav

    orgFileName = request.json.get('orgFileName')
    print(orgFileName)
    # 使用 os.path.splitext 分离文件名和扩展名
    orgFileName_Main, orgFileNam_extension = os.path.splitext(orgFileName)

    # 输出文件主名称
    print(orgFileName_Main)   # 古城之恋-和文军丽江 礼物
    print(orgFileNam_extension)

    myTitle0 = 'DeNoise(降噪)-'+ str2   # DeNoise(降噪)-stereo.wav   or   DeNoise(降噪)-mono.wav
    print(len(orgFileName_Main))

    # 如果原始音频文件名称为空白
    if not orgFileName_Main:
        myTitle = myTitle0                # DeNoise(降噪)-stereo.wav
    else:
        myTitle = orgFileName_Main + '-' + myTitle0  # 古城之恋-和文军丽江 礼物-DeNoise(降噪)-stereo.wav
    print(myTitle)

    # 下载文件到服务器上的临时位置
    try:
        print(" download_audio()============================ 2")
        # 获取当前日期和时间，并格式化为所需的字符串格式
        current_time = datetime.datetime.now().strftime("%Y-%m-%d--%H:%M:%S")
        current_time = current_time.replace(":", "-")
        print(" download_audio()============================ 2-1")
        # 原始文件名
        original_filename = myTitle

        # 生成新的文件名

        new_filename = f'{current_time}-{original_filename}'      # 2024-12-28--09-48-15-古城之恋-和文军丽江 礼物-DeNoise(降噪)-stereo.wav
        print(" download_audio()============================ 2-2")
        # 打印新文件名以验证
        print(new_filename)


        input_File = os.path.join(WX_TEMP_DIR, 'usr', 'Audio', 'output', 'DeNoise', DeNoiseFile)
        # C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a / usr\Audio\output\DeNoise\wIEKxGHF2Lgc21f6caffe0ef74c97742eef4a3038f07 - (DeNoise).wav
        # 打印结果
        print("====================================================================================== 2-3")


        output_File = r'D:/WxMinPro/Audio/download/DeNoise/' + new_filename
        # D:/WxMinPro/ Audio/download/DeNoise/2024-12-28--09-48-15-古城之恋-和文军丽江 礼物-DeNoise(降噪).wav


        print(input_File)
        print(output_File)

        # 使用shutil.copy()函数复制文件
        try:
            print(" download_audio()============================ 4")
            shutil.copy(input_File, output_File)
            print(f'降噪音频文件已成功下载到 {output_File}')
            # 你可以在这里清理旧文件、限制文件访问时间等
            # ...
            print(" download_audio()============================ 5")

            response = jsonify({'success': True, 'temp_file_path': output_File})
            response.status_code = 200  # 设置状态码为 200
            return response

            # return jsonify({'success': True, 'temp_file_path': output_File}), 200

        except Exception as e:
            print(" download_audio()============================ 6")
            print(f'下载降噪音频文件时出错: {e}')
            response = jsonify({'success': False, 'message': str(e)})
            response.status_code = 400  # 设置状态码为 200
            return response

            # return jsonify({'success': False, 'message': str(e)}), 400


    except requests.RequestException as e:
        print(" download_audio()============================ 7")
        response = jsonify({'success': False, 'message': str(e)})
        response.status_code = 500  # 设置状态码为 200
        return response
        # return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/downloadAudio', methods=['POST'])
def download_audio():
    print(" download_audio()============================ 1")
    file_url = request.json.get('file_url')
    print(file_url)
    if not file_url:
        response = jsonify({'success': False, 'message': 'File URL is required'})
        response.status_code = 400  # 设置状态码为 400
        return response

        # return jsonify({'success': False, 'message': 'File URL is required'}), 400

    filename = request.json.get('filename')
    title = request.json.get('title')
    print(filename)
    print(len(filename))
    # 去掉文件名存在非法的特殊不可见，如\n 空格等
    filename = filename.rstrip()
    print(len(filename))
    print(title)
    print(len(filename))


    audioType = request.json.get('audioType')
    print(audioType)

    if audioType=='vocals':
        myTitle0 = 'vocals(人声).wav'
    elif audioType=='other':
        myTitle0 = 'other(伴奏).wav'
    elif  audioType=='drums':
        myTitle0 = 'drums(鼓).wav'
    elif audioType=='bass':
        myTitle0 = 'bass(贝斯).wav'
    else:
        myTitle0 = 'DeNoise(降噪).wav'

    # 标题为空或只包含空白字符
    if not title:
        myTitle = myTitle0
    else:
        myTitle = title + '-'+ myTitle0
    print(myTitle)


    # 下载文件到服务器上的临时位置
    try:
        print(" download_audio()============================ 2")
        # 获取当前日期和时间，并格式化为所需的字符串格式
        current_time = datetime.datetime.now().strftime("%Y-%m-%d--%H:%M:%S")
        current_time = current_time.replace(":", "-")
        print(" download_audio()============================ 2-1")
        # 原始文件名
        original_filename = myTitle

        # 生成新的文件名

        new_filename = f'{current_time}-{original_filename}'
        print(" download_audio()============================ 2-2")
        # 打印新文件名以验证
        print(new_filename)

        waveFile =f'{audioType}.wav'

        # WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a'
        # filename2 = 'T46KsF7llS9g0dad379fb7f5771a294f3f9d2b25f045'
        # print(len(filename2))

        # 使用 os.path.join 构建路径
        # SeparateAudio_File = os.path.join(WX_TEMP_DIR, 'usr', 'Audio', 'output', 'htdemucs', filename, 'vocals.wav')
        SeparateAudio_File = os.path.join(WX_TEMP_DIR, 'usr', 'Audio', 'output', 'htdemucs', filename, waveFile)

        # 打印结果
        print("====================================================================================== 2-3")
        print(SeparateAudio_File)


        # SeparateAudio_File = os.path.join(WX_TEMP_DIR, 'usr', 'Audio', 'output', 'htdemucs', filename, 'vocals.wav')
        # 注意：如果 filename 应该包含扩展名之前的部分，请确保它已正确设置
        # 例如：filename = 'somefile' 而不是 'somefile.somethingelse'（除非那是您想要的）
        # SeparateAudio_File = WX_TEMP_DIR + r'usr/Audio/output/htdemucs/' + filename +r'\vocals.wav'

        Download_File = r'D:/WxMinPro/Audio/download/Separate/' + new_filename
        # Download_File = r'.\Audio/download/' + new_filename

        print(" downloadAudio()============================ 3")
        print(SeparateAudio_File)
        print(Download_File)

        # 使用shutil.copy()函数复制文件
        try:
            print(" download_audio()============================ 4")
            shutil.copy(SeparateAudio_File, Download_File)
            print(f'文件已成功从 {SeparateAudio_File} 下载到 {Download_File}')
            # 你可以在这里清理旧文件、限制文件访问时间等
            # ...
            print(" download_audio()============================ 5")
            response = jsonify({'success': True, 'temp_file_path': Download_File})
            response.status_code = 200
            return response

            # return jsonify({'success': True, 'temp_file_path': Download_File}), 200

        except Exception as e:
            print(" download_audio()============================ 6")
            print(f'下载{waveFile}文件时出错: {e}')
            response = jsonify({'success': False, 'message': str(e)})
            response.status_code = 400
            return response

            # return jsonify({'success': False, 'message': str(e)}), 400


    except requests.RequestException as e:
        print(" download_audio()============================ 7")
        jsonify({'success': False, 'message': str(e)})
        response.status_code = 500
        return response

        # return jsonify({'success': False, 'message': str(e)}), 500


# 分离音频文件中的人声和背景音乐
# import subprocess
def run_demucs(input_file, output_dir, model="htdemucs", device="cpu"):    #mdx_extra 和 htdemucs
    command = [
        "demucs",                         #"python", "-m", "demucs.separate",
        "-n", model,
        "--out", output_dir,             #  htdemucs  htdemucs_6s  mdx  mdx_extra
        "--device", device ,             # 如果有GPU 可以选择 cuda
        input_file
    ]

    try:
        # result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')  # 不显示进度条
        result = subprocess.run(command)   # 显示进度条
        print("Demucs ran successfully!")
        print("Output1:", result)
        print("Output2:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running Demucs:", e)
        print("Output:", e.stdout)
        print("Error Output:", e.stderr)
        raise  # 重新抛出异常，以便 Flask 处理

@app.route('/api/separateAudio', methods=['POST'])
def separateAudio():
    try:
        print("==================== 0 separateAudio")
        data = request.get_json()  # 解析 JSON 数据
        audioPath = data.get("audioPath")
        # AudioFilePath = data.get("AudioFilePath")
        file_path = data.get("filePath")
        fileSize = data.get("fileSize")
        duration = data.get("duration")
        filename = data.get("filename")
        extension = data.get("extension")

        title = data.get("title")
        artist = data.get("artist")
        album = data.get("album")

        print("==================== 1 接收小程序传递过来的信息：")
        print(audioPath)
        # print(AudioFilePath)
        print(file_path)
        print(fileSize)
        print(duration)
        print(filename)
        print(extension)
        print(title)
        print(artist)
        print(album)

        if not file_path:
            print("==================== 2 not file_path")
            return jsonify({"error": "No file path provided"}), 400

        # 解析文件路径（这里假设 filePath 是相对于某个基础路径的）
        # 注意：这里假设 filePath 是服务器上的相对路径，而不是小程序中的路径
        # 你需要根据实际情况调整这部分逻辑
        # WX_TEMP_DIR = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a/'
        tt = file_path[7:]
        print("==================== 3 separateAudio tt")
        print(tt)

        input_file = WX_TEMP_DIR + tt
        print("==================== 3 input_file")
        print(input_file)
        if not os.path.exists(input_file):
            print("==================== 4 not os.path.exists(input_file)")
            return jsonify({"error": "File not found"}), 404


        output_dir = WX_TEMP_DIR + '/usr/Audio/output'
        run_demucs(input_file, output_dir)
        result = {"success": 1, "files": output_dir}

        vocalsPath = r"http://usr/Audio/output/htdemucs/"+filename+r'/vocals.wav'
        otherPath = r"http://usr/Audio/output/htdemucs/"+filename+r'/other.wav'
        drumsPath = r"http://usr/Audio/output/htdemucs/"+filename+r'/drums.wav'
        bassPath = r"http://usr/Audio/output/htdemucs/"+filename+r'/bass.wav'
        separatedOK = '1'

        print("==================== 5 result")
        print(result)

        str_fileSize =str(fileSize)

        # // 将音频信息保存在mydata 变量中
        mydata = audioPath+"\n"  + file_path + "\n" + str_fileSize+ "\n" + duration + "\n" + filename + "\n"  + extension + "\n" + vocalsPath+ "\n" + otherPath + "\n"+ drumsPath + "\n"+bassPath + "\n"+ title+  "\n"+ artist  +  "\n"+ album +  "\n"+  separatedOK
        # // 观察mydata
        print(mydata)

        # 要写入的字符串
        text_to_write = mydata
        AudioInfo_File = WX_TEMP_DIR + '/usr/AudioInfo.txt'
        # 使用 open() 函数打开文件（如果文件不存在，将会创建它）
        # 'w' 模式表示写入（会覆盖文件内容，如果文件已存在）
        # 'a' 模式表示追加（会在文件末尾添加内容，如果文件已存在）
        # 'x' 模式表示创建新文件（如果文件已存在，操作会失败）
        with open(AudioInfo_File, 'w', encoding='utf-8') as file:
            # 使用 write() 方法将字符串写入文件
            file.write(text_to_write)

        # 当 with 语句块结束时，文件会自动关闭
        # 无需手动调用 file.close()
        # // 将mydata数据写到wx.env.USER_DATA_PATH的AudioInfo.txt中

        #  2024 - 12 - 24修改End

        return jsonify(result), 200
    except Exception as e:
        print("==================== 6 except Exception as e")
        print(e)
        return jsonify({"error": str(e)}), 500



def separate_audio():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    separator = spleeter.separator.Separator('spleeter:2stems')
    separator.separate_to_file(filepath, os.path.join(SEPARATED_FOLDER, os.path.splitext(filename)[0]))

    separated_files = [
        {'path': f'/separated/{os.path.splitext(filename)[0]}/vocals.wav', 'type': '人声'},
        {'path': f'/separated/{os.path.splitext(filename)[0]}/instrumental.wav', 'type': '背景音乐'}
    ]

    return jsonify({'success': True, 'files': separated_files})

@app.route('/separated/<path:path>')
def send_separated_file(path):
    return send_from_directory(SEPARATED_FOLDER, path)



UPLOAD_FOLDER = './Audio/uploads'
SEPARATED_FOLDER = './Audio/input'
SEPARATED_FOLDER = 'separated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SEPARATED_FOLDER, exist_ok=True)

def get_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    duration_sec = duration_ms / 1000.0
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    return {
        'fileSize': file_size_mb,
        'duration': duration_sec
    }

# import requests
# 获取音频文件的大学和播放时长
@app.route('/api/getAudioInfo', methods=['POST'])
def getAudioInfo():
    print("==================== 1 getAudioInfo   filePath")
    file = request.form.get("filePath")
    print(file)
    filename = request.form.get("filename")
    print("==================== 2 getAudioInfo   filename")
    print(filename)
    extension = request.form.get("extension")


    # file = request.files['filePath']

    print("==================== 3 getAudioInfo   extension")
    print(extension)
    # 解析URL
    parsed_url = urlparse(file)
    #
    # 从解析结果中提取路径部分
    path = parsed_url.path
    #
    # # 使用os.path.basename获取文件名
    file_name = os.path.basename(path)
    #
    print(file_name)

    # tmp_FOLDER = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a' + '/tmp/'
    # usr_FOLDER = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a' + '//usr/Audio/'
    tmp_FOLDER = WX_TEMP_DIR + r'/tmp/'
    usr_FOLDER = WX_TEMP_DIR + r'/usr/Audio/'
    tmp_File = os.path.join(tmp_FOLDER, file_name)
    usr_File = os.path.join(usr_FOLDER, file_name)

    # 获取目标目录路径
    destination_dir = os.path.dirname(usr_FOLDER)

    # 如果目标目录不存在，则创建它
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 使用shutil.copy()函数复制文件
    try:
        shutil.copy(tmp_File, usr_File)
        print(f'文件已成功从 {tmp_File} 复制到 {usr_File}')
    except Exception as e:
        print(f'复制文件时出错: {e}')

    UPLOAD_FOLDER=r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a'+'/usr/Audio/'
    # file_path = os.path.join(UPLOAD_FOLDER, file_name)
    file_path = usr_File
    print(file_path)

    #########################################
    # 定义URL和保存路径
    # url = file
    # save_path =file_path

    # # 确保本地目录存在
    # os.makedirs(os.path.dirname(save_path), exist_ok=True)
    #
    # # 发送HTTP请求下载文件
    # response = requests.get(url, stream=True)
    # response.raise_for_status()  # 如果请求出错，这里会抛出HTTPError异常
    #
    # # 将文件内容写入本地文件
    # with open(save_path, 'wb') as f:
    #     for chunk in response.iter_content(chunk_size=8192):
    #         f.write(chunk)
    #
    # print(f"File saved to {save_path}")

    ########################################


    #获取音频时间的标题、艺术创作集、和唱片集名称
    # import mutagen

    # 假设音频文件的路径是 'path/to/your/audiofile.mp3'
    # base_dir = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a\usr\Audio'
    # file_path = base_dir + '/6W3MEnyE02EGe4e19eea79b944154ecd956a82ec714c.ogg'

    # 使用 mutagen.File 来打开音频文件
    audio_file = mutagen.File(usr_File, easy=True)

    # 提取标题、艺术家和专辑名
    title = audio_file.get('title', [None])[0]  # 'title' 标签可能不存在，所以使用列表和 [0] 来获取值或 None
    artist = audio_file.get('artist', [None])[0]
    album = audio_file.get('album', [None])[0]

    # 打印提取的信息
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")


    info = get_audio_info(file_path)
    print(info)
    print(type(info))

    info['fileSize'] = round(info['fileSize'], 2)
    info['duration'] = round(info['duration'], 2)
    info['title'] = title
    info['artist'] = artist
    info['album'] = album
    print(info)
    return jsonify(info)



# 修改聊天仿真模型参数
@app.route('/api/EditCsb', methods=['POST'])
def EditCsb():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',  # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()


    data = request.get_json()
    param1 = int(data.get('MinYear'))
    param2 = int(data.get('MaxYear'))
    param3 = int(data.get('BL'))
    param4 = int(data.get('ManN'))
    param5 = int(data.get('WenmenN'))
    param6 = int(data.get('ChatN'))
    print(f'param1:{param1},param2:{param2},param3:{param3},param4:{param4},param5:{param5},param6:{param6}')

    try:
        sql = f"UPDATE csb  SET MinYear = {param1}, MaxYear = {param2} , BL = {param3} , ManNumber = {param4}, WenmenNumber = {param5}, ChatNumber = {param6} WHERE id='1';"
        print(sql)
        # 执行sql语句
        cursor.execute(sql )
        connect.commit()
        # 关闭连接
        cursor.close()
        connect.close()
        return jsonify({'message': '成功修改聊天仿真模型参数表（Data submitted successfully!）'}), 200
    except Exception as e:
        print(f"修改聊天仿真模型参数表出错:{e}")
        # cursor.rollback()
        cursor.close()
        connect.close()
        return jsonify({'修改聊天仿真模型参数表出错(Error)': str(e)}), 500


# import openai
# import os
# from aip import AipSpeech

def chatGPTTest(question):
    # 指定 OpenAI API 的密钥
    # openai.api_key = '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'
    try:
        print(" 1 ===========================")
        # openai.api_key = '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'
        # openai.api_key ='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'
        openai.api_key ='sk-mG09gWgSCt0J7rT-KIPmC312awJ-QPJ-Fj9sEARXAwT3BlbkFJkYQBy1RWbAbuySA7ll0tUSz7-VBMcwUIoRFUVz4z0A'

        os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"

        # q= [{"role": "user", "content": "你好"}]
        q = [{"role": "user", "content": question}]

        print(" 2 ===========================")

        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=q
        )
        print(" 3 ===========================")
        print(rsp)
        msg = rsp.get("choices")[0]["message"]["content"]
        print(" 4 ===========================")

    except:
        print(" 5 ===========================")
        msg ="调用openAI出错，不能为你提供chat服务！"
    print(" 6 调用openAI ===========================")
    print(msg)
    return msg

# chatGPTTest("苏州在哪里")



FPath = r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
FPath_wx = r'C:\Users\sumeng\AppData\Local\微信开发者工具\User Data\80d774828fc67c7dafc59cd74ce70db0\WeappSimulator\WeappFileSystem\o6zAJs14CMRXnJVl83i3XW2SleZ4\wx76d3fbf0d976784a\usr\SoundRecordFile.mp3'




# import os
# Third-party Library
# from aip import AipSpeech
# 1.将FPath格式文件转为pcm格式文件   单声道  16000采样
# FPath = r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
def get_file_content(filePath):
    # 执行cmd命令os.system()
    os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()  # 返回声音文件的2进制数据流

def  waveToText(FPath_wx,FPath):
    # import shutil
    # 定义源文件和目标文件路径（带空格路径）
    # 将录音文件从微信小程序内部空间，copy到指定地方：'/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
    source_path = FPath_wx
    destination_path =r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'

    try:
        # 复制文件
        shutil.copy(source_path, destination_path)
        print(f"文件已成功复制到: {destination_path}")
    except FileNotFoundError:
        print("源文件未找到，请检查路径是否正确。")
        return -1
    except PermissionError:
        print("权限不足，请检查文件访问权限。")
        return -1
    except Exception as e:
        print(f"文件复制失败: {e}")
        return -1
    """ 你的 APPID AK SK """
    APP_ID = '115646617'
    API_KEY = 'DX5dTvydZjEQnKJIXAKNk2Bg'
    SECRET_KEY ='asm9u96ldnwaT5q28aYIpejPQSLhApNX'

    # 与百度进行一次加密校验,认证你是合法用户合法的应用
    # AipSpeech是百度语音的客户端,认证成功之后,客户端将被开启,这里的client就是已经开启的百度语音的客户端了
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 2.将音频转成文字

    # pcmPath =r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.pcm'.encode()
    res = client.asr(get_file_content(FPath), 'pcm', 16000,
                     {
                         'dev_pid': 1537,
                     })
    # 将录音转成文字,然后打印

    print(res.get("result"))
    return res.get("result")[0]






###################################################3
# FPath = r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
# 将在人工智能服务器上生成的 电影推荐结果文件 movies.out 下载到本地
@app.route('/api/RecToText', methods=['POST'])
def RecToText( ):
    print("RecToText")

    msg ="江苏省-测试中"
    # question = "杭州在中国的哪一个省"
    question = waveToText(FPath_wx,FPath)
    print("语音转换为文本："+question)

    data ={'question':question}
    print(data)
    return jsonify(data)



########################################################3

# 本代码DispUser()用于读取注册用户表（users），传给微信小程序 前端
@app.route('/api/DispUser', methods=[ 'POST'])
def DispUser():
    print("================== @app.route('/api/DispUser', methods=[ 'POST']) ============================")

    try:
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',  # 数据库用户名
            passwd='123456',  # 密码
            db='chatGPT',
            charset='utf8'
        )

        # 获取游标
        cursor = connect.cursor()

        sql = "SELECT * from users ;"

        # 执行sql语句
        cursor.execute(sql)

        # 获取所有返回结果
        res = cursor.fetchall()  # 结果是列表套字典

        # 关闭数据库连接
        connect.close()

        listData = []
        print("=========== res =============")
        print(res)
        # 如果非空
        if res:
            # 效验密码(索引0 获取真正的列表里面的字典)
            print("=========== 注册用户信息 res  len(res)  len(res[0])  type(real_dict) real_dict =============")
            print(res)
            print(len(res))
            real_dict = res[0]
            print(len(real_dict))
            print(type(real_dict))  # 'tuple'  原组类型
            print(real_dict)

            # res 的结构如下
            '''
            ((1, '13685153598', 'SM', '123456', datetime.datetime(2024, 2, 22, 18, 48, 39), '男', datetime.date(1964, 9, 4),
              '/static/image/header.png'),
             (2, '13333333333', 'Lisi', '123456', datetime.datetime(2024, 2, 22, 19, 12, 36), '女', datetime.date(1999, 9, 9),
             '/static/image/ala.png'), 
             ......
            )
            '''

            for k in range(0, len(res)):
                real_dict = res[k]
                print(f"第 {k} 个注册用户信息：")
                print(real_dict)
                myid = real_dict[0]
                myPhone = real_dict[1]
                myUserName = real_dict[2]
                myPassword = real_dict[3]
                myRegisterTime = str(real_dict[4])  # 转换为字符串
                myGender = real_dict[5]
                myBirthday = str(real_dict[6])     # 转换为字符串
                myFaceImg = real_dict[7]
                myUserType = real_dict[8]

                # 将数据构造成 字典
                dict1 = {'id':int(k),'UserID':myid, 'Phone': myPhone, 'statu': True,'UserName': myUserName, 'Password': myPassword, 'Gender': myGender,
                         'Birthday': myBirthday, 'RegisterTime': myRegisterTime, 'FaceImg': myFaceImg,'UserType':myUserType}
                # print(dict1)
                # 将一条聊天记录 添加到 列表listData中
                listData.append(dict1)

            print("所有用户信息：")
            print(listData)
            # 转为json
            res_json = json.dumps(listData)

            # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
            # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
            return res_json, 200, {"Content-Type": "application/json"}
        else:
            print("注册表 users 为空！!!!")
            return "1"
    except:
        print("读取 users 失败！!!")
        return "2"



# 本代码SaveUserType()用于 批量删除注册用户
@app.route('/api/SaveUserType', methods=[ 'POST'])
def SaveUserType():
    print("================== @app.route('/api/SaveUserType', methods=[ 'POST']) ============================")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 读取微信小程序前端转递来的数据 （ 修改过的 UserTypeList 和 UserIDList  修改后的用户类型（UserType）列表  与原始 UserID列表
    UserTypeList = request.form.get("UserTypeList")  # “1,2,8,5,5,5”     整个是一个大的字符串
    UserIDList = request.form.get("UserIDList")      # “1,2,3,28,29,33”
    # print(UserTypeList)
    # print(UserIDList)

    # 分割成字符串列表
    UserType = UserTypeList.split(",")  # ['1', '2', '8', '5', '5', '5']
    UserID = UserIDList.split(",")      # ['1', '2', '3', '28', '29', '33']


    print(type(UserType))  # <class 'list'>
    print(type(UserID))    # <class 'list'>
    print(UserType)        # ['1', '2', '8', '5', '5', '5']
    print(UserID)          # ['1', '2', '3', '28', '29', '33']

    myUserTypeList = UserType
    myUserIDList = UserID
    print(type(myUserTypeList[0]))  # <class 'str'>
    print(type(myUserIDList[0]))    # <class 'str'>
    try:
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',  # 数据库用户名
            passwd='123456',  # 密码
            db='chatGPT',
            charset='utf8'
        )

        # 获取游标
        cursor = connect.cursor()

        # 遍历每一个 记录
        for k in range(0,len(myUserTypeList)):
            UT = eval(myUserTypeList[k])   # 转为 int   因为表结构中 UserType 为 int   取出第 k个用户的 UserType
            ID = eval(myUserIDList [k])    # 转为 int   因为表结构中 UserID 为 int     取出第 k个用户的 UserID
            # 构造更新 语句 SQL
            # 将  UserID={ID} 用户的 UserType 修改为  {UT}
            update_sql = f'UPDATE users SET UserType = {UT} Where  UserID={ID}'
            print(update_sql)

            # 执行批量更新
            cursor.execute(update_sql)

            # 提交更改并关闭连接
            connect.commit()


        return "成功更新"

    except Exception as e:
        print("Error:", str(e))
        # 发生错误时回滚事务
        connect.rollback()
        return "更新失败"
    finally:
        # 关闭游标和连接
        cursor.close()
        connect.close()

# 本代码DelUser()用于 批量删除注册用户
@app.route('/api/DelUser', methods=[ 'POST'])
def DelUser():
    print("================== @app.route('/api/EditUser', methods=[ 'POST']) ============================")
    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（用户名称（Phone)、密码（Password）

    # 读取微信小程序前端表单 （input）数据
    DelList = request.form.get("DelList")  #13685153598,13333333333,18051094982 整个是一个大的字符串
    # print(DelList)
    Phone = DelList.split(",")             # ['13685153598', '13333333333', '18051094982']
    # print(type(Phone))
    print(Phone)

    try:
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',  # 数据库用户名
            passwd='123456',  # 密码
            db='chatGPT',
            charset='utf8'
        )


        # 获取游标
        cursor = connect.cursor()


        # 确定要删除的 用户手机号
        condition = ""
        for k in range(0,len(Phone)):
            if k==0:                                                 #删除第一个人 ，不需要 用 ” or “
                condition = f" Phone ='{Phone[k]}' "
            else:
                condition = condition + f" or Phone ='{Phone[k]}'"   #删除后继的多个人 ，用 ” or “ 连接
        print(condition)

        # 构造删除用户记录的 SQL   先用 users2 测试 ，后面才用 users   users2为备份的注册用户数据表
        sql = 'DELETE  from users where ' + condition + " ;"

        print(sql)

        # 执行sql语句，筛选在拼接
        cursor.execute(sql)

        # 提交执行
        connect.commit()

        return "成功删除"

    except Exception as e:
        print("Error:", str(e))
        # 发生错误时回滚事务
        connect.rollback()
        return "删除失败"
    finally:
        # 关闭游标和连接
        cursor.close()
        connect.close()



# 随机产生 年龄（min_year,max_year ）之间的 出生年月，如（15岁 -60岁） ，返回日期型的：1970-10-13
def birth(min_year, max_year):
    # 假设出生日期范围为60年前到当前时间之间（60*365=21600） 到 15年前 （15*365 =5475）
    min_days = min_year * 365
    max_days = max_year * 365
    n = random.randint(min_days, max_days)
    # n天前日期
    birth = now - datetime.timedelta(days=n)
    return birth


# 模拟作息时间，随机产生 2020 年 到现在的一个聊天时间 ，返回日期时间型的：2021-10-07 10:54:25
def CreateChatTime():
    mynow = datetime.date.today()
    # 模拟不同年份的聊天斌率 ，体现 2023 年最高，方便以后 按照年份进行统计分析
    years = [2020, 2021, 2021, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2024, 2024]
    year = hour = random.choice(years)             # 只生成 myYear 如2020  到当年的聊天时间
    if year == now.year:
        month = random.randint(1, mynow.month)     # 如果是当年 ，只生成 当月之前的时间
    else:
        month = random.randint(1, 12)
    if year == mynow.year & month == mynow.month:  # 如果为当年当月，确保只生成前一天之前的时间
        day = random.randint(1, mynow.day - 1)     # 不生成当天的聊天记录，否则会要判断 时分秒，以免生成 还没有到达的时刻
    else:
        day = random.randint(1, 28)                # 暂时不考虑 闰年问题
    if day == 0:
        day = 1
    # 模拟作息时间，在 0,1,2,3,4,5,5,。。。22,22,22,23 点的聊天斌率比较低 ，可以对聊天此次 按照一天中的 时间进行统计分析
    hours = [0, 1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11,
             12, 12, 12, 12,13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17,
             17, 18, 18, 18, 18,19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 23]
    hour = random.choice(hours)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    date_time = datetime.datetime(year, month, day, hour, minute, second)
    return date_time



# 本代码生成聊天记录文件Dialo.xlsx
@app.route('/api/CreateDialo', methods=[ 'POST'])
def CreateDialo():

    #读取参数表（csb)

    ############################################
    # 连接数据库 csb表
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',  # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    # 检索用户
    # 先获取是否存在用户(手机号）数据
    sql = 'select * from csb '

    # 执行sql语句，筛选在拼接
    cursor.execute(sql)
    # cursor.execute(sql)
    # 获取所有返回结果
    res_csb = cursor.fetchall()  # 结果是列表套字典

    # 关闭数据库连接
    connect.close()
    print("=========== res_csb =============")
    print(res_csb)
    # 如果非空
    if res_csb:
        # 效验密码(索引0 获取真正的列表里面的字典)

        print(res_csb)
        print(len(res_csb))
        print(res_csb[0])
        print(type(res_csb[0]))


        MinY = res_csb[0][1]
        MaxY = res_csb[0][2]
        myBL=res_csb[0][3]
        ManN = res_csb[0][4]
        WenmenN = res_csb[0][5]
        ChatN = res_csb[0][6]
        print("==========  MinY MaxY  myBL  ManN WenmenN ChatN begin================ ")
        print(MinY)
        print(MaxY)
        print(myBL)
        print(ManN)
        print(WenmenN)
        print(ChatN)
        print("==========  MinY MaxY  myBL ManN WenmenN ChatN   end================ ")

    ###########################################



    # import datetime

    # 当前日期：年-月-日
    now = datetime.date.today()

    # python随机生成姓名
    # 姓氏列表
    surnames = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何',
                '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏',
                '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史',
                '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅',
                '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹','欧阳','上官','诸葛']
    # 男人名字列表
    Man_names = ['小', '明', '强', '亮', '敏', '洁', '晓', '新', '建', '国', '军', '峰', '涛', '雷', '刚', '磊', '亚', '梦', '龙', '中', '涛',
                 '桃', '民', '山', '凌', '阿', '天', '理', '宏', '高', '争', '正']

    # 女人名字列表
    Wen_names = ['小', '红', '丽', '美', '娜', '玲', '晓', '燕', '露', '芳', '艳', '静', '婷', '敏', '洁', '雅', '雪', '琳', '晓', '兰', '莉',
                 '梦', '英', '妹', '靓', '媚', '琳', '妞', '茜', '溪']
    # 男人姓名列表和女人姓名列表
    Man = []
    Wenmen = []

    # 男人女人 出生年月
    CSNY_Man = {}
    CSNY_Wenmen = {}

    # 男人女人 出生年份
    YEAR_Man = {}
    YEAR_Wenmen = {}

    # 男人女人 岁数（年龄）
    NL_Man = {}
    NL_Wenmen = {}

    # 随机生成70个男性姓名 =50+20  ManN WenmenN ChatN
    # for i in range(50):
    for i in range(ManN):
        Man_surname = random.choice(surnames)  # 随机选一个
        Man_name = ''.join(random.sample(Man_names, 2))  # 随机选两个用空字符串连接
        Man.append(Man_surname + Man_name)

    # 确保姓名也不是均匀分布
    Man1 = random.choice(Man)
    Man2 = random.choice(Man)
    Man3 = random.choice(Man)
    Man4 = random.choice(Man)
    Man5 = random.choice(Man)
    Man6 = random.choice(Man)

    # 随机重复20个男人姓名
    for k in range(1, 8):  #7
        Man.append(Man1)
    for k in range(1, 6):  #5
        Man.append(Man2)
    for k in range(1, 4):  #3
        Man.append(Man3)
    for k in range(1, 3):  #2
        Man.append(Man4)
    for k in range(1, 2):  #1
        Man.append(Man5)
    for k in range(1, 3):  #2
        Man.append(Man5)

    random.choice(Man)

    print(Man)  # 字符串连接

    # 随机生成70个女性姓名  50+20  ManN WenmenN ChatN
    # for i in range(50):
    for i in range(WenmenN):
        Wen_surname = random.choice(surnames)  # 随机选一个
        Wen_name = ''.join(random.sample(Wen_names, 2))  # 随机选两个用空字符串连接
        Wenmen.append(Wen_surname + Wen_name)

    print(Wenmen)  # 字符串连接

    Wenmen1 = random.choice(Wenmen)
    Wenmen2 = random.choice(Wenmen)
    Wenmen3 = random.choice(Wenmen)
    Wenmen4 = random.choice(Wenmen)
    Wenmen5 = random.choice(Wenmen)
    Wenmen6 = random.choice(Wenmen)

    # 随机重复20个女人姓名
    for k in range(1, 7):          #6
        Wenmen.append(Wenmen1)
    for k in range(1, 6):          #5
        Wenmen.append(Wenmen2)
    for k in range(1, 5):          #4
        Wenmen.append(Wenmen3)
    for k in range(1, 4):          #3
        Wenmen.append(Wenmen4)
    for k in range(1, 2):          #1
        Wenmen.append(Wenmen5)
    for k in range(1, 2):          #1
        Wenmen.append(Wenmen6)

    print(Wenmen)

    print('当前日期：', now)
    # 生成10个随机日期
    # min_year = 15  # 最小 15岁
    # max_year = 60  # 最大 60岁
    min_year = MinY  # 最小 15岁
    max_year = MaxY  # 最大 60岁

    # 给40名 男性 随机生成一个  出生年月和年龄（岁数） ManN WenmenN ChatN
    # for i in range(40):
    for i in range(ManN):
        d = birth(min_year, max_year)
        y = d.year
        nl = now.year - y
        print(d, y, nl)

        CSNY_Man[Man[i]] = d
        YEAR_Man[Man[i]] = y
        NL_Man[Man[i]] = nl

    # 给60名 女性 随机生成一个  出生年月、出生年份和年龄（岁数） ManN WenmenN ChatN
    # for i in range(60):
    for i in range(WenmenN):
        d = birth(min_year, max_year)
        y = d.year
        nl = now.year - y
        # print(d, y, nl)

        CSNY_Wenmen[Wenmen[i]] = d
        YEAR_Wenmen[Wenmen[i]] = y
        NL_Wenmen[Wenmen[i]] = nl

    print(CSNY_Man)
    print(YEAR_Man)
    print(NL_Man)

    print(CSNY_Wenmen)
    print(YEAR_Wenmen)
    print(NL_Wenmen)

    # 创建空白的DataFrame对象
    df = pd.DataFrame()

    # 打开原始电影对话台词 聊天记录 共 96785 行
    '''
    喂，吉姆，晚饭后去喝点啤酒怎么样？
    你知道这很诱人，但对我们的健康真的不好。
    什么意思?它会帮助我们放松。
    你真的这么认为吗？我没有。这只会让我们变胖，变傻。记得上次吗？
    我想你是对的。但是我们该怎么办呢？我不想坐在家里。
    我建议去健身房，在那里我们可以唱歌，还可以认识一些朋友。
    '''
    with open('./zhddline_lines.txt', 'r', encoding='utf-8') as file:
        # 一次全部读到 lines 列表中
        lines = file.readlines()

        #     # 遍历所以行，一次处理 2行 ，一行为 问题 ，一行为 聊天答案
        # for i in range(0, len(lines) - 1, 2):  # 正式转换所有行
        for i in range(0, ChatN, 2):                  #ChatN 为管理员设置的聊天记录数
        # for i in range(0,2000,2):                   # 测试用，仅仅处理前 1000行 记录，产生 500对聊天数据
            # 将奇数行 和 偶数行去除 \n ，添加到DataFrame中的 'Question' 、 'Answer'，其它为  空白的字段，如 用户名 、性别、出生日期 、出生年份、岁数（年龄）、聊天时间
            df = df.append(
                {'Question': lines[i].strip('\n'), 'Answer': lines[i + 1].strip('\n'), 'UserName': '', 'Gender': '',
                 'Birthday': now, 'Year': now.year, 'NL': 0, 'ChatTime': now}, ignore_index=True)

    file.close()
    print("=========================================================")
    print("df.shape[0]:")
    print(df.shape[0])
    print("=========================================================")

    # 对所有记录，添加 用户名 、性别、出生日期 、出生年份、岁数（年龄）
    for i in range(df.shape[0]):
        n = df.index
        k = random.randint(1, 101)  # 产生 1、2、3、4、5.。。100   其中myBL/100 为女性
        if k <= myBL:  # 1、2、3、4、5 、myBL   myBL/100为 女性
            name = random.choice(Wenmen)  # 随机选择一个女人
            df.loc[i, 'UserName'] = name  # 姓名  为聊天的用户名
            df.loc[i, 'Gender'] = '女'  # 性别      该女人对应的 性别
            df.loc[i, 'Birthday'] = CSNY_Wenmen[name]  # 出生年月   该女人对应的 出生年月
            df.loc[i, 'Year'] = YEAR_Wenmen[name]  # 出生年份   该女人对应的 出生年份
            df.loc[i, 'NL'] = NL_Wenmen[name]  # 年龄      该女人对应的 年龄
        else:
            # 1-myBL/100 为 男性
            name = random.choice(Man)  # 随机选择一个男人
            df.loc[i, 'UserName'] = name  # 聊天童虎名
            df.loc[i, 'Gender'] = '男'  # 聊天者 性别
            df.loc[i, 'Birthday'] = CSNY_Man[name]  # 聊天者出生年月
            df.loc[i, 'Year'] = YEAR_Man[name]  # 聊天者出生年份
            df.loc[i, 'NL'] = NL_Man[name]  # 聊天者岁数

        df.loc[i, 'ChatTime'] = CreateChatTime()  # 随机生成聊天时间为 2020年到现在的某一个时间

    # 保存到excel 中
    df.to_excel('./Dialo.xlsx', index=False)
    print("Dialo.xlsx 已经生成！")

    listData = []

    # 测试结果
    for i in range(0, 20):
        # print(df.loc[i, 'Question'])
        # print(df.loc[i, 'Answer'])
        # print(df.loc[i, 'UserName'])
        # print(df.loc[i, 'Gender'])
        # print(df.loc[i, 'Birthday'])
        # print(df.loc[i, 'Year'])
        # print(df.loc[i, 'NL'])
        # print(df.loc[i, 'ChatTime'])
        Q1 =df.loc[i, 'Question'][:10]  #只截取前面10个汉字
        A1 = df.loc[i, 'Answer'][:10]   #只截取前面10个汉字
        # print("========= 聊天问题与答案摘要 =======")
        # print(Q1)
        # print(A1)
        d1 = df.loc[i, 'Birthday']
        date_str = d1.strftime("%Y-%m-%d")               #将日期格式转换为 字符串
        t1 = df.loc[i, 'ChatTime']
        datetime_str = t1.strftime("%Y-%m-%d %H:%M:%S")  #将日期时间格式转换为 字符串
        # print(datetime_str)
        n1 =df.loc[i, 'NL']
        n2 = int(n1)                                     #将int64 转换为 int
        # 将数据构造成 字典
        dict1 ={'Question':Q1,'Answer':A1,'UserName':df.loc[i, 'UserName'], 'Gender':df.loc[i, 'Gender'], 'Birthday':date_str ,'NL':n2 ,'ChatTime':datetime_str}
        # print(dict1)
        # 将一条聊天记录 添加到 列表listData中
        listData.append(dict1)

    # 观察 列表数据
    print(listData)
    # # 保存到excel 中
    # df.to_excel('./Dialo.xlsx', index=False)
    # print("Dialo.xlsx 已经生成！")

    # 转为json  注意：转换之前，一定要将其中的数据 规范化 ，如 日期等 转为 字符串 ，int64 转换 int
    res_json = json.dumps(listData)

    # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
    # 数据在前端用 res.data......提取   listData:res.data ,其中res.data 就是 转为 json格式的listData
    return res_json, 200, {"Content-Type": "application/json"}


# 本代码浏览 注册用户表
@app.route('/api/EditUser', methods=[ 'POST'])
def EditUser():
    #连接数据库 users表
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',  # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    # 检索用户
    # 先获取是否存在用户(手机号）数据
    sql = 'select * from users '

    # 执行sql语句，筛选在拼接
    cursor.execute(sql)
    # cursor.execute(sql)
    # 获取所有返回结果
    res = cursor.fetchall()  # 结果是列表套字典

    # 关闭数据库连接
    connect.close()

    listData = []
    # 如果非空
    if res:
        # 效验密码(索引0 获取真正的列表里面的字典)
        print("=========== 注册用户信息 res  len(res)  len(res[0])  type(real_dict) real_dict =============")
        print(res)
        print(len(res))
        real_dict = res[0]
        print(len(real_dict))
        print(type(real_dict))  # 'tuple'  原组类型
        print(real_dict)

        # res 的结构如下
        '''
        ((1, '13685153598', 'SM', '123456', datetime.datetime(2024, 2, 22, 18, 48, 39), '男', datetime.date(1964, 9, 4),
          '/static/image/header.png'),
         (2, '13333333333', 'Lisi', '123456', datetime.datetime(2024, 2, 22, 19, 12, 36), '女', datetime.date(1999, 9, 9),
         '/static/image/ala.png'), 
         ......
        )
        '''

        for k in range(0,len(res)):
            real_dict = res[k]
            print(f"第 { k } 个注册用户信息：")
            print(real_dict)
            myid = real_dict[0]
            myPhone = real_dict[1]
            myUserName = real_dict[2]
            myPassword = real_dict[3]
            myRegisterTime = str(real_dict[4])   #转换为字符串
            myGender = real_dict[5]
            myBirthday = str(real_dict[6])       #转换为字符串
            myFaceImg = real_dict[7]
            myUserType = real_dict[8]

            # d1 = myBirthday
            # date_str = d1.strftime("%Y-%m-%d")  # 将日期格式转换为 字符串
            # t1 = myRegisterTime
            # datetime_str = t1.strftime("%Y-%m-%d %H:%M:%S")  # 将日期时间格式转换为 字符串
            # print(datetime_str)

            # 将数据构造成 字典
            dict1 = {'Phone': myPhone,  'UserName': myUserName, 'Password':myPassword, 'Gender': myGender,
                     'Birthday': myBirthday,  'RegisterTime': myRegisterTime,'FaceImg': myFaceImg,'UserType':myUserType}
            # print(dict1)
            # 将一条聊天记录 添加到 列表listData中
            listData.append(dict1)

        print("所有用户信息：")
        print(listData)
        # 转为json
        res_json = json.dumps(listData)

        # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
        # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
        return res_json, 200, {"Content-Type": "application/json"}


    else:
        print('注册表为空')
        return '0'


# 本代码根据 聊天记录文件Dialo.xlsx 进行可视化分析
@app.route('/api/DtVisual', methods=[ 'POST'])
def DtVisual():

    print("================== @app.route('/api/DtVisual', methods=[ 'POST']) ============================")

    # Question , Answer, UserID, UserName, ChatTime, Gender, Birthday ,NL   Year
    comments = pd.read_excel(r'./Dialo.xlsx')

    # (1) 聊天数量按照日期分布情况（line)
    #######################################################
    num = comments['ChatTime'].dt.date.value_counts().sort_index()
    print(" ============== 1  聊天数量按照日期分布情况（line1)  ")
    X1 = num.index[::30]    #每隔30天 取一个日期数据
    Y1 = []
    for k in range(len(X1)):
        Y1.append(num[X1[k]])
    X1 = list(X1)
    formatted_dates = [date.strftime("%Y-%m-%d") for date in X1]   #将日期型转换为 字符串型
    X1 = formatted_dates


    # (2)聊天数量按照周次分布情况 （line)
    num = comments['ChatTime'].dt.dayofweek.map(
        {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}).value_counts()
    print(" ============== 2  聊天数量按照周次分布情况 （Pie)  ")
    X2 = num.index
    Y2 = []
    for k in range(len(X2)):
        Y2.append(num[X2[k]])
    X2 = list(X2)
    print(X2)
    print(Y2)

    # (3)聊天数量按照 一天里的时间点分布情况  （line)
    num = comments['ChatTime'].dt.hour.value_counts().sort_index()
    print(" ============== 3  聊天数量按照 一天里的时间点分布情况  （line3) ")

    X3 = num.index
    Y3 = []
    for k in range(len(X3)):
        Y3.append(num[X3[k]])
    X3 = list(X3)
    print(X3)
    print(Y3)

    # (4)聊天数量按照性别点分布情况 (bar1)
    num = comments['Gender'].value_counts().sort_index()
    print(" ============== 4  聊天数量按照性别点分布情况 (bar1) ")
    X4 = num.index
    Y4 = []
    for k in range(len(X4)):
        Y4.append(num[X4[k]])
    X4 = list(X4)
    print(X4)
    print(Y4)
    # X4 =['女', '男']
    # Y4 =[32232, 16160]

    # (5) 聊天数量按照年龄分布情况  (bar2)
    num = comments['NL'].value_counts().sort_index()
    print(" ============== 5  聊天数量按照年龄分布情况  (bar2) ")
    X5 = num.index
    Y5 = []
    for k in range(len(X5)):
        Y5.append(num[X5[k]])
    X5 = list(X5)
    print(X5)
    print(Y5)


    # 聊天情感分析
    line = open("zhddline_1000.txt", "r", encoding='utf8').readlines()
    sentimentslist = []
    for i in line:
        s = SnowNLP(i)
        # print(s.sentiments)
        sentimentslist.append(s.sentiments)

    # 区间转换为[-0.5, 0.5]
    result = []
    i = 0
    while i < len(sentimentslist):
        result.append(sentimentslist[i] - 0.5)
        i = i + 1

    # print("====== sentimentslist  result ======")
    # print(len(sentimentslist))
    # print(len(result))
    X6 = np.arange(0, len(result), 1)
    Y6 = result

    print(X6[:30])
    print(Y6[:30])
    x61 = list(map(int, X6))
    y62 = Y6
    # 可视化画图
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号“-”显示异常
    #
    # plt.plot(np.arange(0, len(result), 1), result, 'r-')
    # plt.xlabel('聊天序号（The Number of Wechat)')
    # plt.ylabel('情感（Sentiments）')
    # plt.title('基于chatGPT聊天情感分析（Sentiments of chatGPT）')
    # plt.show()

    # x11 = [1,3,5,7,9,11,13,15,17,19,21]
    # y12=[9, 9, 5, 10, 6, 10, 9, 13, 4, 5, 7]


    x11 = X1
    y12 = list(map(int, Y1))



    # x21 =['周六', '周一', '周五', '周三', '周日', '周四', '周二']
    # y22 = [7036, 7009, 6939, 6923, 6853, 6839, 6793]
    x21 = X2
    y22 = list(map(int, Y2))   #  列表中 'numpy.int64' 类型的元素，转换为 int 类型


    # y32 = [533, 501, 531, 538, 543, 1011, 1620, 1566, 2022, 2655, 2607, 2694, 2066, 2697, 3205, 3233, 3119, 2627, 2023, 3213, 3661, 3680, 1553, 494]
    # x31 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    x31 = X3
    y32 =  list(map(int, Y3))



    # x41 = ['女', '男']
    # y42 = [32232, 16160]
    x41 = X4
    y42 = list(map(int, Y4))


    # x51 = [17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59]
    # y52 = [826, 486, 3524, 1161, 1324, 4172, 463, 1346, 3913, 493, 1459, 489, 1358, 495, 5530, 2582, 320, 1004, 313, 484, 1343, 341, 2543, 1020, 2581, 333, 472, 1059, 328, 1311, 1343, 311, 692, 988, 482, 667, 836]
    x51 =X5
    y52 =list(map(int, Y5))

    # 动态生成 饼图所需要的数据 myPie
    # x21 =['周六', '周一', '周五', '周三', '周日', '周四', '周二']
    # y22 = [7036, 7009, 6939, 6923, 6853, 6839, 6793]
    myPie=[]
    for k in range(len(x21)):
        dict1 ={'name':x21[k] ,'value':y22[k]}
        myPie.append(dict1)
    print(myPie)
    '''
    [{'name': '周六', 'value': 7036}, {'name': '周一', 'value': 7009}, {'name': '周五', 'value': 6939},
     {'name': '周三', 'value': 6923}, {'name': '周日', 'value': 6853}, {'name': '周四', 'value': 6839},
     {'name': '周二', 'value': 6793}]
    '''


    # 直接用常量定义的 myPie
    # myPie = [
    #     {'value': 7036, 'name': '周六'},
    #     {'value': 7009, 'name': '周一'},
    #     {'value': 6939, 'name': '周五'},
    #     {'value': 6923, 'name': '周三'},
    #     {'value': 6853, 'name': '周日'},
    #     {'value': 6839, 'name': '周四'},
    #     {'value': 6793, 'name': '周二'}
    # ]

    print('================================ 测试 WordClod =====================================')

    # 下面的代码，对聊天问题进行分词切割，然后转换为 字典的形式，返回 小程序前端 WC1：  {'想': 85, '喜欢': 78, '真的': 47, '谢谢': 39, '工作': 39, 。。。}
    ########################################################  2024-12-8 begin
    # jieba.load_userdict(dict_path)                 # dict_path为文件类对象或自定义词典的路径
    jieba.load_userdict('./WCDict.txt')  # 加载自定义词典

    # 对聊天问题进行分词切割
    comment_cut = comments['Question'].apply(jieba.lcut)  # 每一个弹幕评论都使用分词函数 lcut
    print("\n===================================  9  comment_cut  ===================\n")
    print(comment_cut)
    '''
    0                 [喂, ，, 吉姆, ，, 晚饭, 后, 去, 喝点, 啤酒, 怎么样, ？]
    1                 [什么, 意思, ?, 它会, 帮助, 我们, 放松, 。]
    '''

    # 加载停用词表
    with open('./stoplist.txt', encoding='utf-8') as f:
        stop_words = f.read()

    stop_words += '\n'

    # 去除停用词
    comment_after = comment_cut.apply(lambda x: [i for i in x if i not in stop_words])  # 去除停用词

    print(comment_after)

    '''
    list：将comment_after 转换为 多维列表
    _flatten 函数 将 多维列表 拍偏为 一维 
    pd.Series： 将一维列表转换为 Series （一维的数据表）
    value_counts： Series 表在的元素 进行 计数统计
    '''
    word_fre = pd.Series(_flatten(list(comment_after))).value_counts()
    print("\n 10 ===================================  word_fre  ===================\n")
    print(word_fre)
    '''
    想     85
    喜欢    78
    真的    47
    谢谢    39
    工作    39
      ..
    '''

    print("\n 11 ===================================  word_fre.index  ===================\n")
    print(word_fre.index)

    # 聊天问题“词” 如下
    '''
    ndex(['想', '喜欢', '真的', '谢谢', '工作', '我会', '这是', '听', '时间', '太',
       ...
       '声音', '疼痛', '停不下来', '每周', '舞曲', '明快', '玛吉', '解雇', '湿滑', '退掉'],
      dtype='object', length=2494)
    '''



    '''
   {'想': 85, '喜欢': 78, '真的': 47, '谢谢': 39, '工作': 39, '我会': 34, '这是': 32, '听': 32, '时间': 26, '太': 25, ...}
    '''

    print("\n 12 ===================================  WC1  ===================\n")

    WC1 = word_fre.to_dict()

    print(WC1)

    ############################## 2024-12-08  end

    # 构造一个字典 Dict 型数据
    data = {
        "user_Data11": x11,
        "user_Data12": y12,
        "user_Data21": x21,
        "user_Data22": y22,
        "user_Data31": x31,
        "user_Data32": y32,
        "user_Data41": x41,
        "user_Data42": y42,
        "user_Data51": x51,
        "user_Data52": y52,
        "user_Data53": myPie,
        "user_Data61": x61,
        "user_Data62": y62,
        "user_WC1": WC1,
    }
    #######################################################################3### 2024-12-08  end
    print("\n 13 ===================================  data  ===================\n")
    print(data)
    # 转为json
    res_json = json.dumps(data)
    print("\n 14 ===================================  res_json  ===================\n")
    print(res_json)
    # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
    # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
    return res_json, 200, {"Content-Type": "application/json"}





# 本代码Login用于登录检查
@app.route('/api/Login', methods=[ 'POST'])
def Login():

    print("================== @app.route('/api/Login', methods=[ 'POST']) ============================")
    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（用户名称（Phone)、密码（Password）

    # 读取微信小程序前端表单 （input）数据
    Phone = request.form.get("Phone")
    Password = request.form.get("Password")

    print(Phone,Password)
    # 路径数据库进行验证

    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',  # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    # 检索用户
    # 先获取是否存在用户(手机号）数据
    sql = 'select * from users where Phone=%s'

    # 执行sql语句，筛选在拼接
    cursor.execute(sql, (Phone,))
    # cursor.execute(sql)
    # 获取所有返回结果
    res = cursor.fetchall()  # 结果是列表套字典

    # 关闭数据库连接
    connect.close()

    # 如果存在该用户，再判断密码是否存在
    if res:
        # 效验密码(索引0 获取真正的列表里面的字典)
        real_dict = res[0]
        print(type(real_dict))
        print(real_dict)

        # 校验密码 元组中 第3个 元素   ‘123456’ 为 密码
        #(1, '13685153598', 'SM', '123456', datetime.datetime(2024, 2, 22, 18, 48, 39), '男', datetime.date(1964, 9, 4), '/static/image/header.png')

        # 如果密码也正确，为合法用户，需要保存该用户对应的所有信息
        if Password == real_dict[3]:
            myid = real_dict[0]
            myPhone = real_dict[1]
            myUserName = real_dict[2]
            myPassword = real_dict[3]
            myRegisterTime = str(real_dict[4])
            myGender = real_dict[5]
            myBirthday =str( real_dict[6])
            myFaceImg =real_dict[7]
            myUserType = int(real_dict[8])  #转为 int

            print('登录成功')

            #构造一个字典 Dict 型数据
            data = {
                "user_id":myid,
                "user_Phone": myPhone,
                "user_name": myUserName,
                "user_Password": myPassword,
                "user_Gender": myGender,
                "user_RegisterTime": myRegisterTime,
                "user_Birthday": myBirthday,
                "user_FaceImg": myFaceImg,
                "user_UserType": myUserType,
            }
            print(data)
            # 转为json
            res_json = json.dumps(data)

            # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
            # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
            return res_json, 200, {"Content-Type": "application/json"}

            # return '1'
        else:
            print('密码错误')
            return '0'
    else:
        print('用户名不存在 ')
        return '0'




# 本代码Register 用注册
@app.route('/api/Register', methods=['POST'])
def Register():
    global FaceImg
    print("================== @app.route('/api/Register', methods=[ 'POST']) ============================")
    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（用户名称（Username)、密码（Password）
    Phone = request.form.get("Phone")
    UserName = request.form.get("UserName")
    Password = request.form.get("Password")
    # UserID = request.form.get("UserID")
    Birthday = request.form.get("Birthday")
    Gender = request.form.get("Gender")
    # Email = request.form.get("Email")
    RegisterTime = str(datetime.datetime.now())
    UserType = int(3)
    # FaceImg = request.form.get("FaceImg")
    print("FaceImg:")
    print(FaceImg)

    print(Phone,UserName,Gender,Birthday,RegisterTime,Password ,FaceImg,UserType)
    try:
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',  # 数据库用户名
            passwd='123456',  # 密码
            db='chatGPT',
            charset='utf8'
        )

        # 获取游标
        cursor = connect.cursor()

        ##########################################
        # 检测原账号是否已经存在（手机号）
        sql = 'select * from users where Phone=%s'

        # 执行sql语句，筛选在拼接
        cursor.execute(sql, (Phone,))
        # cursor.execute(sql)
        # 获取所有返回结果
        res = cursor.fetchall()  # 结果是列表套字典

        # # 关闭数据库连接
        # connect.close()

        # 如果存在该用户，再判断密码是否存在
        if res:
            print('该手机号已经注册过！ ')
            # 关闭数据库连接
            connect.close()
            data ={'user_answer': '1'}
            res_json = json.dumps(data)
            return  res_json

        #################################################
        sql = "INSERT INTO users(Phone , UserName, Gender,  Birthday,RegisterTime,Password,FaceImg,UserType) VALUES ('%s', '%s','%s',  '%s', '%s','%s','%s',%d  )"
        # print(f" 3 {sql}")
        data = (Phone , UserName, Gender,  Birthday,RegisterTime,Password,FaceImg,UserType)
        cursor.execute(sql % data)
        # print(" 3===========================")
        connect.commit()
        print('成功保存注册账号信息')

        # 关闭数据库连接
        connect.close()
        data = {'user_answer': '0'}
        res_json = json.dumps(data)
        return res_json
        # return "0"
    except:
        print(" 注册失败  ERR ")
        data = {'user_answer': '2'}
        res_json = json.dumps(data)
        return res_json
        # return "2"


# 本代码，用python 利用 ctypes 的cdll   调用“libpycall.so" 动态链接库中的函数 add
@app.route('/api/CreateJar', methods=[ 'POST'])
def CreateJar():

    print("================== @app.route('/api/CreateJar', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（函数名称、参数1、参数2、参数3）


    Myclass_path = request.form.get("Myclass_path")
    FileName_txt = request.form.get("FileName_txt")
    FileName_jar = request.form.get("FileName_jar")
    FileName_java1 = request.form.get("FileName_java")
    print(FileName_java1)
    FileName_java = "D:/WxMinPro/java/" + FileName_java1
    if os.path.exists(FileName_java):
        os.remove(FileName_java)


    # FileName_java = "D:/WxMinPro/java/" + "JpypeDemo.java"
    if os.path.exists("D:/WxMinPro/java/Test.java"):
        os.renames("D:/WxMinPro/java/Test.java",FileName_java)
    else:
        msg = f'Test.java不存在， 请选择要打包的 java文件！'
        print(msg)
        msg = "ERR"
        return msg

    print(Myclass_path,FileName_txt,FileName_jar,FileName_java)

    bj = 0
    if  not os.path.exists(FileName_java):
        print(f"要打包的[{FileName_java}]不存在！")
        bj = 2
        sum ="ERR"
        return sum

    try:
        import subprocess
        # import os

        # （1）下面为 键盘输入 打的包完整的主类名称，如：com.example.JpypeDemo
        text0 = "Main-Class: com.example.JpypeDemo"
        # text1 = input('请输入要打的jar包的完整的主类名称（如：com.example.JpypeDemo）：')
        text1 = "com.example.JpypeDemo"
        text2 = "Main-Class: " + text1
        print("你要打成jar包的完整的主类名称为：" + text2)

        # （2）设置myclass所在路径
        # Myclass_path = "C:/soft/myspark/PyCallJava/out/myclass"
        # FileName_txt = Myclass_path + r"/Main-Class.txt"
        # FileName_jar = r'D:/WxMinPro/PyCallJava.jar'
        # FileName_java = r'C:/soft/myspark/PyCallJava/src/com/example/JpypeDemo.java'

        # （3）将打包主类配置文件写入 FileName指定是文件中
        file = open(FileName_txt, 'w')
        file.write(text2)
        file.close()

        # print("=========== 1===============")
        # （4）将java文件 编译为 class字节文件
        # 本代码，用python 利用 javac.exe   将“。java" 源码程序，编译成 JpypeDemo.class 字节码 并且写在myclass文件夹中
        # subprocess.call(['javac.exe', '-encoding', 'UTF-8', '-d',  r'C:/soft/myspark/PyCallJava/out/myclass', r'C:/soft/myspark/PyCallJava/src/com/example/JpypeDemo.java']) #ok
        subprocess.call(['javac.exe', '-encoding', 'UTF-8', '-d', Myclass_path, FileName_java])
        # print("=========== 2===============")
        # javac -encoding UTF-8 -d C:\soft\myspark\PyCallJava\out\myclass JpypeDemo.java

        # 切换到 myclass  必须要切换到生成的 class类中去运行（除非把 class字节文件copy到当前目录中）
        print(Myclass_path)
        os.chdir(Myclass_path)

        # （5）将当前的 myclass_path 下 com 根类下的 class文件 打为 jar包文件
        # 基本格式
        # jar -cvfm  PyCallJava.jar  Main-Class.txt  com

        # 将 myclass  下主类 ”COM"下面的 class 字节码 打包到 当前目录中（myclass）中，命名为PyCallJava.jar 也可以打包到指定目录中
        subprocess.call(['jar.exe', '-cvfm', FileName_jar, FileName_txt, 'com'])
        msg = "打包成功！"
        # print("=========== 3===============")
        return msg
    except:
        print("打包出错！")
        # 卸载so动态库，否则一直占用，不能运行新的库
        msg = "ERR"
        return msg


def UploadFile(LocalFilePath ,ServerFilePath,hostname='10.30.1.110', username='root', password='Cstorfs_123'):
    import paramiko
    # hostname = '10.30.1.110'
    # username = 'root'
    # password = 'Cstorfs_123'
    # （3）  把本地的 py文件（LocalFilePath) 上传到 10.30.1.110 的 ServerFilePath /home/tyx
    # print("\n=============================================================\n")
    Local_Python_File = LocalFilePath # 要上传到服务器上运行的本地文件
    Server_Python_File =ServerFilePath  # 上传到服务器上要运行的文件
    # Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    # Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径
    try:
        print(f"3-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台 的 {Server_Python_File} ")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()

        # 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
        # sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test.py')
        sftp.put(Local_Python_File, Server_Python_File)
        sftp.close()
        print("上传成功！")
        return 1
    except:
        print("上传失败！Error！")
        return 0



# 在远程服务器上运行 script
def execute_remote_script(hostname, username, password, script):
    import paramiko
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(script)
    output = stdout.read().decode()
    error = stderr.read().decode()

    client.close()

    if output:
        print("Output:\n", output)
    if error:
        print("Error:\n", error)


# 删除库文件
@app.route('/api/DelFile', methods=['GET'])
def  DelFil():
    # import os
    File_so = 'D:/WxMinPro/static/receive/c/libpycall.so'
    File_c = 'D:/WxMinPro/static/receive/c/Test.c'
    try:
        if  os.path.exists(File_so):
            os.remove(File_so)
        if  os.path.exists(File_c):
            os.remove(File_c)
        return '0'
    except:
        return '1`'


# 删除库文件
@app.route('/api/DelFilePy', methods=['GET'])
def  DelFilPy():
    # import os
    File_out = 'D:/WxMinPro/static/receive/Py/Test.Out'
    File_Py = 'D:/WxMinPro/static/receive/c/Test.Py'
    try:
        if  os.path.exists(File_out):
            os.remove(File_out)
        if  os.path.exists(File_Py):
            os.remove(File_Py)
        return '0'
    except:
        return '1`'


# 将前端指定的文件保存到指定的地方
@app.route('/api/ReceiveFaceImg', methods=['GET', 'POST'])
def ReceiveFaceImg():
    global FaceImg
    print("==============  ReceiveFaceImg()  ==========================")
    if request.method == "POST":
        myFile = request.files['file']
        print(myFile)
        # 获取上传文件的名称
        Filename = myFile.filename
        print(Filename)
        NewFilename ='D:/WxMinPro/static/icon/FaceImg/'+Filename
        # 上传后新的头像唯一文件名
        print(NewFilename)
        # 头像网络路径 注意和 NewFilename是不一样的
        FaceImg = '/static/icon/FaceImg/'+Filename
        # myFile.save('D:/WxMinPro/static/icon/FaceImg/Test.png')
        myFile.save(NewFilename)

        # 构造一个字典 Dict 型数据
        data = {
            "user_FaceImg":FaceImg,
        }
        print(data)
        # 转为json
        res_json = json.dumps(data)

        # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
        # 数据在前端用 res.data.user_FaceImg 提取
        return res_json, 200, {"Content-Type": "application/json"}

        # return '1'


# 将前端用麦克风录制的语音文件保存到指定的地方：D:/WxMinPro/static/SoundRecordFile/SoundRecordFile.MP3
@app.route('/api/SoundRecordFile', methods=['GET', 'POST'])
def SoundRecordFile():
    if request.method == "POST":
        myFile = request.files['file']
        myFile.save('D:/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3')
        return '1'



# 将前端指定的文件保存到指定的地方
@app.route('/api/Receive', methods=['GET', 'POST'])
def receive():
    if request.method == "POST":
        myFile = request.files['file']
        myFile.save('D:/WxMinPro/static/receive/c/Test.c')
        return '1'

# 将前端指定的文件保存到指定的地方
@app.route('/api/ReceivePy', methods=['GET', 'POST'])
def receivePy():
    if request.method == "POST":
        myFile = request.files['file']
        myFile.save('D:/WxMinPro/static/receive/Py/Test.Py')
        # 再上传到远程人工智能服务器上
        LocalFilePath = 'D:/WxMinPro/static/receive/Py/Test.Py'
        ServerFilePath = '/home/tyx/Test.py'
        try:
            rs=UploadFile(LocalFilePath ,ServerFilePath )
            if rs ==1:
                print("上传成功！")
                return '1'
            else:
                print("上传失败！")
                return '0'
        except:
            print("上传失败！")
            return '0'

# 将前端指定的文件保存到指定的地方
@app.route('/api/ReceiveJava', methods=['GET', 'POST'])
def receiveJava():
    if request.method == "POST":
        myFile = request.files['file']
        print(myFile)
        myFile.save('D:/WxMinPro/java/Test.java')
        return '1'



@app.route('/api/CompileFile', methods=['GET', 'POST'])
def CompileFile():
    Fpath = request.args.get("file")
    print( Fpath)
    try:
        # import subprocess
        File_gcc = r'C:/soft/Dev-Cpp-5.15/TDM-GCC-64/bin/gcc.exe'
        File_so = 'D:/WxMinPro/static/receive/c/libpycall.so'
        File_c = 'D:/WxMinPro/static/receive/c/Test.c'
        if not os.path.exists(File_gcc):
            print(f"编译器[{File_gcc}]不存在！")
            return '1'
        if os.path.exists(File_c):
            subprocess.call([File_gcc, '-o', File_so, '-shared', '-fPIC', File_c])
            print("编译成功！")
            return '0'
        else:
            print(f"原文件[{File_c}]不存在！")
            return '3'
    except:
        print("编译失败！")
        return '3'



# 本代码，用python 利用 ctypes 的cdll   调用“libpycall.so" 动态链接库中的函数 add
@app.route('/api/RunFile', methods=[ 'POST'])
def RunFile():
    print("================== @app.route('/api/RunFile', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（函数名称、参数1、参数2、参数3）
    FunctionName = request.form.get("FunctionName")
    Data1 = request.form.get("Data1")
    Data2 = request.form.get("Data2")
    Data3 = request.form.get("Data3")
    print(FunctionName,Data1,Data2,Data3)
    # Phone = json.loads(Phone)
    # Code = json.loads(Code)
    # print(Fpath)
    bj = 0
    File_so = 'D:/WxMinPro/static/receive/c/libpycall.so'
    if not os.path.exists(File_so):
        print(f"编译器[{File_so}]不存在！")
        bj = 2
        sum =f"[{File_so}]库文件不存在！"
        return sum

    try:
        from ctypes import cdll
        import ctypes
        # 加载动态库（。so)
        lib = "D:/WxMinPro/static/receive/c/libpycall.so"
        libpycall = cdll.LoadLibrary(lib)
        # print("=======================  libpycall ================\n")
        # 调用动态库中的函数
        # 加法
        if FunctionName=='Add':
            # sum = libpycall.add(90, 30)
            sum = libpycall.Add(int(Data1), int(Data2))
            print("Add:",sum)
            bj=0
        # 减法
        if FunctionName == 'Sub':
            sum = libpycall.Sub(int(Data1), int(Data2))
            print("Sub:",sum)
            bj=0

        # 乘法
        if FunctionName == 'Mul':
            sum = libpycall.Mul(int(Data1), int(Data2))
            print("Mul:",sum)
            bj=0

        # 除法
        if FunctionName == 'Div':
            sum = libpycall.Div(int(Data1), int(Data2))
            if (sum == -9999):
                sum="分母不能为 0 "
                bj = 1
            else:
                bj = 0
            print("Div:",sum)

        # 求余
        if FunctionName == 'Rem':
            sum = libpycall.Rem(int(Data1), int(Data2))
            if (sum == -9999):
                bj = 1
                sum="分母不能为 0 "
            else:
                bj = 0
            print("Rem:",sum)

        # 阶乘 n!
        if FunctionName == 'Fac':
            sum = libpycall.Fac(int(Data1))
            print("=========================================================")
            print(type(sum))
            print(sum)
            if (sum == -9999):
                bj = 1
                sum="只能计算(0-10）以内的阶乘"
            else:
                bj = 0
            print("Fac:",sum)

        # 判别素数
        if FunctionName == 'isPrime':
            sum = libpycall.isPrime(int(Data1))
            if (sum ):
                bj = 1
                sum =Data1 +  "是素数！"
            else:
                bj = 0
                sum = Data1 + "不是素数！"
            print("isPrime:", sum)

        print("运行结果 sum=", sum)


        # 卸载so动态库，否则一直占用，不能运行新的库
        handle = libpycall._handle
        del libpycall
        ctypes.windll.kernel32.FreeLibrary(handle)


        # 回调函数需要返回一个字符串类型，故如果 sum 是 int 数值类型的需要转换为字符串
        if  isinstance(sum,int):
            sum = str(sum)
        # 返回运行结果
        return sum
    except:
        print("运行出错！")
        # 卸载so动态库，否则一直占用，不能运行新的库
        handle = libpycall._handle
        del libpycall
        ctypes.windll.kernel32.FreeLibrary(handle)
        return "ERR"


import jpype as jp
from jpype import *

# 本代码，用python 利用 jpype 编译连接 java
@app.route('/api/RunFileJava', methods=[ 'POST'])
def RunFileJava():
    global JVM_BJ
    print("================== @app.route('/api/RunFileJava', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（函数名称、参数1、参数2、参数3）
    FunctionName = request.form.get("FunctionName")
    Data1 = request.form.get("Data1")
    Data2 = request.form.get("Data2")
    Data3 = request.form.get("Data3")
    FileName_jar = request.form.get("FileName_jar")
    print(FunctionName,Data1,Data2,Data3,FileName_jar)

    # python 利用jpype 类库 调用jar包中的java类

    # import os

    # 1.加载jar包 (事先把java 打成jar包）
    jarpath = "./PyCallJava.jar"  # jar包所在位置 （可以打包后copy到 。py所在目录下）

     # 判断 jar文件 是否存在
    if not os.path.exists(FileName_jar):
        print(f"[{FileName_jar}]不存在！")
        bj = 2
        sum = f"[{FileName_jar}]文件不存在！"
        return sum
    try:
        # 2.获取jvm.dll 的文件路径
        jvmPath = jp.getDefaultJVMPath()

        # 防止JVM重复启动报错 ，因为Flask后端无法关闭 JVM ，即执行jp.shutdownJVM() 会报错
        # 只有第1次运行，才能启动  jp.startJVM(）
        if JVM_BJ==0:
            # 3.开启jvm
            jp.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jarpath))
            JVM_BJ =1

        # # 4.加载java类（参数是java的长类名）
        JDClass = jp.JClass("com.example.JpypeDemo")
        # 注意：com.example为  java中  package com.example;
        # JpypeDemo 中 java 中的主类

        # # 5.实例化java对象
        jd = JDClass()

        # 6.调用java方法，由于是静态方法，直接使用类名就可以调用方法

        # 加法
        if FunctionName == 'Add':
            sum = jd.Add(int(Data1), int(Data2))
            print("Add:", sum)
            bj = 0

       # 减法
        if FunctionName == 'Sub':
            sum = jd.Sub(int(Data1), int(Data2))
            print("Sub:", sum)
            bj = 0

        # 乘法
        if FunctionName == 'Mul':
            sum = jd.Mul(int(Data1), int(Data2))
            print("Mul:", sum)
            bj = 0

        # 除法
        if FunctionName == 'Div':
            sum = jd.Div(int(Data1), int(Data2))
            if (sum == -999):
                sum = "分母不能为 0 "
                bj = 1
            else:
                bj = 0
            print("Div:", sum)

        # 求余
        if FunctionName == 'Rem':
            sum = jd.Rem(int(Data1), int(Data2))
            if (sum == -999):
                bj = 1
                sum = "分母不能为 0 "
            else:
                bj = 0
            print("Rem:", sum)

       # 阶乘
        if FunctionName == 'Fac':
            sum = jd.Fac(int(Data1))
            print(sum)
            if ((sum == -999) | (sum<0 )):
                bj = 1
                sum = "只能计算(0-20）以内"
            else:
                bj = 0
            print("Fac:", sum)

        # sayHello
        if FunctionName =='sayHello':
            sum = jd.sayHello(Data1)
            msg = sum
            print(sum)
            str1 =f"{msg}"
            return str1

        # sayNow
        if FunctionName == 'sayNow':
            sum = jd.sayNow(Data1)
            msg = sum
            print(sum)
            str1 = f"{msg}"
            return str1

        # 显示运行结果
        print("运行结果 sum=", sum)
        # 回调函数需要返回一个字符串类型，故如果 sum 是 int 数值类型的需要转换为字符串
        if isinstance(sum, int):
            msg = str(sum)
        else:
            msg = sum

        # print("================= 10 ====================")
        # 7.关闭jvm
        # Flask 的Bug 因为多线程，不能关闭JVM 虚拟机！！！！！！
        # jp.shutdownJVM()
        # system.exit()


    except:
        print("运行出错！")
        msg ="ERR"

    return msg





 # 在远程服务器上运行 script
def execute_remote_script(hostname, username, password, script):
    import paramiko
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(script)
    output = stdout.read().decode()
    error = stderr.read().decode()

    client.close()

    if output:
        print("Output:\n", output)
    if error:
        print("Error:\n", error)



# 本代码，用python 利用 paramiko  运行Python脚本
@app.route('/api/RunFilePy', methods=[ 'POST'])
def RunFilePy():
    import paramiko
    print("================== @app.route('/api/RunFilePy', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（服务器IP(ServerIP)、服务器路径(ServerIP)、本地路径(LocalPath）
    # 定义服务器信息
    hostname = request.form.get("ServerIP")
    username = 'root'
    password = 'Cstorfs_123'

    # 远程服务器存放上传Python文件的文件夹
    server_Path = request.form.get("ServerPath")
    # server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹

    # 应用程序所在的文件夹
    local_Path = request.form.get("LocalPath") # D:\WxMinPro

    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'Test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定

    # 人工智能服务器上运行的结果文件
    Out_File = 'test.out'   # 用户可以自己指定

    print(hostname,server_Path,local_Path,Python_File,Out_File)

    print("\n=================== 开始 Begin RunFilePy......========================\n")
    try:
        Local_Python_File = local_Path + '/' + Python_File    # 要上传到服务器上运行的本地文件
        Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
        Server_Out_File = server_Path + '/' + Out_File        # 服务器上 生成的程序运行结果文件
        Local_Out_File = local_Path + '/' + Out_File          # 服务器上 生成的程序运行结果下载到本地的路径
        #
        # print(f"3-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()

        # (4） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
        # print("\n=============================================================\n")
        # 动态生成 script
        # script ="nohup python /home/tyx/test.py > /home/tyx/test.out"
        script = "nohup python " + Server_Python_File + ' > ' + Server_Out_File
        print(f"4-0 在远程服务器（{hostname}）后台运行 Python 程序（{script} :")
        execute_remote_script(hostname, username, password, script)

        # 等待服务器运行结束
        time.sleep(20)

        # print("\n=============================================================\n")
        # （六） 在本地显示运行结果
        print(f"6-0 在本地显示运行结果 ({Server_Out_File} )")
        # script ="cat /home/tyx/test.out"
        script = "cat " + Server_Out_File
        execute_remote_script(hostname, username, password, script)
        msg = "运行成功！"

    except:
        msg ="ERR"


    print("\n=================== RunFilePy   End  ==============================\n")
    return msg


# 本代码，用python 利用 paramiko  下载运行结果文件（test.out)
@app.route('/api/DownloadPy', methods=[ 'POST'])
def DownloadPy():
    msg=''
    import paramiko
    print("================== @app.route('/api/DownloadPy', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（服务器IP(ServerIP)、服务器路径(ServerIP)、本地路径(LocalPath）
    # 定义服务器信息
    hostname = request.form.get("ServerIP")
    username = 'root'
    password = 'Cstorfs_123'

    # 远程服务器存放上传Python文件的文件夹
    server_Path = request.form.get("ServerPath")
    # server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹

    # 应用程序所在的文件夹
    local_Path = request.form.get("LocalPath") # D:\WxMinPro

    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定

    # 人工智能服务器上运行的结果文件
    Out_File = 'test.out'   # 用户可以自己指定

    print(hostname,server_Path,local_Path,Python_File,Out_File)

    print("\n=================== 开始（Begin DownloadPy.....========================\n")

    # Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    # Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径
    Server_Out_File = "/home/tyx/test.out"

    try:
        # print("\n============================1=================================\n")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()


        # (五） 下载生成的  /home/tyx/test.out
        # print("\n===========================2==================================\n")
        print(f"5-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")
        # sftp = ssh.open_sftp()
        # sftp.get('/home/tyx/test.out', r'D:\chatGPT-Program\test.out')
        try:
            # print("\n============================3=================================\n")
            sftp.get(Server_Out_File, Local_Out_File)
            print("成功下载[Test.out]文件！")
            # print("\n============================4=================================\n")
            # （六） 在本地显示运行结果
            # print(f"6-0 在本地显示运行结果 ({Server_Out_File} )")
            # # script ="cat /home/tyx/test.out"
            # script = "cat " + Server_Out_File
            # execute_remote_script(hostname, username, password, script)
            print(f"6-0 在本地显示运行结果 ({Local_Out_File} )")
            script ="cat /home/tyx/test.out"
            # script = "type " + Local_Out_File
            execute_remote_script(hostname, username, password, script)
            msg = "成功下载 [Test.out]文件！"
            print("成功下载 [Test.out]文件！")
        except:

            msg = "ERR"
            print("下载[Test.out]文件失败")

        # 关闭sftp
        sftp.close()
        # 关闭ssh
        ssh.close()

    except:
        msg ="ERR"
        print("下载[Test.out]文件失败！")

    print("\n===================  DownloadPy  End  ==============================\n")
    return msg



# 本代码，用python 利用 paramiko  下载运行结果文件（test.out)
@app.route('/api/DisplayPy', methods=[ 'POST'])
def DisplayPy():
    msg=''
    import paramiko
    print("================== @app.route('/api/DisplayPy', methods=[ 'POST']) ============================")
    # Fpath = request.args.get("file")
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数用：request.args.get("参数名称")
    # 如是form 的post 方式传递 ，用 request.form.get("参数名称")
    # 接受表单上用户输入的内容（服务器IP(ServerIP)、服务器路径(ServerIP)、本地路径(LocalPath）
    # 定义服务器信息
    hostname = request.form.get("ServerIP")
    username = 'root'
    password = 'Cstorfs_123'

    # 远程服务器存放上传Python文件的文件夹
    server_Path = request.form.get("ServerPath")
    # server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹

    # 应用程序所在的文件夹
    local_Path = request.form.get("LocalPath") # D:\WxMinPro

    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定

    # 人工智能服务器上运行的结果文件
    Out_File = 'test.out'   # 用户可以自己指定

    print(hostname,server_Path,local_Path,Python_File,Out_File)

    print("\n=================== 开始 Begin DisplayPy......========================\n")

    Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径
    # Server_Out_File = "/home/tyx/test.out"

    try:
        script = "cat " +Server_Out_File
        execute_remote_script(hostname, username, password, script)
        try:
            # Local_Out_File =r"D:\WxMinPro\Static\Receive\Py\test.out"
            print(Local_Out_File)
            # f = open(r'D:/WxMinPro/Static/Receive/Py/test.txt' ,'r',encoding="utf-8")
            f=open(Local_Out_File,'r',encoding="utf-8")
            # print("\n===================  222  ==============================\n")
            lines=f.readlines()
            msg=''
            for line in lines:
                msg = msg + line
            print(msg)
            f.close()
        except:
            msg = "ERR"
            print("读取[Test.out]文件失败！")
    except:

        msg = "ERR"
        print("下载[Test.out]文件失败")


    print("\n===================  DisplayPy  End  ==============================\n")
    return msg





@app.route('/api/data', methods=['GET'])
def get_data():
    global data_bj
    data_bj = data_bj+1
    data = {'message': f'Hello, World-{data_bj}'}
    print(data)
    return jsonify(data)

@app.route('/api/RemoteRun', methods=['GET'])
def RemoteRun():

    import paramiko
    import os
    import time

    # 定义服务器信息
    hostname = '10.30.1.110'
    username = 'root'
    password = 'Cstorfs_123'
    # 远程服务器存放上传Python文件的文件夹
    # server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹
    server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹
    # 应用程序所在的文件夹
    local_Path = os.getcwd()  # D:\chatGPT-Program
    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
    # 人工智能服务器上运行的结果文件
    Out_File = 'test.out'  # 用户可以自己指定

    print("\n=================== 开始 Begin RemoteRun......========================\n")
    print("返回操作系统类型（ windows:nt  linux:posix）:")
    print(os.name)  # 返回操作系统 windows:nt linux:posix
    print("返回当前工作目录:")
    print(os.getcwd())  # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

    # (1）在本地 登录远程人工智能的Linux 虚拟机 （10.30.1.110）
    # print("\n=============================================================\n")
    print(f"1-1 在远程服务器（{hostname}）上运行 liunx 命令: ls  -l ")
    script = "ls -l"
    execute_remote_script(hostname, username, password, script)

    # （2）-1 查看当前 虚拟环境下安装的包  conda  list
    # print("\n=============================================================\n")
    # print("2-1 查看当前 虚拟环境 (conda env export) :")
    # script = "conda env export"
    # execute_remote_script(hostname, username, password, script)

    # （2）-2 激活 虚拟环境  conda activate py3.7-Tensorflow
    # print("\n=============================================================\n")
    # print("2-2:激活 虚拟环境  conda activate py3.7-Tensorflow :")
    # script = "conda activate py3.7-Tensorflow"
    # execute_remote_script(hostname, username, password, script)

    # print("\n=============================================================\n")
    # # （2）-3 查看当前 虚拟环境下安装的包  conda  list
    # print("2-3 查看激活新的虚拟环境后的虚拟环境信息 (conda env export) :")
    # script ="conda env export"
    # execute_remote_script(hostname, username, password, script)

    # （3）  把本地的 py文件（temp-001.py 或 test.py) 上传到 10.30.1.110 的 /home/tyx/temp-001.py 或  /home/tyx/test.py
    # print("\n=============================================================\n")
    Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径

    print(f"3-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
    # sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test.py')
    sftp.put(Local_Python_File, Server_Python_File)
    # sftp.close()

    # (4） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
    # print("\n=============================================================\n")
    # 动态生成 script
    # script ="nohup python /home/tyx/test.py > /home/tyx/test.out"
    script = "nohup python " + Server_Python_File + ' > ' + Server_Out_File
    print(f"4-0 在远程服务器（{hostname}）后台运行 Python 程序（{script} :")
    execute_remote_script(hostname, username, password, script)

    # 等待服务器运行结束
    time.sleep(20)

    # (五） 下载生成的  /home/tyx/test.out
    # print("\n=============================================================\n")
    print(f"5-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")
    # sftp = ssh.open_sftp()
    # sftp.get('/home/tyx/test.out', r'D:\chatGPT-Program\test.out')
    sftp.get(Server_Out_File, Local_Out_File)

    # 关闭sftp
    sftp.close()
    # 关闭ssh
    ssh.close()

    # print("\n=============================================================\n")
    # （六） 在本地显示运行结果
    print(f"6-0 在本地显示运行结果 ({Server_Out_File} )")
    # script ="cat /home/tyx/test.out"
    script = "cat " + Server_Out_File
    execute_remote_script(hostname, username, password, script)

    print("\n===================  RemoteRun  End  ==============================\n")

    # ==========================
    global RemoteRun_bj
    RemoteRun_bj  = RemoteRun_bj +1
    data = {'message': f'RemoteRun-{RemoteRun_bj}'}
    print(data)
    return jsonify(data)


@app.route('/api/Upload', methods=['GET'])
def Upload():

    import paramiko
    import os
    import time

    # 定义服务器信息
    hostname = '10.30.1.110'
    username = 'root'
    password = 'Cstorfs_123'
    # 远程服务器存放上传Python文件的文件夹
    server_Path = '/root/'  # 人工智能服务器（10.30.1.110）的root
    # 应用程序所在的文件夹
    local_Path = os.getcwd()  # D:\chatGPT-Program
    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'movies-tf17.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
    # 人工智能服务器上运行的结果文件
    print("\n=================== 开始 Begin Upload......========================\n")
    print("返回操作系统类型（ windows:nt  linux:posix）:")
    print(os.name)  # 返回操作系统 windows:nt linux:posix
    print("返回当前工作目录:")
    print(os.getcwd())  # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

    # （1）  把本地的 py文件（temp-001.py 或 test.py) 上传到 10.30.1.110 的 /home/tyx/temp-001.py 或  /home/tyx/test.py
    # print("\n=============================================================\n")
    Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    print(f"1-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
    sftp.put(Local_Python_File, Server_Python_File)

    # 关闭sftp
    sftp.close()
    # 关闭ssh
    ssh.close()

    # print("\n=============================================================\n")
    # （2） 在本地显示上传结果
    print(f"2-0 在本地显示上传结果 ({ Server_Python_File} )")
    # script ="cat /home/tyx/test.out"
    script = "cat " +  Server_Python_File
    execute_remote_script(hostname, username, password, script)

    print("\n===================  Upload  End  ==============================\n")

    # ==========================
    global Upload_bj
    Upload_bj = Upload_bj + 1
    data = {'message': f'Upload-{Upload_bj}'}
    print(data)
    return jsonify(data)


@app.route('/api/Movies', methods=['GET'])
def Movies():
    # print("========= Movies ================")
    import paramiko
    import os
    import time

    # 定义服务器信息
    hostname = '10.30.1.110'
    username = 'root'
    password = 'Cstorfs_123'
    # 远程服务器存放上传Python文件的文件夹
    server_Path = '/root/'  # 人工智能服务器（10.30.1.110）的root
    # 应用程序所在的文件夹
    local_Path = os.getcwd()  # D:\chatGPT-Program
    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
    # 人工智能服务器上运行的结果文件
    Out_File = 'Movies.out'  # 用户可以自己指定

    print("\n=================== 开始Be gin Movies......========================\n")
    print("返回操作系统类型（ windows:nt  linux:posix）:")
    print(os.name)  # 返回操作系统 windows:nt linux:posix
    print("返回当前工作目录:")
    print(os.getcwd())  # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

    # （1）  把本地的 py文件（temp-001.py 或 test.py) 上传到 10.30.1.110 的 /home/tyx/temp-001.py 或  /home/tyx/test.py
    # print("\n=============================================================\n")
    Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径

    print(f"1-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
    # sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test.py')
    sftp.put(Local_Python_File, Server_Python_File)
    # sftp.close()

    # (2） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
    # print("\n=============================================================\n")
    Server_Python_File ="/root/movies-tf17.py"
    # 动态生成 script
    # script ="nohup python /home/tyx/test.py > /home/tyx/test.out"
    script = "nohup python " + Server_Python_File + ' > ' + Server_Out_File
    print(f"2-0 在远程服务器（{hostname}）后台运行 Python 程序（{script} :")
    execute_remote_script(hostname, username, password, script)

    # 等待服务器运行结束
    time.sleep(50)

    # (3） 下载生成的  /home/tyx/test.out
    # print("\n=============================================================\n")
    print(f"3-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")

    sftp.get(Server_Out_File, Local_Out_File)

    # 关闭sftp
    sftp.close()
    # 关闭ssh
    ssh.close()

    # print("\n=============================================================\n")
    # （六） 在本地显示运行结果
    print(f"4-0 在本地显示运行结果 ({Server_Out_File} )")
    # script ="cat /home/tyx/test.out"
    script = "cat " + Server_Out_File
    execute_remote_script(hostname, username, password, script)

    print("\n===================  Movies  End  ==============================\n")

    # ==========================
    global Movies_bj
    Movies_bj = Movies_bj + 1
    data = {'message': f'Movies-{Movies_bj}'}
    print(data)
    return jsonify(data)


# 将在人工智能服务器上生成的 电影推荐结果文件 movies.out 下载到本地
@app.route('/api/Download', methods=['GET'])
def Download():
    # print("========= Download ================")
    import paramiko
    import os
    import time

    # 定义服务器信息
    hostname = '10.30.1.110'
    username = 'root'
    password = 'Cstorfs_123'
    # 远程服务器存放上传Python文件的文件夹

    server_Path = '/root'  # 人工智能服务器（10.30.1.110）的root
    # 应用程序所在的文件夹
    local_Path = os.getcwd()  # D:\chatGPT-Program
    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
    # 人工智能服务器上运行的结果文件
    Out_File = 'movies.out'  # 用户可以自己指定


    print("\n=================== 开始（Begin Download......)========================\n")
    print("返回操作系统类型（ windows:nt  linux:posix）:")
    print(os.name)  # 返回操作系统 windows:nt linux:posix
    print("返回当前工作目录:")
    print(os.getcwd())  # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # 等待服务器运行结束
    time.sleep(3)

    # (2） 下载生成的  文件（Server_Out_File： movies.out)

    # 判断文件是否存在
    err_bj=0
    try:
        # print("\n=============================================================\n")
        print(f"1-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")

        sftp.get(Server_Out_File, Local_Out_File)

    except:
        print(f"1-0 在服务器上下载运行结果文件出错！，请检查（{Server_Out_File}) 是否存在？")
        err_bj=1
    # 关闭sftp
    sftp.close()
    # 关闭ssh
    ssh.close()
    if err_bj==0:
        # print("\n=============================================================\n")
        # （3） 在本地显示运行结果
        print(f"2-0 在本地显示运行结果 ({Server_Out_File} )")
        # script ="cat /home/tyx/test.out"
        script = "cat " + Server_Out_File
        execute_remote_script(hostname, username, password, script)

    print("\n===================  Download  End  ==============================\n")

    # ==========================
    global Download_bj
    Download_bj = Download_bj+1
    data = {'message': f'Download-{ Download_bj}'}
    print(data)
    return jsonify(data)


# 保存聊天记录到数据库 (2024-10-20 修改插入 MxName :'文心一言'  'GPT')
import pymysql.cursors
def SaveChat(que, msg, UserID ,UserName , Gender ,Birthday ,MxName):

    print(" 1===========================")
    print(que, msg, UserID, UserName, Gender, Birthday,MxName)
    # global  UserID,UserName,Gender, Birthday
    # import pymysql.cursors
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',  # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    # 插入数据

    Question = que
    # Answer = "苏州位于中国江苏省中部，东南临太湖，南临杭州湾，西北距上海约100公里。"
    Answer = msg

    # Question = "苏州在哪里"
    # Answer = "苏州位于中国江苏省中部，东南临太湖，南临杭州湾，西北距上海约100公里。"

    # 微信小程序，传过来的 UserID变成 str 类型，如果 UserID 为 int类型，则需要转换类型 ，选择为 字符串类型，故无需转换
    # UserID = int(UserID)

    # 常量（测试用）
    # UserID = 1001
    # Gender = '男'
    # Birthday = '2001-10-11'
    # UserName = '王小明'
    # 头像无需保存
    # print(" 2===========================")

    ChatTime = str(datetime.datetime.now())

    # print(Question,Answer, UserID, UserName, Gender, Birthday,ChatTime)

    sql = "INSERT INTO ChatTable( Question,   Answer,  UserID,  UserName, Gender,  Birthday,ChatTime,MxName) VALUES ('%s', '%s', %s,  '%s', '%s','%s' ,'%s' ,'%s')"
    # print(f" 3 {sql}")
    data = (Question, Answer, UserID, UserName,Gender,  Birthday ,ChatTime,MxName)
    cursor.execute(sql % data)
    # print(" 3===========================")
    connect.commit()
    print('成功插入数据')

    # 关闭数据库连接
    connect.close()

##############################################################33


# import os
import qianfan
# import warnings
# import logging
# warnings.simplefilter('ignore')  # 这将忽略所有警告信息
# logging.basicConfig(level=logging.WARNING)

# # sumeng  API_KEY  SECRET_KEY
# # API_KEY ='AfBIOUigTx4iYgCqwGYGVTF7'
# # SECRET_KEY ='q2TsQOfvEj3mdUtdOi7pq6nRXnOHx2g9'
#
# 李梓萌  API_KEY  SECRET_KEY
API_KEY = 'Shvn0A8QF1ilTqamHT21uIZ4'
SECRET_KEY = 'S2sOiPU2LuTMt8f5FCKr7PQIgJFXT8aB'

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_AK"] = API_KEY
os.environ["QIANFAN_SK"] = SECRET_KEY

# 文心一言聊天（千帆语言大模型）
def chatWxyy(questipon):
    try:
        chat_comp = qianfan.ChatCompletion()

        # 调用默认模型，即 ERNIE-Bot-turbo
        resp = chat_comp.do(messages=[{
            "role": "user",
            "content": questipon     #"content": "香格里拉"
        }])



        response_data = resp.body

        # 解析JSON字符串
        data = response_data

        # 提取result字段的值
        result_value = data['result']
    except:

        result_value ="调用问心一言出错，不能为你提供chat服务！"


    print(result_value)
    return result_value





# import openai
# import os
def chatGPT(question):
    # 指定 OpenAI API 的密钥
    # openai.api_key = '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'
    try:
        # openai.api_key = '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'

        # print(" 1 ===========================")
        openai.api_key = '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'

        os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"

        # q= [{"role": "user", "content": "你好"}]
        q = [{"role": "user", "content": question}]

        # print(" 2 ===========================")

        rsp = openai.ChatCompletion.create(
          # model="gpt-3.5-turbo-0301",
          model="gpt-3.5-turbo",
          messages=q
        )
        # print(" 3 ===========================")
        msg = rsp.get("choices")[0]["message"]["content"]
        # print(" 4 ===========================")

    except:
        # print(" 5 ===========================")
        msg ="调用openAI出错，不能为你提供chat服务！"
    # print(msg)
    return msg

# 将在人工智能服务器上生成的 电影推荐结果文件 movies.out 下载到本地
@app.route('/api/GPT', methods=['GET'])
def GPT( ):
    # 获取小程序提交的参数，这里使用
    # request.args.get()方法获取，
    # 若小程序发送的form表单参数，则使用
    # request.form.get()方法获取 ，注意理解这两种接收参数的形式

    # 接受微信小程序 get 方式传递的参数 question，如何是form 的post 方式传递 ，用 request.form.get("question")

    # Question
    # UserID = 1001 ，
    # UserName = '王小明',
    # Gender = '男',
    # Birthday = '2001-10-11'

    question = request.args.get("question")
    UserID = request.args.get("UserID")
    UserName = request.args.get("UserName")
    Gender = request.args.get("Gender")
    Birthday = request.args.get("Birthday")
    MxName = request.args.get("MxName")

    print("========= chatGPT 打印 微信小程序传过来的参数================")
    print(question,UserID ,UserName,Gender,Birthday,MxName)
    # msg ="江苏省-测试中"
    # question = "杭州在中国的哪一个省"
    try:
        if MxName =='文心一言':
            msg = chatWxyy(question)

        if MxName =='GPT':
            msg = chatGPT(question)

        # msg = "测试答案"
        que = question
        # 把 question  ， msg ，UserID ,UserName  , Gender ,Birthday  添加到数据库中
        # 保存聊天记录
        try:
            print(que, msg,UserID ,UserName  , Gender ,Birthday ,MxName)
            SaveChat(que, msg,UserID ,UserName  , Gender ,Birthday, MxName )
        except:
            msg ="保存聊天记录出错！"
    except:
        msg = "调用chatGPT(文心一言)错，不能为你提供解析服务！"

    global  GPT_bj
    GPT_bj= GPT_bj+1
    data = {'message': msg}
    # data = {'message': msg + f"-{GPT_bj}"}
    print(data)
    return jsonify(data)







##############################################################33
# Python 读取到微信小程序传递过来的表单内容
# import json
@app.route('/api/FormPost', methods=['POST'])
def FormPost():
    Phone = request.values.get("Phone")
    Code = request.values.get("Code")

    Phone = json.loads(Phone)
    Code = json.loads(Code)

    print(Phone)
    print(Code)
    message = {"Phone":Phone ,"Code":Code}
    return message



if __name__ == '__main__':
    app.run()



'''
wx.request({
  url: 'https://your-server-url/api', // 设置Flask API的URL
  method: 'POST',
  header: {
    'Content-Type': 'application/json' // 设置请求头为JSON类型
  },
  data: JSON.stringify({param1: value1}), // 设置参数，可以自定义字段和值
  success: function (res) {
    console.log('成功', res); // 打印返回结果
  },
  fail: function () {
    console.error('失败');
  }
})
'''

