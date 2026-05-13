from flask import Flask, jsonify, request

f = Flask(__name__)
app = f
# app.config['SERVER_NAME'] = 'test.com:5000'
i=0

# 在远程服务器上运行 script
def execute_remote_script(hostname, username, password, script):
    import paramiko
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




@app.route('/api/data', methods=['GET'])
def get_data():
    global i
    i=i+1
    data = {'message': f'Hello, World-{i}'}
    print(data)
    return jsonify(data)

@app.route('/api/RemoteRun', methods=['GET'])
def RemoteRun():
    print("========= RemoteRun ================")
    import paramiko
    import os
    import time

    # 定义服务器信息
    hostname = '10.30.1.110'
    username = 'root'
    password = 'Cstorfs_123'
    # 远程服务器存放上传Python文件的文件夹
    server_Path = '/home/tyx'  # 事先应该在人工智能服务器（10.30.1.110）的home下创建 tyx（唐一心）文件夹
    # 应用程序所在的文件夹
    local_Path = os.getcwd()  # D:\chatGPT-Program
    # 要在服务器上运行的在本地应用程序所在的文件夹下的Python文件
    Python_File = 'test.py'  # 注意：程序应该位于 local_Path 文件夹下， 此用户可以自己指定
    # 人工智能服务器上运行的结果文件
    Out_File = 'test.out'  # 用户可以自己指定

    

    print("\n=================== 开始（Begin......)========================\n")
    print("返回操作系统类型（ windows:nt  linux:posix）:")
    print(os.name)  # 返回操作系统 windows:nt linux:posix
    print("返回当前工作目录:")
    print(os.getcwd())  # 返回当前工作目录，Unicode字符串形式返回 D:\untitled1

    # (1）在本地 登录远程人工智能的Linux 虚拟机 （10.30.1.110）
    print("\n=============================================================\n")
    print(f"1-1 在远程服务器（{hostname}）上运行 liunx 命令: ls  -l ")
    script = "ls -l"
    execute_remote_script(hostname, username, password, script)

    # （2）-1 查看当前 虚拟环境下安装的包  conda  list
    print("\n=============================================================\n")
    print("2-1 查看当前 虚拟环境 (conda env export) :")
    script = "conda env export"
    execute_remote_script(hostname, username, password, script)

    # （2）-2 激活 虚拟环境  conda activate py3.7-Tensorflow
    print("\n=============================================================\n")
    print("2-2:激活 虚拟环境  conda activate py3.7-Tensorflow :")
    script = "conda activate py3.7-Tensorflow"
    execute_remote_script(hostname, username, password, script)

    # print("\n=============================================================\n")
    # # （2）-3 查看当前 虚拟环境下安装的包  conda  list
    # print("2-3 查看激活新的虚拟环境后的虚拟环境信息 (conda env export) :")
    # script ="conda env export"
    # execute_remote_script(hostname, username, password, script)

    # （3）  把本地的 py文件（temp-001.py 或 test.py) 上传到 10.30.1.110 的 /home/tyx/temp-001.py 或  /home/tyx/test.py
    print("\n=============================================================\n")
    Local_Python_File = local_Path + '/' + Python_File  # 要上传到服务器上运行的本地文件
    Server_Python_File = server_Path + '/' + Python_File  # 上传到服务器上要运行的文件
    Server_Out_File = server_Path + '/' + Out_File  # 服务器上 生成的程序运行结果文件
    Local_Out_File = local_Path + '/' + Out_File  # 服务器上 生成的程序运行结果下载到本地的路径

    print(f"3-0 把本地的 py文件（{Local_Python_File}) 上传到 人工智能平台（{hostname}） 的 {Server_Python_File} ")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # 将本地 Local_Python_File 文件 上传到 人工智能服务器的  Server_Python_File
    # sftp.put(r'D:\chatGPT-Program\test.py', '/home/tyx/test.py')
    sftp.put(Local_Python_File, Server_Python_File)
    # sftp.close()

    # (4） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
    print("\n=============================================================\n")
    # 动态生成 script
    # script ="nohup python /home/tyx/test.py > /home/tyx/test.out"
    script = "nohup python " + Server_Python_File + ' > ' + Server_Out_File
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
    script = "cat " + Server_Out_File
    execute_remote_script(hostname, username, password, script)

    print("\n===================  The  End  ==============================\n")

    # ==========================
    global i
    i=i+1
    # import Remote_Run   as  RR
    data = {'message': f'RemoteRun-{i}'}
    print(data)
    return jsonify(data)



if __name__ == '__main__':
    app.run()



# from flask import Flask, jsonify, request
#
# app = Flask(__name__)
#
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     data = {'message': 'Hello, World!'}
#     return jsonify(data)
#
# if __name__ == '__main__':
#     app.run()

'''
wx.request({
  url: 'https://your-server-url/api', // 设置Flask API的URL
  method: 'POST',
  header: {
    'Content-Type': 'application/json' // 设置请求头为JSON类型
  },
  data: JSON.stringify({param1: value1}), // 设置参数，可以自定义字段和值
  success: function (res) {
    console.log('成功', res); // 打印返回结果
  },
  fail: function () {
    console.error('失败');
  }
})
'''