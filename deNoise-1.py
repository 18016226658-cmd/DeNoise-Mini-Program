str = 'ESxnOW7QiUYFc22f2844135ada275fed69f46d9e4c0b-(DeNoise)-stereo.wav'
str2 = str[55:]
print(str2)
# str = 'ESxnOW7QiUYFc22f2844135ada275fed69f46d9e4c0b'



# import wave
# import numpy as np
#
#
# def read_wav(file_path):
#     with wave.open(file_path, 'rb') as wav_file:
#         frame_rate = wav_file.getframerate()
#         num_frames = wav_file.getnframes()
#         num_channels = wav_file.getnchannels()
#         sample_width = wav_file.getsampwidth()
#         audio_bytes = wav_file.readframes(num_frames)
#         audio_data = np.frombuffer(audio_bytes, dtype=np.int16)  # Assuming 16-bit samples
#
#         if num_channels != 1:
#             raise ValueError("The input WAV file is not mono (single channel).")
#
#         return frame_rate, audio_data
#
#
# def write_wav(file_path, frame_rate, num_channels, sample_width, audio_data):
#     num_frames = len(audio_data) // num_channels
#     audio_bytes = audio_data.tobytes()
#
#     with wave.open(file_path, 'wb') as wav_file:
#         wav_file.setnchannels(num_channels)
#         wav_file.setsampwidth(sample_width)
#         wav_file.setframerate(frame_rate)
#         wav_file.writeframes(audio_bytes)
#
#
# def merge_mono_to_stereo(file1, file2, output_file):
#     frame_rate1, audio_data1 = read_wav(file1)
#     frame_rate2, audio_data2 = read_wav(file2)
#
#     if frame_rate1 != frame_rate2:
#         raise ValueError("The frame rates of the two WAV files do not match.")
#
#     min_length = min(len(audio_data1), len(audio_data2))
#     audio_data1 = audio_data1[:min_length]
#     audio_data2 = audio_data2[:min_length]
#
#     # Merge into stereo (L, R)
#     stereo_audio_data = np.column_stack((audio_data1, audio_data2))
#     stereo_audio_data = stereo_audio_data.flatten()
#
#     # Write the stereo WAV file
#     sample_width = 2  # 2 bytes per sample for 16-bit
#     write_wav(output_file, frame_rate1, 2, sample_width, stereo_audio_data)
#
#
# # Usage example
# # file1 = r'D:\WxMinPro\Audio\download\DeNoise\2024-12-28--10-13-07-云南 (Live)-拉丹珠-吉萨莎玛-DeNoise(降噪)-1.wav'
# # file2 = r'D:\WxMinPro\Audio\download\DeNoise\2024-12-28--10-13-07-云南 (Live)-拉丹珠-吉萨莎玛-DeNoise(降噪)-2.wav'
#
# file1 = r'D:\WxMinPro\temp_audio1.wav'
# file2 = r'D:\WxMinPro\temp_audio2.wav'
# file1 = 'temp_audio1.wav'
# file2 = 'temp_audio2.wav'
# output_file = r'D:\WxMinPro\Audio\download\DeNoise\new_stereo_output-2.wav'
# merge_mono_to_stereo(file1, file2, output_file)



















# import librosa
# import numpy as np
# import soundfile as sf
#
#
# def preprocess_audio(file_path, sr=22050, n_fft=2048, hop_length=512, win_length=None):
#     """
#     加载音频文件并进行预处理（如降噪）。
#
#     参数:
#     file_path (str): 音频文件的路径。
#     sr (int): 采样率。
#     n_fft (int): FFT 窗口大小。
#     hop_length (int): 每个帧之间的样本数。
#     win_length (int): 每个帧的窗口长度（如果为 None，则默认等于 n_fft）。
#
#     返回:
#     y (np.ndarray): 降噪后的音频信号。
#     sr (int): 采样率。
#     """
#     # 加载音频文件
#     y, sr = librosa.load(file_path, sr=sr)
#
#     # 进行短时傅里叶变换 (STFT)
#     D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
#
#     # 计算功率谱密度 (Power Spectral Density, PSD)
#     magnitude, phase = librosa.magphase(D)
#     power_spectrogram = np.abs(magnitude) ** 2
#
#     # 计算噪声的功率谱密度（假设前1秒为噪声）
#     noise_duration = int(sr * 1)  # 1秒
#     noise_profile = np.mean(power_spectrogram[:, :noise_duration], axis=1, keepdims=True)
#
#     # 应用谱减法降噪
#     alpha = 2  # 过减因子 (over-subtraction factor)
#     clean_power_spectrogram = np.maximum(power_spectrogram - alpha * noise_profile, 0)
#
#     # 恢复幅度谱
#     clean_magnitude = np.sqrt(clean_power_spectrogram)
#
#     # 应用逆 STFT 得到降噪后的音频信号
#     clean_audio = librosa.istft(clean_magnitude * phase, hop_length=hop_length, win_length=win_length)
#
#     return clean_audio, sr
#
#
# # 使用示例
# # input_file = 'input_audio.wav'  # 输入音频文件路径
# # output_file = 'output_audio_denoised.wav'  # 输出音频文件路径
#
# input_file = r'E:\mp3\mp3\aa1.wav'
# output_file =r'E:\mp3\mp3\output_audio_denoised-1.wav'
#
# # 预处理音频并降噪
# clean_audio, sr = preprocess_audio(input_file)
#
# # 保存降噪后的音频文件
# sf.write(output_file, clean_audio, sr)
#
# print(f"降噪后的音频已保存到 {output_file}")