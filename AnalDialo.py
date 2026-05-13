import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Question , Answer, UserID, UserName, ChatTime, Gender, Birthday ,NL   Year
comments = pd.read_excel(r'./Dialo.xlsx')
df1=comments['UserName'].value_counts()

# comments['UserName']  # 本身没有更新
# # comments.head()
# num = comments['UserName'].value_counts().value_counts().sort_index(ascending=False)
# num2 = num[:200]    #前面8个

# (1) 聊天数量按照日期分布情况（line)
#######################################################
num =comments['ChatTime'].dt.date.value_counts().sort_index()
print(" ============== 1  聊天数量按照日期分布情况（line1)  ")
X1 = num.index[::30]
Y1 = []
for k in range(len(X1)):
    Y1.append(num[X1[k]])
X1=list(X1)
print(X1)
print(Y1)

# (2)聊天数量按照周次分布情况 （line)
num =comments['ChatTime'].dt.dayofweek.map({0:'周一' , 1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}).value_counts()
print(" ============== 2  聊天数量按照周次分布情况 （Pie)  ")
X2 = num.index
Y2 = []
for k in range(len(X2)):
    Y2.append(num[X2[k]])
X2=list(X2)
print(X2)
print(Y2)

x21 = X2
y22 = list(map(int, Y2))


myPie=[]
for k in range(len(x21)):
    dict1 ={'name':x21[k] ,'value':y22[k]}
    myPie.append(dict1)
print(myPie)
print(len(myPie))

# (3)聊天数量按照 一天里的时间点分布情况  （line)
num =comments['ChatTime'].dt.hour.value_counts().sort_index()
print(" ============== 3  聊天数量按照 一天里的时间点分布情况  （line3) ")

X3 = num.index
Y3 = []
for k in range(len(X3)):
    Y3.append(num[X3[k]])
X3=list(X3)
print(X3)
print(Y3)

# (4)聊天数量按照性别点分布情况 (bar1)
num =comments['Gender'].value_counts().sort_index()
print(" ============== 4  聊天数量按照性别点分布情况 (bar1) ")
X4 = num.index
Y4 = []
for k in range(len(X4)):
    Y4.append(num[X4[k]])
X4=list(X4)
print(X4)
print(Y4)

# (5) 聊天数量按照年龄分布情况  (bar2)
num =comments['NL'].value_counts().sort_index()
print(" ============== 5  聊天数量按照年龄分布情况  (bar2) ")
X5 = num.index
Y5 = []
for k in range(len(X5)):
    Y5.append(num[X5[k]])
X5=list(X5)
print(X5)
print(Y5)



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from datetime import datetime
# import os
# 聊天情感分析
from snownlp import SnowNLP
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

print("====== sentimentslist  result ======")
print(len(sentimentslist))
print(len(result))
X6=np.arange(0, len(result), 1)
Y6=result

print(X6)
print(Y6)


# 可视化画图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号“-”显示异常

plt.plot(np.arange(0, len(result), 1), result, 'r-')
plt.xlabel('聊天序号（The Number of Wechat)')
plt.ylabel('情感（Sentiments）')
plt.title('基于chatGPT聊天情感分析（Sentiments of chatGPT）')
plt.show()

