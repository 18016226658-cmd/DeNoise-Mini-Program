# Talk-chatGPT.py
'''
  【基于百度AIP及chatGPT实时语音聊天及情感分析系统研究】  Copyright®2020-2025  Applied Technology College Of Soochow University
  Title:  Research on Real Time Voice Chat and Emotion Analysis System Based on Baidu AIP and ChatGPT (Talk-chatGPT)
  Function:  Record to Wav Files,Recognition, PlayBack, Wave Figure,Speech-To-Text
  Software： Python 3.8.3             AipSpeech - playsound 1.2.3    WinX64
  Email:     xz_sumeng@163.com        Winxin:sm09040207
  Author：   Sumeng                   Date：  Oct 2,2023
'''

# from playsound import playsound
# import matplotlib.pyplot as pil

# 导入包
import CallChatGPT   as  chatGPT         # 用于调用 chatGPT（question)

from datetime import datetime

from aip import AipSpeech               # pip install baidu-aip
import wave
import pyaudio
import time
import os
import pylab as pl
import numpy as np
# from multiprocessing import  Process
# import  threading
import warnings
warnings.filterwarnings('ignore')
os.environ['TP_CPP_WIN_LOG_LEVEL']='3'

# 基本参数
CHUNK = 1024                 # 单位
FORMAT = pyaudio.paInt16     # 16位
CHANNELS =1                  # 单声道
RATE = 16000                 # 16000Hz 采样频率
RECORDE_SECONDS =10          # 每次录音时间
PREPARE_TIMES=3              # 录音之前的准备时间
IsRecognition=True           # 是否要语音识别
IsPlay=True                  # 是否要将chatGPT 生成的文本 转换为语音文件
Tstr=""

# 第一个参数的是你要转变的文字。第二个参数是中文的意思，第三个参数是1
# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 5
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 6
Fwave ="./chatGPT_answer.wav"     # 由chatGPT 生成的文本转换成的声音文件（wav）

myRECORDE_SECONDS=RECORDE_SECONDS
def print_Author_info():
    print("\n =======================================================================================================================")
    print("  【基于百度AIP和chatGPT实时语音聊天及情感分析系统研究】  Copyright®2023-2025  Applied Technology College Of Soochow University")
    print("  Title:  Research on Real Time Voice Chat and Emotion Analysis System Based on Baidu AIP and ChatGPT(Talk-chatGPT)")
    print("  Function:  Record to Wav Files,Recognition, chatGPT,PlayBack, Wave Figure,Talk-Text-chatGPT-Text-Wav")
    print("  Software： Python 3.8.3            baidu-aip 2.2.18.0  AipSpeech - playsound 1.2.3  openai 0.27.4  WinX64")
    print("  Email:     xz_sumeng@163.com       Winxin:sm09040207")
    print("  Author：   SuMeng&ZhongJiaNi        Date： Oct 3,2023")
    print(" ============================================================================================== ==========================")
    print("\n 语音识别音频文件应满足 （1）PCM编码 （2）单声道 （3）16位  （4）16000Hz （5）60秒以内  (6) WAV或PCM 格式")
    print("\n 语音实时聊天需连上百度AI云、openAI(chatGPT），请将你的计算机连接上因特网，开始加载数据，请耐心等待...... ")

# 初始化 聊天记录.txt
def clear_ans():
    global Fpath
    # 以下代码实现 如果\Record里已经有 【聊天记录.txt】文件，把它清空
    ansfile=r'.\Record\聊天记录.txt'
    # ansfile = Fpath +'\\Record\\聊天记录.txt'
    if os.path.exists(ansfile):
        # print("聊天记录.txt 已经存在，系统将删除它！")
        os.remove(ansfile)

    f=open(ansfile,'w')
    f.close()


