    # # (4） 在人工智能的Linux 虚拟机 （10.30.1.110）上运行 /home/tyx/test.py
    # # 动态生成 script
    # script = "nohup python " + Server_Python_File + ' > ' + Server_Out_File
    # print(f"4-0 在远程服务器（{hostname}）后台运行 Python 程序（{script} :")
    # execute_remote_script(hostname, username, password, script)
    #
    # # (五） 下载生成的  /home/tyx/test.out
    # print(f"5-0 把服务器上的运行结果文件（{Server_Out_File}) 下载到 {Local_Out_File} ")
    # sftp.get(Server_Out_File, Local_Out_File)
    #
    # # 关闭sftp
    # sftp.close()
    # # 关闭ssh
    # ssh.close()
    #

 #*****************************************************************

# Login登录路由
@app.route('/api/Login', methods=[ 'POST'])
def Login():
    # 读取微信小程序前端表单 （input）数据
    Phone = request.form.get("Phone")
    Password = request.form.get("Password")
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',      # 数据库用户名
        passwd='123456',  # 密码
        db='chatGPT',     # 数据库名
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    # 先获取是否存在用户(手机号）数据
    sql = 'select * from users where Phone=%s'
    # 执行sql语句，筛选在拼接
    cursor.execute(sql, (Phone,))
    # 获取所有返回结果
    res = cursor.fetchall()  # 结果是列表套字典
    # 关闭数据库连接
    connect.close()

    # 如果存在该用户，再判断密码是否存在
    if res:
        # 效验密码(索引0 获取真正的列表里面的字典)
        real_dict = res[0]

        # 如果密码也正确，为合法用户，需要保存该用户对应的所有信息
        if Password == real_dict[3]:
            myUserName = real_dict[2]
            myUserType = int(real_dict[8])  #转为 int

            #构造一个字典 Dict 型数据
            data = {
                "user_name": myUserName,
                "user_UserType": myUserType,
            }

            # 转为json
            res_json = json.dumps(data)

            # 用于实现Flask后端向微信小程序前端页面 传递数据！
            return res_json, 200, {"Content-Type": "application/json"}

        else:
            print('密码错误')
            return '0'
    else:
        print('用户名不存在 ')
        return '0'

















# 本代码SaveUserType()用于 批量删除注册用户
@app.route('/api/SaveUserType', methods=[ 'POST'])
def SaveUserType():
    UserTypeList = request.form.get("UserTypeList")  # “1,2,8,5,5,5”     整个是一个大的字符串
    UserIDList = request.form.get("UserIDList")      # “1,2,3,28,29,33”

    # 分割成字符串列表
    UserType = UserTypeList.split(",")  # ['1', '2', '8', '5', '5', '5']
    UserID = UserIDList.split(",")      # ['1', '2', '3', '28', '29', '33']

    myUserTypeList = UserType
    myUserIDList = UserID

    try:
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',  # 数据库用户名
            passwd='123456',  # 密码
            db='chatGPT',
            charset='utf8'
        )

        # 获取游标
        cursor = connect.cursor()

        # 遍历每一个 记录
        for k in range(0,len(myUserTypeList)):
            UT = eval(myUserTypeList[k])   # 转为 int   因为表结构中 UserType 为 int   取出第 k个用户的 UserType
            ID = eval(myUserIDList [k])    # 转为 int   因为表结构中 UserID 为 int     取出第 k个用户的 UserID
            # 构造更新 语句 SQL
            # 将  UserID={ID} 用户的 UserType 修改为  {UT}
            update_sql = f'UPDATE users SET UserType = {UT} Where  UserID={ID}'
            print(update_sql)

            # 执行批量更新
            cursor.execute(update_sql)

            # 提交更改并关闭连接
            connect.commit()


        return "成功更新"

    except Exception as e:
        print("Error:", str(e))
        # 发生错误时回滚事务
        connect.rollback()
        return "更新失败"
    finally:
        # 关闭游标和连接
        cursor.close()
        connect.close()
