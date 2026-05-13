# Remote-Run.py
'''
库： paramiko、os
演示程序：test.py
前提条件：在本地能登录远程人工智能的Linux 虚拟机 （10.30.1.110）
  （a） 需要 连接苏大的 VPN EasyConnect
  （b） 需要 连接 人工智能平台的 OpenVPN GUI  （GPU）
程序功能：
1-1 在远程服务器（10.30.1.110）上运行 liunx 命令: ls  -l

2-1 查看当前 虚拟环境 (conda env export)

2-2:激活 虚拟环境  conda activate py3.7-Tensorflow 

3-0 把本地的 py文件（D:\chatGPT-Program/test.py) 上传到 人工智能平台（10.30.1.110） 的 /home/tyx/test.py

4-0 在远程服务器（10.30.1.110）后台运行 Python 程序（nohup python /home/tyx/test.py > /home/tyx/test.out

5-0 把服务器上的运行结果文件（/home/tyx/test.out) 下载到 D:\chatGPT-Program/test.out

6-0 在本地显示运行结果 (/home/tyx/test.out )

'''

import paramiko
import os
import time

# 定义服务器信息
hostname ='10.30.1.110'
username = 'root'
password = 'Cstorfs_123'
# 远程服务器存放上传Python文件的文件夹
server_Path = '/home/tyx'   #事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹
# 应用程序所在的文件夹
local_Path = os.getcwd()   #  D:\chatGPT-Program
#要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
Python_File = 'test.py'   #注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
#人工智能服务器上运行的结果文件
Out_File= 'test.out'      # 用户可以自己指定
# 在远程服务器上运行 script
def execute_remote_script(hostname, username, password, script):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(script)
    output = stdout.read().decode()
    error = stderr.read().decode()

    client.close()

    if output:
        print("Output:\n", output)
    if error:
        print("Error:\n", error)

print("\n=================== 开始（Begin......)========================\n")
print("返回操作系统类型（ windows:nt  linux:posix）:")
print(os.name) # 返回操作系统 windows:nt linux:posix
print("返回当前工作目录:")
print(os.getcwd()) # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

# (1）在本地 登录远程人工智能的Linux 虚拟机 （10.30.1.110）
print("\n=============================================================\n")
print(f"1-1 在远程服务器（{hostname}）上运行 liunx 命令: ls  -l ")
script ="ls -l"
execute_remote_script(hostname, username, password, script)

# （2）-1 查看当前 虚拟环境下安装的包  conda  list
print("\n=============================================================\n")
print("2-1 查看当前 虚拟环境 (conda env export) :")
script ="conda env export"
execute_remote_script(hostname, username, password, script)

# （2）-2 激活 虚拟环境  conda activate py3.7-Tensorflow
print("\n=============================================================\n")
print("2-2:激活 虚拟环境  conda activate py3.7-Tensorflow :")
script ="conda activate py3.7-Tensorflow"
execute_remote_script(hostname, username, password, script)


# print("\n=============================================================\n")
# # （2）-3 查看当前 虚拟环境下安装的包  conda  list
# print("2-3 查看激活新的虚拟环境后的虚拟环境信息 (conda env export) :")
# script ="conda env export"
# execute_remote_script(hostname, username, password, script)


# （3）  把本地的 py文件（temp-001.py 或 test.py) 上传到 10.30.1.110 的 /home/tyx/temp-001.py 或  /home/tyx/test.py
print("\n=============================================================\n")
Local_Python_File = local_Path +'/'+Python_File     # 要上传到服务器上运行的本地文件
Server_Python_File = server_Path +'/'+Python_File   # 上传到服务器上要运行的文件
Server_Out_File = server_Path +'/'+Out_File         # 服务器上 生成的程序运行结果文件
Local_Out_File = local_Path +'/' +Out_File          # 服务器上 生成的程序运行结果下载到本地的路径