# 采集语音（录音） 语音保存在 Fname 文件中
def record(Fname):
    global FORMAT ,CHANNELS ,RATE ,RECORDE_SECONDS ,PREPARE_TIMES ,CHUNK
    #      采样格式 ， 通道数 ，采样比率，采样时间（秒数） ， 录音之前的准备时间，单位，
    p= pyaudio.PyAudio()  # 申请一台录音机
    stream=p.open(format=FORMAT, channels=CHANNELS,rate=RATE ,input=True,frames_per_buffer=CHUNK)  # 打开录音机 （开始录音）

    print("    *** Recording......")
    frames=[]
    for j in range(0,int(RATE/CHUNK *RECORDE_SECONDS)):   # 采样率/单位 ： 一秒需要采集的贞数     总采集贞数：1秒需要采集的贞数*秒数
        data = stream.read(CHUNK)                         #采集到的 一贞声音数据
        frames.append(data)                               # 所有采集的声音贞，都放入 frames 列表中

    # print("\n 停止录音！")

    stream.stop_stream()    # 停止采集（录音）
    stream.close()          # 关闭 流设备
    p.terminate()           # 关闭 录音机

    wf= wave.open(Fname,'wb')            # 打开 Fname 用于写入声音数据 （2进制写）
    wf.setnchannels(CHANNELS)            # 设定 通道数   1 单通道
    wf.setframerate(RATE)                # 设定 采样率   16000
    wf.setsampwidth(p.get_sample_size(FORMAT))   # 设定 采样格式   pyaudio.paInt16     # 16位
    wf.writeframes(b''.join(frames))     # 把 声音文件 对应的贞数据，写入 wf(Fname)
    wf.close()               # 关闭 打开的文件

# 播放声音文件
def play_record(Fname):
    mywf = wave.open(Fname, 'rb')   # 打开声音文件（Fname） 用于 2进制读
    # 读 声音数据流  每次 1024个bit
    mydata=mywf.readframes(CHUNK)   # 读取第一贞数据 ，每一次 取出 一个单位（CHUNK ：1024）的 声音数据

    #  创建播放器
    myp= pyaudio.PyAudio()          # 申请一台播放机

    # 获取声音文件各参数格式
    myFORMAT=myp.get_format_from_width(mywf.getsampwidth())   # 取出原来写入 声音文件中的 采样格式
    myCHANNELS=mywf.getnchannels()                            # 取出原来写入 声音文件中的 通道数
    myRATE=mywf.getframerate()                                # 取出原来写入 声音文件中的 采样率


    # 屏幕提示
    print(f"\n 【声音文件参数】 格式（FORMAT）={myFORMAT}  通道数（CHANNELS）={myCHANNELS}   采样频率(RATE)={myRATE} (Hz) ")


    # 打开音频流 output=TRUE 表示输出 （播放）
    mystream=myp.open(format=myFORMAT, channels=myCHANNELS,rate=myRATE ,output=True,frames_per_buffer=CHUNK)

    # 按照 1024数据块的大小 读取播放
    # print("\n *** playding......")
    while len(mydata)>0:                  # 声音文件没有结束（还能取到非空的声音流）
        mystream.write(mydata)            # 向播放器送入一贞数据 （播放 一贞声音）
        mydata = mywf.readframes(CHUNK)   # 取下一贞声音数据

    mystream.stop_stream()                # 停止 播放
    mystream.close()                      # 关闭流设备
    myp.terminate()                       # 关闭 播放机
    mywf.close()                          # 关闭 打开的文件


# 显示波形图
def drow_wav(filename):
    # 打开WAV文档

    f = wave.open(filename, "rb")
    # 读取格式信息

    # (nchannels, sampwidth, framerate, nframes, comptype, compname)

    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    # 读取波形数据

    str_data = f.readframes(nframes)
    f.close()

    #将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)

    if nchannels == 2:                   # 双声道
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        time = np.arange(0, nframes) * (1.0 / framerate)

        # 绘制波形
        pl.subplot(211)
        pl.plot(time, wave_data[0])
        pl.subplot(212)
        pl.plot(time, wave_data[1], c="g")
        pl.xlabel("Time (seconds)")
        pl.show()

    elif nchannels == 1:                   # 单声道

        wave_data.shape = -1, 1
        wave_data = wave_data.T
        time = np.arange(0, nframes) * (1.0 / framerate)

        # 绘制波形
        pl.subplot(211)
        pl.plot(time, wave_data[0])
        pl.xlabel("Time (seconds)")
        pl.show()


