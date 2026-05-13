import pandas as pd
import jieba
from tkinter import _flatten
import os
import json
import numpy as np
from snownlp import SnowNLP

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

    print("====== 6  sentimentslist  result ======")
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

    print(" ============== 7  myPie ")
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

    print('================================ 8 测试 WordClod =====================================')


    ##############################  2024-12-8 begin
    # 分词
    comment_cut = comments['Question'].apply(jieba.lcut)  # 每一个弹幕评论都使用分词函数 lcut
    print("\n===================================  9  comment_cut  ===================\n")
    print(comment_cut)

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
    # print(type(word_fre))

    print("\n 11 ===================================  word_fre.index  ===================\n")
    print(word_fre.index)


    # 聊天问题“词” 如下
    '''
    Index(['冷锋', '狼', '诛', '虽远必', '危危', '真的', '犯', '雇佣兵', '烟雾弹', '中华',
           ...
           '大白天', '效应', '二等', '偏左', 'U', '军功', '2m', 'QBZ95', '教学楼', '最燃'],
          dtype='object', length=8925)
    '''

    # 将Series 数据 转换成 List类型
    # myList = []
    # for i in word_fre.index:
    #     if word_fre[i] > 1:  # word_fre['虽远必']
    #         myList += [(i, int(word_fre[i]))]  # ('虽远必' ,285)
    #
    # print(len(myList))  # 13
    # print(myList)

    '''
    [('冷锋', 163), ('狼', 157), ('诛', 154), ('虽远必', 151), ('危危', 143), ('真的', 141), ('犯', 135), ('雇佣兵', 134), ('烟雾弹', 133), ('中华', 129), ('吴京', 124), ('特种兵', 123), ('哈哈哈哈', 123), ('战狼', 119), ('电影', 115), ('中国', 105), ('这是', 100),...]
    '''

    print("\n 12 ===================================  WC1  ===================\n")

    WC1 =word_fre.to_dict()

    print(WC1)

    ############################## 2024-12-08  end


    #构造一个字典 Dict 型数据
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

    print("\n 13 ===================================  data  ===================\n")
    print(data)
    # 转为json
    res_json = json.dumps(data)
    print("\n 14 ===================================  res_json  ===================\n")
    print(res_json)
    # return 响应体, 状态码, 响应头，用于实现Flask后端向微信小程序前端页面 传递数据！！！！！！！！！！！！！！！！！！！！！
    # 数据在前端用 res.data.user_id 、res.data.user_Phone 、res.data.user_name......提取
    return res_json, 200, {"Content-Type": "application/json"}


aa=DtVisual()
print("\n 15 ===================================  aa  ===================\n")
print(aa)