print(f"3-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)
sftp = ssh.open_sftp()

# 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
# sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test.py')
sftp.put(Local_Python_File , Server_Python_File)
# sftp.close()


# (4） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
print("\n=============================================================\n")
# 动态生成 script
# script ="nohup python /home/tyx/test.py > /home/tyx/test.out"
script ="nohup python " + Server_Python_File +' > ' + Server_Out_File
print(f"4-0 在远程服务器（{hostname}）后台运行 Python 程序（{script} :")
execute_remote_script(hostname, username, password, script)

# 等待服务器运行结束
time.sleep(20)


# (五） 下载生成的  /home/tyx/test.out
print("\n=============================================================\n")
print(f"5-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")
# sftp = ssh.open_sftp()
# sftp.get('/home/tyx/test.out', r'D:\chatGPT-Program\test.out')
sftp.get(Server_Out_File, Local_Out_File)

# 关闭sftp
sftp.close()
# 关闭ssh
ssh.close()

print("\n=============================================================\n")
# （六） 在本地显示运行结果
print(f"6-0 在本地显示运行结果 ({Server_Out_File} )")
# script ="cat /home/tyx/test.out"
script ="cat " + Server_Out_File
execute_remote_script(hostname, username, password, script)


print("\n===================  The  End  ==============================\n")



# test。py 本地要上传到服务器上的 Python 程序
'''
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
'''






#
# import paramiko
#
# ssh = paramiko.SSHClient()                                     # 创建SSH对象
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())      # 允许连接不在know_hosts文件中的主机。即：解决问题:如果之前没有，连接过的ip，会出现选择yes
# # 连接服务器（根据自己的情况选择）
# # ssh.connect(hostname='192.168.128.130', username='root', password='123456')     # 用户名和密码登录
# ssh.connect(hostname='10.30.1.110', username='root', password='Cstorfs_123')     # 用户名和密码登录
# stdin, stdout, stderr = ssh.exec_command('ls -lh')
# result = stdout.read().decode('utf-8')   # 获取命令结果
# print(result)                            # 输出返回的结果
# stdin, stdout, stderr = ssh.exec_command('ssh root@10.30.1.110  conda activate py3.7-Tensorflow; python <  /home/tyx/test-put.py')    # 运行sh文件
# ssh.close()                              # 关闭连接



# # 2. 文件上传下载
# import paramiko
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname='10.30.1.110', username='root', password='Cstorfs_123')
#
# sftp = ssh.open_sftp()
# sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test-put.py')       # 将windows文件上传至Linux
# sftp.get('/home/tyx/test-put.py', r'D:\chatGPT-Program\test-get.py')       # 将Linux文件下载至windows
#
# sftp.close()
# #
# #
# stdin, stdout, stderr = ssh.exec_command('cat /home/tyx/test-put.py')    # 运行sh文件
# result = stdout.read().decode('utf-8')
# print(result)
#
# stdin, stdout, stderr = ssh.exec_command('ssh root@10.30.1.110  conda activate your_env; python < your_python_file /home/tyx/test-put.py')    # 运行sh文件
# ssh username@server_ip  conda activate your_env; python < your_python_file - arg1 arg2

# ssh.close()
#
# import paramiko
# import subprocess
# import base64
# def local_ssh(command):
#     p = subprocess.Popen([command],
#                          stdin=subprocess.PIPE,
#                          stdout=subprocess.PIPE,
#                          stderr=subprocess.PIPE, shell=True)
#     out = p.stdout.read().decode('utf-8')
#     # regex = r'time=(.+?)ms'
#     print(out)

#
# # 2 远程服务上执行指令
# def remote_ssh(sys_ip, username, command, password=''):
#     try:
#         # 创建ssh客户端
#         client = paramiko.SSHClient()
#         # 第一次ssh远程时会提示输入yes或者no
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         if len(password) != 0:
#             print('互信方式远程连接')
#             key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
#             client.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
#         else:
#             print('密码方式远程连接')
#             client.connect(sys_ip, 22, username=username, password=base64.b64decode(password).decode(), timeout=20)
#         print(f"开始在远程服务器上执行指令:{command}")
#         # 执行查询命令
#         stdin, stdout, stderr = client.exec_command(f"""{command}""")
#         # 获取查询命令执行结果,返回的数据是一个list
#         result_ls = stdout.readlines()
#         print(f"{sys_ip}执行结果:{result_ls}")
#         # return result
#     except Exception as e:
#         print(e)
#     finally:
#         client.close()


