# 2-1-py-create-class-jar.py
# 本程序 利用 subprocess.call  执行 javac.exe 将 FileName_java  编译成 class字节码（位于myclass_path）
# 创建 配置文件 Main-Class.txt
# 依据 配置文件 Main-Class.txt 利用 subprocess.call  执行 jar.exe  将class字节码（位于myclass_path） 打成jar包（FileName_jar）

import subprocess
import os

#（1）下面为 键盘输入 打的包完整的主类名称，如：com.example.JpypeDemo
text0 = "Main-Class: com.example.JpypeDemo"
# text1 = input('请输入要打的jar包的完整的主类名称（如：com.example.JpypeDemo）：')
text1 = "com.example.JpypeDemo"
text2 = "Main-Class: "+text1
print("你要打成jar包的完整的主类名称为："+text2)

# （2）设置myclass所在路径
myclass_path ="C:/soft/myspark/PyCallJava/out/myclass"
FileName_txt = myclass_path + r"/Main-Class.txt"
FileName_jar =r'D:/WxMinPro/PyCallJava.jar'
FileName_java =r'C:/soft/myspark/PyCallJava/src/com/example/JpypeDemo.java'

# （3）将打包主类配置文件写入 FileName指定是文件中
file = open(FileName_txt,'w')
file.write(text2)

# （4）将java文件 编译为 class字节文件
# 本代码，用python 利用 javac.exe   将“。java" 源码程序，编译成 JpypeDemo.class 字节码 并且写在myclass文件夹中
# subprocess.call(['javac.exe', '-encoding', 'UTF-8', '-d',  r'C:/soft/myspark/PyCallJava/out/myclass', r'C:/soft/myspark/PyCallJava/src/com/example/JpypeDemo.java']) #ok
subprocess.call(['javac.exe', '-encoding', 'UTF-8', '-d',  myclass_path, FileName_java])

#javac -encoding UTF-8 -d C:\soft\myspark\PyCallJava\out\myclass JpypeDemo.java


# 切换到 myclass  必须要切换到生成的 class类中去运行（除非把 class字节文件copy到当前目录中）
os.chdir(myclass_path )


# （5）将当前的 myclass_path 下 com 根类下的 class文件 打为 jar包文件
# 基本格式
# jar -cvfm  PyCallJava.jar  Main-Class.txt  com

# 将 myclass  下主类 ”COM"下面的 class 字节码 打包到 当前目录中（myclass）中，命名为PyCallJava.jar 也可以打包到指定目录中
subprocess.call(['jar.exe', '-cvfm', FileName_jar,  FileName_txt, 'com'])


