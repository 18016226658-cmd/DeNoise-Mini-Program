'''
基于 scipy 和 pydub 自适应音频降噪算好
在这个示例中，我们使用 wave.open 来打开 WAV 文件，并使用 getparams 方法获取音频参数。然后，我们使用 readframes 方法读取音频数据，
并将其转换为 NumPy 数组。接下来，我们应用带通滤波器进行降噪。最后，我们将处理后的数据转换回音频数据，并使用 wave.open 以写模式打开一
个新的 WAV 文件，将处理后的音频数据写入其中。
请注意，这个示例假设音频数据是 16-bit PCM 编码的。如果你的音频文件使用不同的编码或位深度，你需要相应地调整代码中的 dtype。
此外，如果音频是立体声的，代码将只处理左通道。如果你需要处理双声道，你需要对两个通道分别进行滤波，并将它们合并回一个立体声输出。
'''

# 导入必要的库
from pydub import AudioSegment  # 用于处理音频文件
import wave                     # 用于读取和写入WAV格式的音频文件
import numpy as np              # 用于数值计算
from scipy.signal import butter, filtfilt  # 用于设计数字滤波器和应用滤波器
import os
import json
# from flask import jsonify
from flask import Flask, jsonify, request,send_from_directory
from flask_cors import CORS
f = Flask(__name__)

app = f
CORS(app, origins='*')  # 允许所有域的请求，生产环境中应限制为特定的域

# input_file = r'E:\mp3\mp3\aa1.wav'
input_file = r'九儿_G调_双声道.wav'

output_file =r'E:\mp3\mp3\output_audio_reduced_noise-九儿.wav'
######################################################
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
    b, a = butter(order, [low, high], btype='band')  #butter 函数用于设计一个指定阶数、低截止频率和高截止频率的巴特沃斯带通滤波器

    '''
    butter 函数的一般形式
    b, a = butter(N, Wn, btype='low', analog=False, output='ba')
    N：滤波器的阶数。在您的代码中，这个参数由 order 变量提供。阶数越高，滤波器在截止频率处的滚降越陡峭，但相位失真也可能越大。
    Wn：归一化截止频率。在您的代码中，这个参数由 [low, high] 提供，其中 low 和 high 是相对于奈奎斯特频率（Nyquist frequency，即采样频率的一半）的归一化低截止频率和高截止频率。
    btype：滤波器的类型。可以是 'low'（低通）、'high'（高通）、'band'（带通）或 'bandstop'（带阻）。在您的代码中，这个参数被设置为 'band'，表示设计的是一个带通滤波器。
    analog：如果为 True，则返回一个模拟滤波器；如果为 False（默认值），则返回一个数字滤波器。
    output：输出类型。'ba'（默认值）表示返回滤波器的分子（b）和分母（a）系数，这些系数定义了滤波器的传递函数。其他选项可能包括 'zpk'（零极点增益形式）或 'sos'（第二阶节形式）。
    '''

    return b, a   #返回的是巴特沃斯滤波器的系数。b是分子系数，a是分母系数。这些系数定义了滤波器的传递函数。在数字信号处理中，滤波器的传递函数通常表示为有理函数


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

def DeNoise_all(input_file,output_file):
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
            print(new_output_file)

            merge_mono_to_stereo(temp_wav_file1, temp_wav_file2, new_output_file)
            os.remove(temp_wav_file1)
            os.remove(temp_wav_file2)
            print("==================== 7-7   os.remove(temp_wav_file1)  os.remove(temp_wav_file2) ")

        if n_channels == 1:
            # 输出新的路径  mono_to_stereo
            new_output_file = new_path + '-mono.wav'
            print(new_output_file)
            print("==================== 7-8  n_channels == 1 ")
            left_channel_data = data[::2]
            DeNoise_mono(left_channel_data, new_output_file,fs)
            print("==================== 7-9 DeNoise_mono(left_channel_data, new_output_file,fs)  end ")
    os.remove(temp_wav_file)
    return 200

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


# def DeNoise(input_file,output_file):
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
#         import os
#
#         os.remove(temp_wav_file)
#         return 200
#     except:
#         return 0


