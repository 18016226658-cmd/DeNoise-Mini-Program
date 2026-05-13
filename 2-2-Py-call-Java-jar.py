# 2-2-Py-call-Java-jar.py
# python 利用jpype 类库 调用jar包中的java类
# 进入conda 自己的虚拟环境
# conda activate bil
# 安装  jpye1 包
# conda  install jpype1

import jpype as jp
import os

# 1.加载jar包 (事先把java 打成jar包）
jarpath ="./PyCallJava.jar"    #jar包所在位置 （可以打包后copy到 。py所在目录下）

# 2.获取jvm.dll 的文件路径
jvmPath = jp.getDefaultJVMPath()

# 3.开启jvm
jp.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jarpath))

# # 4.加载java类（参数是java的长类名）
JDClass = jp.JClass("com.example.JpypeDemo")
#注意：com.example为  java中  package com.example;
# JpypeDemo 中 java 中的主类

# # 5.实例化java对象
jd = JDClass()

# 6.调用java方法，由于我写的是静态方法，直接使用类名就可以调用方法
# jd.send()
print("9+7=",jd.Add(9,7))    # 调用calc(int a, int b)方法
print("9-7=",jd.Sub(9,7))    # 调用calc(int a, int b)方法
print("3*7=",jd.Mul(3,7))    # 调用calc(int a, int b)方法
print("24/7=",jd.Div(24,7))    # 调用calc(int a, int b)方法
print("19+7=",jd.Rem(19,7))    # 调用calc(int a, int b)方法
print("3!=",jd.Fac(3))     # 调用factor(int n)方法
print("10!=",jd.Fac(10))   # 调用factor(int n)方法
s = jd.sayHello(" 中秋快乐！")       # 调用sayHello(String user)方法
print(s)
s = jd.sayNow(" Sumeng")       # 调用sayHello(String user)方法
print(s)
# 7.关闭jvm
# jp.shutdownJVM()
# pass

'''
下面为 JpypeDemo.java 程序
package com.example;

public class JpypeDemo {
    public static String sayHello(String user){ //注意！作为被 python调用的接口函数，需要是静态的，否则 python 端会报错
        return "Hello" + user;
    }
    public static int calc(int a, int b){ //注意！作为被 python 调用的接口函数，需要是静态的，否则 python 端会报错
        return a + b;
    }
    public static long factor(int n){ //注意！作为被 python调用的接口函数，需要是静态的，否则 python 端会报错
        long p=1 ,k;
        for ( k=1;k<=n;k++){
           p*=k;
        }
        return p;
    }

    public static void main(String[] args){
    }
}

'''




