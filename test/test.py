import numpy as np
import time

Mins= 2
Sleeps=1
t1 = time.time()
print("===== Begin...... =====")
for  i in range(0,Mins):
    for j in range(0,int(60/Sleeps)+1,10):
        time.sleep(Sleeps)
        print(f"当前运行到：{i} 分 {j*Sleeps} 秒")


t2 = time.time()
print(f"===== 程序运行结束！！======")
print(f"共运行：【{t2-t1} 秒】")