# # 调用方法：
# server_ip = "10.30.1.110"
# server_username = "root"
# server_password = "Cstorfs_123"
# # server_command = "rm -rf /root/1.txt"
# server_command = "python /home/tyx/test-put.py"
# remote_ssh(sys_ip=server_ip, username=server_username, command=server_command)

# ssh username@server_ip  conda activate your_env; python < your_python_file - arg1 arg2



# # 方法二：关注“测试开发自动化” 弓中皓，获取源码）
# import paramiko
#
# #获取Transport实例
# tran = paramiko.Transport("192.168.128.130", 22)
# #连接SSH服务端
# tran.connect(username="root", password="123456")
# #获取SFTP实例
# sftp = paramiko.SFTPClient.from_transport(tran)
# #设置上传的本地/远程文件路径
# localpath= r"D:\chatGPT-Program\test-put.py"    #本地文件路径
# remotepath= r"/home/tyx/test-put-2.py"  #上传对象保存的文件路径
# #执行上传动作
# sftp.put(localpath, remotepath)
# # 执行下载动作
# sftp.get(remotepath, localpath)
# tran.close()


#
# # 3. sudo权限：
# # 关注“测试开发自动化” 弓中皓，获取源码）
# import paramiko
#
# hostname = "192.168.128.130"
# username = 'ubuntu'
# password = 'ubuntu'
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname=hostname, username=username, password=password)
#
# stdin, stdout, stderr = ssh.exec_command('sudo reboot', get_pty=True)  # sudo权限
# stdin.write('ubuntu'+'\n')   # 输入密码
#
# result = stdout.read().decode('utf-8')
# print(result)
# ssh.close()

#
# import os
# import paramiko
#
# def main():
#
#     print os.name
#
#     if __name__ == '__main__':
#
#         try:
#
#             if sys.argv[1] == 'deploy':
#
#
#
#                 # Connect to remote host
#
#                 client = paramiko.SSHClient()
#
#                 client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#                 # client.connect('remote_hostname_or_IP', username='john', password='secret')
#                 client.connect('10.30.1.110', username='root', password='Cstorfs_123')
#
#                 # Setup sftp connection and transmit this script
#
#                 sftp = client.open_sftp()
#
#                 sftp.put(__file__, '/tmp/myscript.py')
#         except:
#             print("\n======== Error !============\n")




#
# # 4. 批量链接
# # 关注“测试开发自动化” 弓中皓，获取源码）
# import paramiko
# from paramiko.ssh_exception import NoValidConnectionsError
# from paramiko.ssh_exception import AuthenticationException
#
#
# # def connect(cmd, hostname,port=22,username='root',passwd='westos'):
# def connect(cmd, hostname, port=22, username='root', passwd='123456'):
#     ##1.创建一个ssh对象
#     client = paramiko.SSHClient()
#     #2.解决问题:如果之前没有，连接过的ip，会出现选择yes或者no的操作，
#     ##自动选择yes
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     #3.连接服务器
#     try:
#         client.connect(hostname=hostname, port=port, username=username, password=passwd)
#         print('正在连接主机%s......'%(hostname))
#
#     except NoValidConnectionsError as e: ###用户不存在时的报错
#         print("连接失败")
#     except AuthenticationException as t: ##密码错误的报错
#         print('密码错误')
#     else:
#         #4.执行操作
#         stdin,stdout, stderr = client.exec_command(cmd)
#         #5.获取命令执行的结果
#         result=stdout.read().decode('utf-8')
#         print(result)
#         #6.关闭连接
#     finally:
#         client.close()
#
# # 为提高效率，此处建议使用多线程
# connect('ls -h', hostname='192.168.128.130', username='root', password='123456')
# connect('ls -h', hostname='192.168.128.130', username='root', password='123456')
#
#
#



