
import os
# Third-party Library
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '115646617'
API_KEY = 'DX5dTvydZjEQnKJIXAKNk2Bg'
SECRET_KEY ='asm9u96ldnwaT5q28aYIpejPQSLhApNX'


# 与百度进行一次加密校验,认证你是合法用户合法的应用
# AipSpeech是百度语音的客户端,认证成功之后,客户端将被开启,这里的client就是已经开启的百度语音的客户端了
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 1.将FPath格式文件转为pcm格式文件   单声道  16000采样
FPath = r'd:/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
def get_file_content(filePath):
    # 执行cmd命令os.system()
    os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()  # 返回声音文件的2进制数据流

# get_file_content(FPath)
# 2.将音频转成文字

# pcmPath =r'd:/WxMinPro/static/SoundRecordFile/SoundRecordFile.pcm'.encode()
# res = client.asr(pcmPath, 'pcm', 16000,
# try:
res = client.asr(get_file_content(FPath), 'pcm', 16000,
    {
        'dev_pid': 1537,
    })
# 将录音转成文字,然后打印
# print(res.get("result")[0])

print(res.get("result"))
# except:
#     print("baidu aip error!")











#
#
# #准备文本及存放路径
# Text='欢迎来到赣南医科大学' # 文字部分也可以从磁盘读取，或者是从图片中识别
# # filePath= "/Users/tuwenjing/Desktop/MyVoice.mp3 " #音频文件存放路径
# filePath = r'/WxMinPro/static/SoundRecordFile/SoundRecordFile.wav'
#
# if not isinstance (result, dict):
#     with open (filePath,'wb')as f: # 以写的方式打开MyVoice.mp3文件
#         f.write(result) # 将result内容写入MyVoice.mp3文件
# else:
#     print("错误")
#
#
#
# #语音合成
# result=client.synthesis (Text,'zh',1, {'vol': 5})
# print(result)
#



#
# # 读取文件
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
# filePath =r'D:\WxMinPro\static\SoundRecordFile\SoundRecordFile.wav'
# # 识别本地文件
# # client.asr(get_file_content('audio.pcm'), 'pcm', 16000, {
# res=client.asr(get_file_content(filePath), 'wav', 16000, {
#     'dev_pid': 1537,
# })
#
# print(res)

# 成功返回
# {
#     "err_no": 0,
#     "err_msg": "success.",
#     "corpus_no": "15984125203285346378",
#     "sn": "481D633F-73BA-726F-49EF-8659ACCC2F3D",
#     "result": ["北京天气"]
# }

# #失败返回
# {
#     "err_no": 2000,
#     "err_msg": "data empty.",
#     "sn": null
# }