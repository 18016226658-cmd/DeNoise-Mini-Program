
# 打印等腰三角形
n = 7
# 外部层循环控制每一行的打印
for i in range(1, n + 1):
    # 内部层循环控制每一行中空格的打印
    for j in range(1, n - i + 1):
        print(' ', end='')  # 打印空格

    # 内部层循环控制每一行中星号的打印
    for k in range(2 * i - 1):
        print('*', end='')  # 打印星号

    print()  # 换行


# import turtle
# import time
# turtle.color("red","yellow")
# turtle.begin_fill()
# for _ in range(50):
#     turtle.speed(0)
#     turtle.forward(200)
#     turtle.left(170)
# turtle.end_fill()
# turtle.mainloop()

