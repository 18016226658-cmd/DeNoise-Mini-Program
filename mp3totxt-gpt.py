
import os
# Third-party Library
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '115646617'
API_KEY = 'DX5dTvydZjEQnKJIXAKNk2Bg'
SECRET_KEY ='asm9u96ldnwaT5q28aYIpejPQSLhApNX'

GPT_bj=0

import openai
import os
from aip import AipSpeech

def chatGPTTest(question):
    # 指定 OpenAI API 的密钥
    # openai.api_key = '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'
    try:
        print(" 1 ===========================")
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




# # 与百度进行一次加密校验,认证你是合法用户合法的应用
# # AipSpeech是百度语音的客户端,认证成功之后,客户端将被开启,这里的client就是已经开启的百度语音的客户端了
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#
# # 1.将FPath格式文件转为pcm格式文件   单声道  16000采样
# FPath = r'd:/WxMinPro/static/SoundRecordFile/SoundRecordFile.mp3'
# def get_file_content(filePath):
#     # 执行cmd命令os.system()
#     os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
#     with open(f"{filePath}.pcm", 'rb') as fp:
#         return fp.read()  # 返回声音文件的2进制数据流
#
# # get_file_content(FPath)
# # 2.将音频转成文字
#
# # pcmPath =r'd:/WxMinPro/static/SoundRecordFile/SoundRecordFile.pcm'.encode()
# # res = client.asr(pcmPath, 'pcm', 16000,
# # try:
# res = client.asr(get_file_content(FPath), 'pcm', 16000,
#     {
#         'dev_pid': 1537,
#     })
# # 将录音转成文字,然后打印
# # print(res.get("result")[0])
#
# print(res.get("result"))
# # except:
# #     print("baidu aip error!")
# question =res.get("result")


question ='上海在哪里？'
try:
    msg = chatGPTTest(question)
    print("==================  msg = chatGPTTest(question) ==== ")
    print(msg)
    # msg = "测试答案"
    que = question
    # 把 question  ， msg ，UserID ,UserName  , Gender ,Birthday  添加到数据库中
    # 保存聊天记录

    print(que, msg, )

except:
    msg = "调用chatGPT错，不能为你提供chat服务！"

# global GPT_bj
GPT_bj = GPT_bj + 1

data = {'message': msg, 'question': que}
print(data)



chatGPTTest("苏州在哪里")













