
# 名称： createDialo.py
# 作者：Sumeng
# 日期：2024-02-24
'''
程序功能：
本程序，将 zhddline_lines.txt  电影对话记录数据集，模拟为 chatGPT 聊天记录集
   问题         答案        用户名       性别      出生日期      出生年份   岁数（年龄）
'Question'  'Answer'   'UserName'   'Gender'  ’Birthday'    'Year'    'NL'

用户名 、性别 、 出生日期 、 出生年份、岁数（年龄） 都是随机模拟的
最后写到 Excel文件中  Dialo.xlsx
'''


# import pymysql.cursors
import pandas as pd
import random
import datetime

# 当前日期：年-月-日
now = datetime.date.today()

# 随机产生 年龄（min_year,max_year ）之间的 出生年月，如（15岁 -60岁） ，返回日期型的：1970-10-13
def birth(min_year,max_year):
    # 假设出生日期范围为60年前到当前时间之间（60*365=21600） 到 15年前 （15*365 =5475）
    min_days = min_year*365
    max_days = max_year *365
    n = random.randint(min_days, max_days)
    # n天前日期
    birth = now - datetime.timedelta(days=n)
    return birth

# 模拟作息时间，随机产生 2020 年 到现在的一个聊天时间 ，返回日期时间型的：2021-10-07 10:54:25
def CreateChatTime():
    mynow = datetime.date.today()
    # 模拟不同年份的聊天斌率 ，体现 2023 年最高，方便以后 按照年份进行统计分析
    years =[2020 ,2021 ,2021,2022,2022,2022,2022,2023,2023,2023,2023,2023,2023,2023,2024,2024]
    year =  hour = random.choice(years)             # 只生成 myYear 如2020  到当年的聊天时间
    if year==now.year:
        month = random.randint(1, mynow.month)      # 如果是当年 ，只生成 当月之前的时间
    else:
        month = random.randint(1, 12)
    if year == mynow.year & month == mynow.month:   # 如果为当年当月，确保只生成前一天之前的时间
        day =random.randint(1,mynow.day -1)         # 不生成当天的聊天记录，否则会要判断 时分秒，以免生成 还没有到达的时刻
    else:
        day = random.randint(1, 28)                 # 暂时不考虑 闰年问题
    if day == 0:
        day = 1
    # 模拟作息时间，在 0,1,2,3,4,5,5,。。。22,22,22,23 点的聊天斌率比较低 ，可以对聊天此次 按照一天中的 时间进行统计分析
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



# python随机生成姓名
# 姓氏列表
surnames = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何',
            '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏',
            '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史',
            '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅',
            '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹']
# 男人名字列表
Man_names = ['小', '明', '强', '亮', '敏', '洁','晓', '新', '建', '国', '军', '峰', '涛', '雷', '刚', '磊','亚' , '梦','龙','中','涛','桃','民','山','凌','阿','天','理','宏','高','争','正']

# 女人名字列表
Wen_names = ['小', '红', '丽', '美', '娜', '玲', '晓','燕', '露', '芳', '艳', '静', '婷', '敏', '洁', '雅', '雪', '琳', '晓', '兰', '莉',  '梦','英','妹','靓' , '媚' , '琳','妞','茜','溪']
# 男人姓名列表和女人姓名列表
Man = []
Wenmen = []

# 男人女人 出生年月
CSNY_Man ={}
CSNY_Wenmen ={}

# 男人女人 出生年份
YEAR_Man ={}
YEAR_Wenmen ={}

# 男人女人 岁数（年龄）
NL_Man ={}
NL_Wenmen ={}

# 随机生成40个男性姓名
for i in range(40):
    Man_surname = random.choice(surnames)  # 随机选一个
    Man_name = ''.join(random.sample(Man_names, 2))  # 随机选两个用空字符串连接
    Man.append(Man_surname+Man_name)

print(Man)  # 字符串连接

