# 导入必要的库
from pydub import AudioSegment
import wave
import numpy as np
from scipy.signal import butter, filtfilt

# pydub：用于加载和保存音频文件，它支持多种格式。
# wave：用于读取和写入WAV格式的音频文件。
# numpy：用于处理数组和矩阵运算，这里是处理音频数据。
# scipy.signal：提供信号处理的函数，这里使用了butter和filtfilt进行带通滤波。

# input_file = r'E:\mp3\mp3\aa1.wav'
# output_file =r'E:\mp3\mp3\output_audio_reduced_noise-2.wav'
input_file = r'E:\mp3\mp3\九儿_G调_双声道.wav'

output_file =r'E:\mp3\mp3\output_audio_reduced_noise-九儿.wav'
# 定义滤波函数
# butter_bandpass：根据给定的低频截止、高频截止、采样频率和滤波器阶数，设计巴特沃斯带通滤波器。
# bandpass_filter：应用设计好的滤波器到数据上。
'''
在信号处理中，尤其是使用巴特沃斯（Butterworth）滤波器时，order（阶数）是一个关键参数，它决定了滤波器的性能特征。阶数越高，滤波器的滚降特性（即滤波器从通带到阻带的过渡区域）越陡峭，但这也可能导致相位失真增加。因此，在选择阶数时需要权衡这两个因素。

在您的代码中，order=5是一个默认参数值，意味着使用五阶巴特沃斯滤波器。这个选择通常是基于经验或者特定的应用需求。在某些情况下，可能需要尝试不同的阶数以找到最佳的滤波效果。

现在，让我们来看看函数返回的内容：

return b, a（在butter_bandpass函数中）:
这里返回的是巴特沃斯滤波器的系数。b是分子系数，a是分母系数。这些系数定义了滤波器的传递函数。在数字信号处理中，滤波器的传递函数通常表示为有理函数，即分子和分母都是多项式。这些系数就是这些多项式的系数。

使用这些系数，您可以应用滤波器到任何数据上，这通常是通过卷积（在时域中）或者频域中的乘法来实现的。在您的代码中，这些系数被用于filtfilt函数，该函数执行前向和后向滤波，以消除相位失真。

return y（在bandpass_filter函数中）:
这里返回的是经过滤波器处理后的数据。y是滤波后的数据数组，它与输入数据data具有相同的形状。这个数组包含了原始数据通过巴特沃斯带通滤波器后的结果，即只有位于lowcut和highcut之间的频率成分被保留下来，而其他频率成分被抑制。

filtfilt函数通过先对数据进行前向滤波，然后进行后向滤波（即反向通过相同的滤波器），来消除由于滤波器引起的相位失真。这种方法的一个缺点是它会导致数据边缘的效应，因为数据在边缘处没有被完全对称地滤波。然而，在许多应用中，这种边缘效应是可以接受的，因为滤波后的数据中心部分通常是最感兴趣的。
'''

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# 加载音频文件
'''
pydub库中的AudioSegment.from_file函数确实可以处理多种音频格式，包括但不限于WAV文件。
然而，当涉及到降噪算法时，特别是当您使用基于频率的滤波方法（如巴特沃斯带通滤波器）时，
通常需要将音频数据转换为一种易于处理和分析的格式。
如果您的降噪算法不依赖于频率域的精确分析，或者您愿意接受MP3压缩可能带来的限制，
那么理论上您仍然可以尝试对MP3文件应用降噪算法。但是，您可能需要先使用pydub或
其他库将MP3文件转换为WAV格式，以便进行更精确的处理，然后再将处理后的数据转换回MP3格式（如果需要的话）。

另外，值得注意的是，pydub在处理MP3文件时可能会依赖于底层的FFmpeg库。因此，在使用pydub处理MP3文件之前，
请确保您的系统中已经安装了FFmpeg，并且pydub能够正确地找到并使用它。

总的来说，虽然降噪算法不一定仅限于WAV文件，但WAV格式通常更易于处理和获得更好的效果。
如果您打算对MP3文件应用降噪算法，请务必仔细考虑上述因素，并可能需要进行一些额外的处理步骤。
'''
# audio = AudioSegment.from_file("input_audio.wav", format="wav")
audio = AudioSegment.from_file(input_file, format="wav")
# 导出为临时WAV文件
temp_wav_file = "temp_audio.wav"
audio.export(temp_wav_file, format="wav")

# 读取WAV文件参数和数据
'''
n_frames是从getparams()返回的元组中获取的，它表示整个WAV文件中的帧数。
然后，readframes(n_frames)被用来读取整个文件的所有音频数据帧，
这些数据帧以字节的形式存储在audio_bytes变量中。

需要注意的是，audio_bytes变量中的数据是原始的音频数据，它还没有被转换为NumPy数组或者进行任何处理。
通常，你需要根据sampwidth和n_channels的值来将这些原始数据转换为适当的格式（比如16位PCM格式的NumPy数组），
以便进行进一步的处理和分析。
'''
'''
声道数（n_channels）、
采样宽度（sampwidth，以字节为单位）、
采样频率（fs，即每秒采样次数）
以及帧数（n_frames）。
'''

