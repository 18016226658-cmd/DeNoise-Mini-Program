import random
from datetime import datetime
import datetime
def CreateChatTime():
    now = datetime.date.today()
    year = random.randint(2020, now.year)
    if year==now.year:
        month = random.randint(1, now.month)
    else:
        month = random.randint(1, 12)
    if year == now.year & month == now.month:
        day =random.randint(1,now.day -1)    #不生成当天的聊天记录，否则会要判断 时分秒，以免生成 还没有到达的时刻
    else:
        day = random.randint(1, 28)
    if day == 0:
        day = 1
    # 模拟作息时间，在 0,1,2,3,4,5,5,。。。22,22,22,23 点的聊天斌率比较低
    hours =[ 0,1,2,3,4,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9,9,9,10,10,10,10,10,11,11,11,11,11,12,12,12,12,
             13,13,13,13,13,14,14,14,14,14,14,15,15,15,15,15,15,16,16,16,16,16,16,17,17,17,17,17,18,18,18,18,
             19,19,19,19,19,19,20,20,20,20,20,20,20,21,21,21,21,21,21,21,22,22,22,23]
    # hour = random.randint(0, 23)
    hour = random.choice(hours)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    date_time = datetime.datetime(year, month, day, hour, minute, second)
    # print(date_time)
    return  date_time

for i in range(1,1000):
    ChatTime=CreateChatTime()
    print(ChatTime)