# 随机生成60个女性姓名
for i in range(60):
    Wen_surname = random.choice(surnames)  # 随机选一个
    Wen_name = ''.join(random.sample(Wen_names, 2))  # 随机选两个用空字符串连接
    Wenmen.append( Wen_surname+Wen_name)

print( Wenmen)  # 字符串连接


print('当前日期：', now)
# 生成10个随机日期
min_year = 15   #最小 15岁
max_year = 60   #最大 60岁

# 给40名 男性 随机生成一个  出生年月和年龄（岁数）
for i in range(40):
    d = birth(min_year, max_year)
    y = d.year
    nl = now.year - y
    print(d, y, nl)

    CSNY_Man[Man[i]] = d
    YEAR_Man[Man[i]] = y
    NL_Man[Man[i]] = nl

# 给60名 女性 随机生成一个  出生年月、出生年份和年龄（岁数）
for i in range(60):
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
with open('./zhddline_lines.txt', 'r',encoding='utf-8') as file:
    # 一次全部读到 lines 列表中
    lines = file.readlines()

#     # 遍历所以行，一次处理 2行 ，一行为 问题 ，一行为 聊天答案
    for i in range(0,len(lines)-1,2):           # 正式转换所有行
    # for i in range(0,100,2):                   # 测试用，仅仅处理前 100行 记录，产生 50对聊天数据
        # 将奇数行 和 偶数行去除 \n ，添加到DataFrame中的 'Question' 、 'Answer'，其它为  空白的字段，如 用户名 、性别、出生日期 、出生年份、岁数（年龄）、聊天时间
        df = df.append({'Question': lines[i].strip('\n'), 'Answer': lines[i+1].strip('\n'), 'UserName':'' ,'Gender':'','Birthday':now,'Year':now.year,'NL':0, 'ChatTime':now}, ignore_index=True)

print("=========================================================")
print("df.shape[0]:")
print(df.shape[0])
print("=========================================================")

# 对所有记录，添加 用户名 、性别、出生日期 、出生年份、岁数（年龄）
for i in range(df.shape[0]):
    n=df.index
    k =random.randint(1, 6)   # 产生 1、2、3、4、5   其中2/5 为男性  3/5为 女性
    if   k <=3:     # 1、2、3  3/5为 女性
         name = random.choice(Wenmen)                 # 随机选择一个女人
         df.loc[i,'UserName'] =name                   # 姓名  为聊天的用户名
         df.loc[i,'Gender']= '女'                     # 性别      该女人对应的 性别
         df.loc[i, 'Birthday'] =CSNY_Wenmen[name]     # 出生年月   该女人对应的 出生年月
         df.loc[i, 'Year'] = YEAR_Wenmen[name]        # 出生年份   该女人对应的 出生年份
         df.loc[i, 'NL'] = NL_Wenmen[name]            # 年龄      该女人对应的 年龄
    else:
        # 4、5   2/5为 男性
        name = random.choice(Man)                     # 随机选择一个男人
        df.loc[i,'UserName'] = name                   # 聊天童虎名
        df.loc[i,'Gender'] = '男'                     # 聊天者 性别
        df.loc[i, 'Birthday'] = CSNY_Man[name]        # 聊天者出生年月
        df.loc[i, 'Year'] = YEAR_Man[name]            # 聊天者出生年份
        df.loc[i, 'NL'] = NL_Man[name]                # 聊天者岁数

    df.loc[i, 'ChatTime'] = CreateChatTime( )      # 随机生成聊天时间为 2020年到现在的某一个时间

# 测试结果
for i in range(0, 10):
    print(df.loc[i, 'Question'])
    print(df.loc[i, 'Answer'])
    print(df.loc[i, 'UserName'])
    print(df.loc[i, 'Gender'])
    print(df.loc[i, 'Birthday'])
    print(df.loc[i, 'Year'])
    print(df.loc[i, 'NL'])
    print(df.loc[i, 'ChatTime'])

# 保存到excel 中
df.to_excel('./Dialo.xlsx', index=False)