#
# from fabric import Connection # 建议将ssh连接所需参数变量化
# # user = '用户名'
# # host = 'host地址'
# # password = '密码'
#
# # 利用fabric.Connection快捷创建连接
# # c = Connection(host=f'{user}@{host}', connect_kwargs=dict( password=password ))
#
# # 利用run方法直接执行传入的命令
# # c.run('pwd');
#
# # 可以看到，非常简单就完成了连接服务器及执行指定命令的过程，且run()方法所执行的命令打印出的结果，可以通过stdout属性进行保存：
#
# # hide=True抑制run()过程对执行结果的自动打印
# output = c.run('df -h', hide=True).stdout print(output)
#
# from invoke import Responder # 配置命令行内容监听规则
# sudopass = Responder( pattern=f'\[sudo\] password for {user}:', response=password '\n' ) # 注意需要设置
# pty=True c.run('sudo pwd', pty=True, watchers=[sudopass])
#
# # (2) 方式2：利用fabric.Config设置sudo密码
# #
# # 除了上一种方式外，我们还可以使用fabric.Config在创建连接时就一次性提前配置好sudo密码，之后需要执行sudo命令时用sudo()方法代替run()方法即可：
#
# from fabric import Config # 预先配置sudo密码
# config = Config(overrides={ 'sudo': { 'password': password } })
# c = Connection(host=f'{user}@{host}', connect_kwargs={'password': password}, config=config)
# c.sudo('pwd')
#
# # 3. 远程文件传输
# # 很多朋友都知道可以使用pscp、xshell之类的工具手动进行服务器与本地之间的文件相互传输，这些任务我们同样可以在fabric中自动化进行：
# # (1) 从本地上传文件到服务器
# # 使用put()方法可以将指定的本地文件上传至服务器的指定位置，remote参数对应服务器目标保存位置：
#
# c = Connection(host=f'{user}@{host}', connect_kwargs={'password': password}) # 创建示例文件
# with open('file_transfer.txt', 'w') as d:
#     d.write('1')
#
#     # 利用put方法上传至服务器
#     c.put('file_transfer.txt', remote='/home/feffery/')
#
#     # 打印已上传文件内容
#     c.run('cat /home/feffery/file_transfer.txt')
#
#
# # (2) 从服务器下载指定文件到本地
# # 相反的，当我们需要从服务器取回指定文件到本地时，就可以使用get()方法：
#
# c = Connection(host=f'{user}@{host}', connect_kwargs={'password': password})
#
# # 向文件末尾追加行
# c.run('echo "\n2" >> file_transfer.txt')
# c.get('/home/feffery/file_transfer.txt')
# print(open('file_transfer.txt').read())


# import paramiko
# import json
#
#
# def read_config(config_path):
#     return json.load(open(config_path, 'r', encoding="utf-8"))
#
#
# def upload_scp_run_download(cfg_path):
#     cfg = read_config(cfg_path)
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_p


# 这种方式比较简单，没有进行封装。单纯的实现了远程连接linux服务器。
# 下面还有一种方式，是在这个方式的基础上将每个主要步骤做了封装，方便业务调用。
#
# import paramiko
# class ConnectShell:
#     def remotConnect(self):
#         # 服务器相关信息,下面输入你个人的用户名、密码、ip等信息
#         # ip = "192.168.1.110"
#         # ip = "10.30.1.110"
#         ip = "192.168.128.130"
#         port = 22
#         user = "root"
#         password = "123456"
#
#         # 创建SSHClient 实例对象
#         ssh = paramiko.SSHClient()
#
#         # 调用方法，表示没有存储远程机器的公钥，允许访问
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#         # 连接远程机器，地址，端口，用户名密码
#         ssh.connect(ip, port, user, password, timeout=10)
#
#         # 输入linux命令
#         ls = "ls"
#         stdin, stdout, stderr = ssh.exec_command(ls)
#
#         # 输出命令执行结果
#         result = stdout.read()
#         print(result)
#         # 关闭连接
#         ssh.close()
#         return
#
# if __name__ == '__main__':
#     # host = Linux('192.168.1.106', 'long', 'long')
#     host = ConnectShell()
#     host.remotConnect()
#
#


