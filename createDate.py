import datetime
import random
# 当前日 期年-月-日
now = datetime.date.today()

def birth(min_year,max_year):
    # 假设出生日期范围为60年前到当前时间之间（60*365=21600） 到 15年前 （15*365 =5475）
    min_days = min_year*365
    max_days = max_year *365
    n = random.randint(min_days, max_days)
    # n天前日期
    birth = now - datetime.timedelta(days=n)
    return birth


print('当前日期：', now)
# 生成10个随机日期
min_year = 15   #最小 15岁
max_year = 60   #最大 60岁
for i in range(20):
    d=birth(min_year,max_year)
    y=d.year
    nl = now.year -y
    print(d,y,nl)