with wave.open(temp_wav_file, 'rb') as wav_file:
    params = wav_file.getparams()
    n_channels, sampwidth, fs, n_frames = params[:4]
    audio_bytes = wav_file.readframes(n_frames)

    # 根据采样宽度将音频数据转换为NumPy数组
    # 如果不是16-bit PCM，则转换为16-bit PCM
    if sampwidth == 1:  # 8-bit PCM
        print("sampwidth(1-8-bit PCM):", end=" ")
        print(sampwidth)
        dtype_in = np.uint8    # 8位有符号整数
        dtype_out = np.int16   # 16位有符号整数
        scale_factor = 256.0 / 32768.0  # 将8-bit数据缩放到-1到1之间，并转换为16-bit
    elif sampwidth == 2:  # 16-bit PCM
        print("sampwidth(2-16-bit PCM):", end=" ")
        print(sampwidth)

        dtype_in = np.int16
        dtype_out = np.int16
        scale_factor = 1.0 / 32768.0  # 将16-bit数据缩放到-1到1之间（如果需要）
    elif sampwidth == 4:  # 32-bit PCM
        print("sampwidth(4-32-bit PCM):", end=" ")
        print(sampwidth)

        dtype_in = np.int32
        dtype_out = np.int16
        scale_factor = 1.0 / 2147483648.0  # 将32-bit数据缩放到-1到1之间，并准备转换为16-bit
    else:
        print(f"Unsupported sample width: {sampwidth}")
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    '''
    audio_bytes是一个包含音频数据的字节序列，它可能是通过读取WAV文件或其他音频数据源得到的。 
    dtype_in是一个NumPy数据类型（dtype），它指定了数组中元素的数据类型和形状。对于音频数据，
    这通常是一个表示音频样本的数据类型，比如np.int16（对于16位PCM音频）或n
    p.float32（对于浮点音频数据）。
    np.frombuffer函数会根据dtype_in指定的数据类型来解析audio_bytes中的数据，并创建一个NumPy数组。
    这个数组中的每个元素都对应audio_bytes中的一个或多个字节，具体取决于dtype_in的大小。
    '''
    data = np.frombuffer(audio_bytes, dtype=dtype_in)

    # 如果音频是立体声，则分别处理两个通道
    if n_channels == 2:
        print("立体声 channels:", end=" ")
        print(n_channels)

        # 第一个冒号: 表示切片的开始位置是数组的起始位置（索引为0）。
        # 第二个冒号: 表示切片的结束位置是数组的结束位置（索引为 len(data) - 1）。
        # data[::2] 会从数组 data 中选择索引为偶数的所有元素（从0开始计数）。
        left_channel = data[::2]

        # data[1::2]会从数组data中选择索引为奇数的所有元素（从1开始计数），
        # 即它会跳过每个偶数索引的元素，并从第一个奇数索引（即索引1）开始选择。
        right_channel = data[1::2]

        '''
        tereo_data = np.array([
            0x01, 0x00,  # 左声道第一个样本（0x0001）
            0x02, 0x00,  # 右声道第一个样本（0x0002）
            0x03, 0x00,  # 左声道第二个样本（0x0003）
            0x04, 0x00   # 右声道第二个样本（0x0004）
        ], dtype=np.uint8)
        '''

        # 对每个通道进行滤波
        left_filtered = bandpass_filter(left_channel, lowcut=100, highcut=3000, fs=fs)
        right_filtered = bandpass_filter(right_channel, lowcut=100, highcut=3000, fs=fs)

        # 将滤波后的通道合并回一个数组，并保持为16-bit PCM编码
        data_filtered = np.empty((left_filtered.size + right_filtered.size,), dtype=dtype_out)
        data_filtered[::2] = left_filtered.astype(dtype_out) * 32768  # 缩放回16-bit范围
        data_filtered[1::2] = right_filtered.astype(dtype_out) * 32768  # 缩放回16-bit范围（注意：这里假设我们想要保持原始振幅范围）
    else:
        print("单声道channels:", 'end=')
        print(n_channels)
        # 如果音频是单声道，则直接处理整个数据
        data_filtered = bandpass_filter(data, lowcut=100, highcut=3000, fs=fs)
        data_filtered = data_filtered.astype(dtype_out) * 32768  # 转换为16-bit PCM并缩放

# 将处理后的数据转换回音频字节数据
audio_bytes_filtered = data_filtered.tobytes()

# 写入新的WAV文件
# with wave.open("output_audio_reduced_noise.wav", 'wb') as wav_file:
with wave.open(output_file, 'wb') as wav_file:
    n_channels_out = 2 if n_channels == 2 else 1  # 保持原始声道数
    sampwidth_out = 2  # 16-bit PCM
    n_frames_out = len(data_filtered) // (n_channels_out if n_channels_out > 1 else 1)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((n_channels_out, sampwidth_out, fs, n_frames_out, comptype, compname))
    wav_file.writeframes(audio_bytes_filtered)

# 删除临时文件
import os
os.remove(temp_wav_file)