# 四、远程ssh连接服务器方式二
# 这个方式是在上面的第一种方式上进行了封装。

# 4.1定义一个linux类实现连接远程连接linux服务器
# #
# import paramiko
# # import refrom
# import time
# # import sleep
# # 定义一个类，表示一台远端linux主机
# #
# class Linux(object):
#     # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
#     def __init__(self, ip, username, password, timeout=30):
#         self.ip = ip
#         self.username = username
#         self.password = password
#         self.timeout = timeout
#         # transport和chanel
#         self.t = ''
#         self.chan = ''
#         # 链接失败的重试次数
#         self.try_times = 3
#         # 调用该方法连接远程主机
#     def connect(self):
#         while True:
#             # 连接过程中可能会抛出异常，比如网络不通、链接超时
#             try:
#                 self.t = paramiko.Transport(sock=(self.ip, 22))
#                 self.t.connect(username=self.username, password=self.password)
#                 self.chan = self.t.open_session()
#                 self.chan.settimeout(self.timeout)
#                 self.chan.get_pty()
#                 self.chan.invoke_shell()
#                 # 如果没有抛出异常说明连接成功，直接返回
#                 print(u'连接%s成功' % self.ip)
#                 # 接收到的网络数据解码为str
#                 print(self.chan.recv(65535).decode('utf-8'))
#                 return
#
#             # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
#
#             except  Exception:
#                 if self.try_times != 0:
#                     print(u'连接%s失败，进行重试' % self.ip)
#                     self.try_times -= 1
#                 else:
#                     print(u'重试3次失败，结束程序')
#                     exit(1)
#     # 断开连接
#     def close(self):
#         self.chan.close()
#         self.t.close()
#
#     # 发送要执行的命令
#     def send(self, cmd,pattern):
#         cmd += '\r'
#         # 通过命令执行提示符来判断命令是否执行完成
#         patt = pattern
#         p = re.compile(patt)
#         result = ''
#         # 发送要执行的命令
#         self.chan.send(cmd)
#         # 回显很长的命令可能执行较久，通过循环分批次取回回显
#         while True:
#             time.sleep(0.5)
#             ret = self.chan.recv(65535)
#             ret = ret.decode('utf-8')
#             result += ret
#             if p.search(ret):
#                 print(result)
#                 return result
#
# #测试linux类代码#
# if __name__ == '__main__':
#     # host = Linux('10.30.1.110', 'long', 'long')
#     host = Linux('10.30.1.110', 'long', 'long')
#     host.connect()
#     host.send('su root',r'.*(]#|密码).*')
#     host.send('storfs_123')
#     host.send('pwd')
#     host.close()
#




# # 4.2定义一个App类调用linux类根据业务需求传入不同的参数实现业务不同的功能。（此时linux类作为一个工具类）
# from common.connectionLinux.Linux import Linux
# class App(object):
#     #主节点服务器IP地址
#     MASTIP = '192.168.1.106'
#     #多个服务器IP地址
#     IPlist = ['192.168.1.107','192.168.1.108','192.168.1.110']
#     def __init__(self):
#         self.host = Linux(self.MASTIP, 'long', 'long')
#     #非root账户登录
#     def connect(self):
#         self.host.connect()
#     #切换root账户登录
#     def sendCmdRoot(self):
#         pattern1 = r'.*(密码).*'
#         pattern2 = r'.*(]#).*'
#         cmd1 = 'su root'
#         cmd2 = '123456'
#         self.host.send(cmd1,pattern1)
#         self.host.send(cmd2,pattern2)
#      #子节点文件拷贝到主节点
#     def copyCmd(self):
#         for ip in self.IPlist:
#             print(ip)
#             pattern = r'.*(]#).*'
#             cmd = 'scp root@'+ip+':/home/long/test.txt /home/long'
#             print(cmd)
#             self.host.send(cmd,pattern)
# if __name__ == '__main__':
#     #连接linux
#     app = App()
#     app.connect()
#     app.sendCmdRoot()
#     app.copyCmd()