# 连续录音
def multi_record():
    global  IsRecognition, IsPlay
    # 多次录音
    question = ""
    j=0
    while True:
        question = ""
        j+=1
        print(f"\n 请准备好话筒，{PREPARE_TIMES} 秒后可开始语音提问,每次录音 {RECORDE_SECONDS} 秒")
        time.sleep(PREPARE_TIMES)
        print(f"\n 第{j}次提问开始...")
        filename=".\Record\\"+"record_"+str(j)+".wav"
        # filename='record_{}.wav'.format(j)
        try:
            record(filename)   # 采集声音（录音） 并将数据写入 filename 文件
            print(f" 第{j}次提问结束!")
            time.sleep(1)
        except:
            print("\n 提问录音失败，请确保音频设备连接正常！")
        # 如果要进行语音识别（ 语音 转为 文本）
        if IsRecognition==True:
            print(f"\n 开始进行语音识别......")
            try:
                question=Speech_To_Text(filename)         # 将此语音文件 转换为 文本 ，即聊天的问题（question）
                if len(question)>0:
                    # answer = chatGPT.chatGPT(question)    # 将此问题，向chatGPT 提问，其结果为 answer
                    answer = "测试中......,你负责貌美如花，我负责攒钱养家!"              # 如果 不使用 chatGPT 请用本语句替代上面的 一行
                    print(f"\n【chatGPT】:"+answer)
                    # print(answer)                         # 屏幕显示 chatGPT的回答内容
                    write_text(question,answer)           # 将问题 和 答案 写入 【聊天记录.txt】
                else:
                    print("\n 请提出问题！")

            except:
                print("\n 语音识别 或 调用chatGPT 失败！")


        # 将【chatGPT}生成的答案转换成语音
        if IsPlay==True :
            print("\n 开始将【chatGPT}生成的答案转换成语音 ......")
            try:
                Text_to_Speech(answer,PER, SPD, PIT, VOL, AUE, Fwave)

                try:
                    play_record(Fwave)
                except:
                    print("\n 回放答案语音文件失败！")
            except:
                print("\n 【chatGPT}答案文本转换语音失败！")

            # print(f"\n 开始显示波形图......")
            # try:
            #     drow_wav(Fwave)
            # except:
            #     print("\n 显示波形图失败！")




        Fnext = input("\n 按【Q】键结束录音，【回车】键继续进行下一次录音： ")
        # Fnext =input("\n\033[1;31;40m" + " 按【Q】键结束录音，【回车】键继续进行下一次录音：" + "\033[0m")
        if len(Fnext) > 0:
            if Fnext in 'Qq':
                break


# 将 语音转换为 文本
def Speech_To_Text(Fname):

    global Tstr   # 问题 + 答案 的聊天过程字符串

    # sumeng 2023- 10 - 02 申请的开发者账号：
    # APP_ID = "40371226"
    # APP_KEY = "ABuoooMN5LGs9GPFKQg2jR5j"
    # SECRET_KEY = "3fwTAG9Syhmuw6Ew8wvwsw5akZgmZ8kZ"
    # APP_ID = "20265615"
    # APP_KEY = "7HdKRT9MkGZcYGQU06Y0FGEn"
    # SECRET_KEY = "DE7Fj6AXxXGdez24KZWIrlDTh3ceWlSt"
    APP_ID = "49135791"
    APP_KEY = "g2xKDg3rAmzqI6LCAVdcSMd8"
    SECRET_KEY = "QhiVGFDPd7P8NdIX4rKhGpEcvOjg3ubX"

    ans = ""
    # 与百度进行一次加密校验,认证你是合法用户合法的应用
    # AipSpeech是百度语音的客户端,认证成功之后,客户端将被开启,这里的client就是已经开启的百度语音的客户端了
    try:
        client = AipSpeech(APP_ID,APP_KEY,SECRET_KEY)  # 申请百度 api 调用的客户机
        while True:
            open_success=False


            try:
                with open(Fname, 'rb') as fp:
                    au = fp.read()             # 读入声音文本（2进制方式） 到 au中
                open_success=True
            except:
                print("\n 打开语音文件失败！")
                open_success=False

            if open_success:
                try:
                    res = client.asr(au, 'pcm', 16000, {'dev_pid': 1537, })  # 正式调用 百度aip 进入语音识别为 文本
                    # print(res)
                    ans = "".join(res['result'])                             # 提取 识别结果（文本）
                    print("\n 【你的问题】： " + "".join(res['result']))
                except:
                    print("\n 向百度发起【client.asr】客户请求失败！")


            break

    except:
        print("\n 请检查网络是否连接或你的百度 API 账号是否正确？")

    return ans