# # 降噪处理
# @app.route('/api/DeNoiseAudio', methods=['POST'])
def DeNoiseAudio():
    try:
        print("==================== 0 DeNoiseAudio")
        # data = request.get_json()  # 解析 JSON 数据
        # audioPath = data.get("audioPath")      # http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav
        # file_path = data.get("filePath")       # http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav
        # fileSize = data.get("fileSize")        # 0.00
        # duration = data.get("duration")        # 00:00:00
        # orgFileName= data.get("orgFileName")   # 古城之恋-和文军丽江 礼物.wav
        # filename = data.get("filename")        # nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07
        # extension = data.get("extension")      # wav
        # title = data.get("title")              # 空白
        # artist = data.get("artist")            # 空白
        # album = data.get("album")              # 空白

        audioPath =  'http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav'
        file_path = 'http://tmp/nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07.wav'
        fileSize =  '0.00'
        duration = '00:00:00'
        orgFileName =' 古城之恋-和文军丽江 礼物.wav'
        filename ='nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07'
        extension = 'wav'
        title = ' '# 空白
        artist ='' # 空白
        album = '' # 空白
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

        # 注意：此函数已废弃，实际实现请参考 api/audio.py 中的 denoise_audio()
        # 新代码已改为从 backend/Audio/input 读取文件，输出到 backend/Audio/uploads/DeNoise

        ################################################
        # 使用 os.path.splitext 分离文件名和扩展名
        orgFileName_Main, orgFileName_extension = os.path.splitext(orgFileName)
        myTitle0 = '(DeNoise).wav'

        # 生成降噪后的音频文件名，因为要在微信小程序中用 audio组件播放，不能带中文字符，new_filename能保证不会重复
        new_filename = filename + '-' + myTitle0  # nkmHu0DSpZ1m21f6caffe0ef74c97742eef4a3038f07-(DeNoise).wav

        print("==================== 5 new_filename")
        print(new_filename)

        # 下载文件到服务器上的临时位置
        try:
            # print(" DeNoise_audio()============================ 6")

            # 注意：此函数已废弃，实际实现请参考 api/audio.py 中的 denoise_audio()
            # 新代码应使用：backend/Audio/uploads/DeNoise 目录
            output_file = None  # 占位符，实际应使用新路径

            # 打印结果
            print("================================== 6 output_file")
            print(output_file)

            print("============= 7 开始进入 =DeNoise_all(input_file, output_file)")
            # 调用降噪程序
            res=DeNoise_all(input_file, output_file)
            print("============= 8  退出 DeNoise_all(input_file, output_file) res:")
            print(res)
            if res==200:
                result = {"success": 1, "files": new_filename}

                DeNoisePath = r"http://usr/Audio/output/DeNoise/"+new_filename

                DeNoiseOK = '1'

                print("==================== 8 result")


                str_fileSize =str(fileSize)

                # // 将音频信息保存在mydata 变量中
                mydata = audioPath+"\n"  + file_path + "\n" + str_fileSize+ "\n" + duration + "\n" + orgFileName + "\n"+ filename + "\n"  + extension + "\n" + DeNoisePath+ "\n"  +  DeNoiseOK
                # // 观察mydata
                print(mydata)

                # 注意：以下代码已废弃，不再写入微信开发者工具临时目录
                # 新代码应使用数据库保存降噪信息，参考：api/audio.py 中的 save_denoise_data() 函数
                # text_to_write = mydata
                # AudioInfo_File = WX_TEMP_DIR + '/usr/DeNoiseInfo.txt'  # 已废弃
                # with open(AudioInfo_File, 'w', encoding='utf-8') as file:
                #     file.write(text_to_write)


                print("==================== 9 result")
                print(result)
                # response = jsonify(result)
                # response.status_code = 200  # 设置状态码为 200
                # return response
                # return jsonify(result), 200
                return  200
            else:
                print("==================== 10  401")
                # response = jsonify({"error": "0"})
                # response.status_code = 401  # 设置状态码为 401
                # return response
                # return jsonify({"error": "0"}), 401
                return  401

        except Exception as e:
            print("==================== 11 except Exception as e  402")
            print(e)
            # response = jsonify({"error": str(e)})
            # response.status_code = 402  # 设置状态码为 402
            # return response
            return  402

            # return jsonify({"error": str(e)}), 402

    except Exception as e:
        print("====================12 except Exception as e :500")
        print(e)
        # response = jsonify({"error": str(e)})
        # response.status_code = 500  # 设置状态码为 500
        # return response
        # return jsonify({"error": str(e)}), 500
        # return jsonify({"error": str(e)})
        return 500


######################################################

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


# Usage example
# file1 = r'D:\WxMinPro\Audio\download\DeNoise\2024-12-28--10-13-07-云南 (Live)-拉丹珠-吉萨莎玛-DeNoise(降噪)-1.wav'
# file2 = r'D:\WxMinPro\Audio\download\DeNoise\2024-12-28--10-13-07-云南 (Live)-拉丹珠-吉萨莎玛-DeNoise(降噪)-2.wav'
# output_file = 'D:\WxMinPro\Audio\download\DeNoise\stereo_output.wav'
# merge_mono_to_stereo(file1, file2, output_file)


# ============================================
# 以下代码已废弃（旧测试代码）
# 新代码请使用 api/audio.py 中的接口
# ============================================
# print(("开始降噪处理。。。。。。"))
# DeNoiseAudio()  # 已废弃：不再直接调用此函数


'''
这段代码的主要步骤包括：

导入库：导入处理音频所需的库，包括pydub（用于加载和导出音频文件）、wave（用于读取和写入WAV文件）、numpy（用于数值计算）以及scipy.signal中的butter和filtfilt函数（用于设计和应用滤波器）。
定义滤波器函数：定义两个函数butter_bandpass和bandpass_filter，分别用于设计带通滤波器和将滤波器应用到数据上。
加载音频文件：使用pydub的AudioSegment类加载WAV格式的音频文件。
导出临时WAV文件：由于pydub的AudioSegment对象不能直接转换为NumPy数组，因此需要将音频文件导出为临时WAV文件。
读取WAV文件：使用wave模块打开临时WAV文件，并读取音频参数（声道数、采样宽度、采样率、帧数）和音频数据。
转换音频数据：根据采样宽度将音频字节数据转换为NumPy数组，并（如果需要）从立体声转换为单声道。
应用滤波器：使用定义的带通滤波器函数对音频数据进行降噪处理。
转换回音频数据：将处理后的NumPy数组数据转换回音频字节数据，以便写入新的WAV文件。
写入新的WAV文件：使用wave模块打开一个新的WAV文件，设置音频参数，并写入处理后的音频数据。
清理临时文件：删除临时WAV文件以节省磁盘空间（可选步骤）。
'''