
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
X6=list(np.arange(0, len(result), 1))
Y6=result

print(X6)
print(Y6)
X66= list(map(int, X6))
X6 = X66
print(type(X6[1]))
print(type(Y6[1]))

# 可视化画图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号“-”显示异常

plt.plot(np.arange(0, len(result), 1), result, 'r-')
plt.xlabel('聊天序号（The Number of Wechat)')
plt.ylabel('情感（Sentiments）')
plt.title('基于chatGPT聊天情感分析（Sentiments of chatGPT）')
plt.show()