# 文本转声音文件

def  Text_to_Speech(ANS,PER ,SPD,PIT,VOL,AUE,Fname):
    # sumeng 2023- 10 - 02 申请的开发者账号：
    # APP_ID = "40371226"
    # APP_KEY = "ABuoooMN5LGs9GPFKQg2jR5j"
    # SECRET_KEY = "3fwTAG9Syhmuw6Ew8wvwsw5akZgmZ8kZ"
    # APP_ID = "49135791"
    # APP_KEY = "g2xKDg3rAmzqI6LCAVdcSMd8"
    # SECRET_KEY = "QhiVGFDPd7P8NdIX4rKhGpEcvOjg3ubX"
    APP_ID = "20265615"
    APP_KEY = "7HdKRT9MkGZcYGQU06Y0FGEn"
    SECRET_KEY = "DE7Fj6AXxXGdez24KZWIrlDTh3ceWlSt"
    # 与百度进行一次加密校验,认证你是合法用户合法的应用
    # AipSpeech是百度语音的客户端,认证成功之后,客户端将被开启,这里的client就是已经开启的百度语音的客户端了
    try:
        client = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)  # 申请百度 api 调用的客户机
        while True:
            open_success = False

            try:
                # result = client.synthesis("做我女朋友吧,你负责貌美如花，我负责攒钱养家", "zh", "1", {
                result = client.synthesis(ANS, "zh", "1", {
                    "vol": VOL,  # 音量
                    "spd": SPD,  # 音速
                    "pit": PIT,  # 语调
                    "per": PER,  # 0:女，1:男,3:逍遥,4:萝莉 5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
                    "aue": AUE
                })
                print("\n 已成功将文本转换成语音！" )
            except:
                print("\n 向百度发起【client.synthesis】客户请求失败！")

            break

    except:
        print("\n 请检查网络是否连接或你的百度 API 账号是否正确？")

    try:
        with open(Fname,"wb") as f:
            f.write(result)
            f.close()
    except:
        print("\n 写入语音文件出错？")

    # play_record(fname)





# 把 聊天问题 和 chatGPT 答案 写入 文件
def write_text(question,answer):
    global Fpath ,Tstr
    text1 = "【你的问题】：" + question
    text2 = "【GPT回答】：" + answer
    ansfile = '.\Record\\聊天记录.txt'     #相对路径

    # ansfile =Fpath + '\\Record\\聊天记录.txt'

    # 因为要多次识别，故要追加方式打开 （绝对路径方式打开）
    try:
        file1 = open(ansfile, 'a', encoding='utf-8')

        try:
            Tstr = Tstr + text1 +"\n"
            file1.write(text1)
            file1.write("\n ")  # 避免段太长 ，人为分段
            file1.write(text2)
            Tstr = Tstr + text2 +"\n\n"
            file1.write("\n\n ")
            file1.close()

        except:
            print("\n 写【聊天记录.txt】文件错！")
    except:
        print("\n 打开【聊天记录.txt】文件出错")


def main():

    print_Author_info()
    clear_ans()          # 【聊天记录.txt】文件
    multi_record()       # 循环聊天

    if len(Tstr) > 0:
        print("\n\n\n ===========【聊天完毕】===========     ")
        print("\n ===【请浏览【你的问题】及【GPT答案】===\n\n" + Tstr)
        mr = input("\n\n 按【回车】结束语音聊天:  ")

    print("\n 谢谢使用基于chatGPT的语音聊天系统！")
    time.sleep(2)



if __name__=="__main__":
    # myPass=myLogin()
    # if myPass==True:
    #     main()
    main()






