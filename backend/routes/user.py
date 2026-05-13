# routes/user.py
# ============================================
# 用户相关接口路由模块
# ============================================
# 功能：处理用户登录、注册、用户管理等API接口
# 说明：使用Flask Blueprint实现模块化路由管理

# ============================================
# 1. 导入依赖库
# ============================================
from flask import Blueprint, request, jsonify  # Flask框架相关
import pymysql                                  # MySQL数据库连接
import json                                     # JSON数据处理
import datetime                                 # 日期时间处理
from db_config import DB_CONFIG                 # 数据库配置

# ============================================
# 2. 创建蓝图对象
# ============================================
# Blueprint用于将路由组织成模块，便于代码管理和维护
user_bp = Blueprint('user', __name__)

# ============================================
# 3. 音频登录接口
# ============================================
@user_bp.route('/api/LoginAudio', methods=['POST'])
def login_audio():
    """
    音频登录接口
    ===========
    功能：验证用户手机号和密码，返回用户信息
    
    请求参数（form表单）:
        Phone (str): 用户手机号
        Password (str): 用户密码
    
    返回值:
        成功: JSON格式的用户信息（状态码200）
        失败: 字符串'0'（手机号不存在或密码错误）
    
    用户信息字段说明:
        - user_id: 用户ID（自增主键）
        - user_Phone: 手机号
        - user_name: 用户名
        - user_Password: 密码
        - user_Gender: 性别
        - user_RegisterTime: 注册时间
        - user_Birthday: 出生日期
        - user_FaceImg: 头像路径
        - user_UserType: 用户类型（1-管理员，2-普通用户，3-游客）
        - user_MaxSepTimes: 音频分离最大次数
        - user_CurSepTimes: 音频分离当前已用次数
        - user_MaxNoiseTimes: 音频降噪最大次数
        - user_CurNoiseTimes: 音频降噪当前已用次数
    """
    print("================== @app.route('/api/LoginAudio', methods=[ 'POST']) ============================")
    
    # 3.1 获取请求参数
    Phone = request.form.get("Phone")      # 从form表单获取手机号
    Password = request.form.get("Password")  # 从form表单获取密码
    
    print(Phone, Password)
    
    try:
        # 3.2 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)  # 使用配置连接数据库
        cursor = connect.cursor()               # 创建游标对象
        
        # 3.3 查询用户信息（使用参数化查询防止SQL注入）
        sql = 'select * from users where Phone=%s'
        cursor.execute(sql, (Phone,))  # 参数化查询，Phone作为参数传入
        res = cursor.fetchall()        # 获取查询结果
        
        # 3.4 验证用户信息
        if res:
            # 用户存在，检查密码
            real_dict = res[0]  # 获取第一条记录（手机号唯一，应该只有一条）
            
            # 提取用户信息（根据数据库表结构索引）
            # 注意：这里使用索引访问，如果表结构改变需要相应修改
            if Password == real_dict[3]:  # 验证密码（索引3对应Password字段）
                # 密码正确，提取所有用户信息
                myid = real_dict[0]                    # UserID
                myPhone = real_dict[1]                 # Phone
                myUserName = real_dict[2]              # UserName
                myPassword = real_dict[3]              # Password
                myRegisterTime = str(real_dict[4])     # RegisterTime
                myGender = real_dict[5]                # Gender
                myBirthday = str(real_dict[6])         # Birthday
                myFaceImg = real_dict[7]               # FaceImg
                myUserType = int(real_dict[8])         # UserType
                myMaxSepTimes = int(real_dict[9])      # MaxSepTimes
                myCurSepTimes = int(real_dict[10])     # CurSepTimes
                myMaxNoiseTimes = int(real_dict[11])   # MaxNoiseTimes
                myCurNoiseTimes = int(real_dict[12])   # CurNoiseTimes
                
                print('登录成功')
                
                # 3.5 构建返回数据
                data = {
                    "user_id": myid,
                    "user_Phone": myPhone,
                    "user_name": myUserName,
                    "user_Password": myPassword,
                    "user_Gender": myGender,
                    "user_RegisterTime": myRegisterTime,
                    "user_Birthday": myBirthday,
                    "user_FaceImg": myFaceImg,
                    "user_UserType": myUserType,
                    "user_MaxSepTimes": myMaxSepTimes,
                    "user_CurSepTimes": myCurSepTimes,
                    "user_MaxNoiseTimes": myMaxNoiseTimes,
                    "user_CurNoiseTimes": myCurNoiseTimes,
                }
                
                # 3.6 返回JSON格式的用户信息
                res_json = json.dumps(data)
                connect.close()  # 关闭数据库连接
                return res_json, 200, {"Content-Type": "application/json"}
            else:
                # 密码错误
                print('密码错误')
                connect.close()
                return '0'
        else:
            # 用户不存在
            print('用户名不存在')
            connect.close()
            return '0'
    except Exception as e:
        # 异常处理：登录过程中出现错误
        print(f"登录失败: {e}")
        return '0'

# ============================================
# 4. 音频注册接口
# ============================================
@user_bp.route('/api/RegisterAudio', methods=['POST'])
def register_audio():
    """
    音频注册接口
    ===========
    功能：注册新用户账号
    
    请求参数（form表单）:
        Phone (str): 用户手机号（必填，唯一）
        UserName (str): 用户名（必填）
        Password (str): 密码（必填）
        Birthday (str): 出生日期（可选，格式：YYYY-MM-DD）
        Gender (str): 性别（可选，'男'或'女'）
        FaceImg (str): 头像路径（可选，默认：/static/image/header.png）
    
    返回值:
        '0': 注册成功
        '1': 手机号已注册
        '2': 注册失败（数据库错误）
    
    默认配额设置:
        - UserType: 3（游客）
        - MaxSepTimes: 3（音频分离最大3次）
        - CurSepTimes: 0（当前已用0次）
        - MaxNoiseTimes: 3（音频降噪最大3次）
        - CurNoiseTimes: 0（当前已用0次）
    """
    global FaceImg
    print("================== @app.route('/api/RegisterAudio', methods=[ 'POST']) ============================")
    
    # 4.1 获取请求参数
    Phone = request.form.get("Phone")
    UserName = request.form.get("UserName")
    Password = request.form.get("Password")
    Birthday = request.form.get("Birthday")
    Gender = request.form.get("Gender")
    # 头像路径：优先使用请求参数，否则使用默认值
    FaceImg = request.form.get("FaceImg") or FaceImg or "/static/image/header.png"
    
    # 4.2 设置默认值
    RegisterTime = str(datetime.datetime.now())  # 注册时间：当前时间
    UserType = int(3)          # 用户类型：3-游客（默认）
    MaxSepTimes = int(3)       # 音频分离最大次数：3次
    CurSepTimes = int(0)       # 音频分离当前已用次数：0次
    MaxNoiseTimes = int(3)     # 音频降噪最大次数：3次
    CurNoiseTimes = int(0)     # 音频降噪当前已用次数：0次
    
    print(Phone, UserName, Gender, Birthday, RegisterTime, Password, FaceImg, UserType)
    
    try:
        # 4.3 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 4.4 检测手机号是否已注册（防止重复注册）
        sql = 'select * from users where Phone=%s'
        cursor.execute(sql, (Phone,))  # 使用参数化查询
        res = cursor.fetchall()
        
        if res:
            # 手机号已存在
            print('该手机号已经注册过！')
            connect.close()
            return '1'  # 返回'1'表示手机号已注册
        
        # 4.5 插入新用户数据（使用参数化查询防止SQL注入）
        sql = "INSERT INTO users(Phone, UserName, Gender, Birthday, RegisterTime, Password, FaceImg, UserType, MaxSepTimes, CurSepTimes, MaxNoiseTimes, CurNoiseTimes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # 准备插入的数据（元组格式）
        data = (Phone, UserName, Gender, Birthday, RegisterTime, Password, FaceImg, UserType, MaxSepTimes, CurSepTimes, MaxNoiseTimes, CurNoiseTimes)
        cursor.execute(sql, data)  # 执行插入操作
        connect.commit()            # 提交事务
        print('成功保存注册账号信息')
        connect.close()
        return '0'  # 返回'0'表示注册成功
    except Exception as e:
        # 异常处理：注册过程中出现错误（如数据库连接失败、SQL语法错误等）
        print(f"注册失败 ERR: {e}")
        import traceback
        traceback.print_exc()  # 打印详细错误堆栈
        return '2'  # 返回'2'表示注册失败

# ============================================
# 5. 获取用户列表接口
# ============================================
@user_bp.route('/api/EditUser', methods=['POST'])
def edit_user():
    """
    获取用户列表接口
    ===============
    功能：获取系统中所有注册用户的信息列表
    
    请求参数:
        无（POST请求，但不需要参数）
    
    返回值:
        成功: JSON数组，包含所有用户信息（状态码200）
        失败: 空数组 []（状态码200）
    
    用户信息字段:
        - Phone: 手机号
        - UserName: 用户名
        - Password: 密码
        - Gender: 性别
        - Birthday: 出生日期
        - RegisterTime: 注册时间
        - FaceImg: 头像路径
        - UserType: 用户类型（1-管理员，2-普通用户，3-游客）
    
    使用场景:
        - 管理员查看所有用户
        - 用户管理页面显示用户列表
    """
    try:
        # 5.1 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 5.2 查询所有用户（注意：生产环境应添加分页和权限检查）
        sql = 'select * from users'
        cursor.execute(sql)
        res = cursor.fetchall()  # 获取所有查询结果
        connect.close()
        
        # 5.3 构建用户列表
        listData = []
        if res:
            # 遍历查询结果，提取用户信息
            for k in range(0, len(res)):
                real_dict = res[k]  # 获取第k条记录
                
                # 提取用户字段（根据数据库表结构索引）
                myPhone = real_dict[1]                 # Phone
                myUserName = real_dict[2]              # UserName
                myPassword = real_dict[3]              # Password
                myRegisterTime = str(real_dict[4])      # RegisterTime（转为字符串）
                myGender = real_dict[5]                # Gender
                myBirthday = str(real_dict[6])         # Birthday（转为字符串）
                myFaceImg = real_dict[7]               # FaceImg
                myUserType = real_dict[8]              # UserType
                # 处理配额字段，确保None值被转换为默认值
                myMaxSepTimes = int(real_dict[9]) if len(real_dict) > 9 and real_dict[9] is not None else 10      # MaxSepTimes
                myCurSepTimes = int(real_dict[10]) if len(real_dict) > 10 and real_dict[10] is not None else 0      # CurSepTimes
                myMaxNoiseTimes = int(real_dict[11]) if len(real_dict) > 11 and real_dict[11] is not None else 10  # MaxNoiseTimes
                myCurNoiseTimes = int(real_dict[12]) if len(real_dict) > 12 and real_dict[12] is not None else 0   # CurNoiseTimes
                
                # 构建用户信息字典
                dict1 = {
                    'Phone': myPhone,
                    'UserName': myUserName,
                    'Password': myPassword,
                    'Gender': myGender,
                    'Birthday': myBirthday,
                    'RegisterTime': myRegisterTime,
                    'FaceImg': myFaceImg,
                    'UserType': myUserType,
                    'MaxSepTimes': myMaxSepTimes,
                    'CurSepTimes': myCurSepTimes,
                    'MaxNoiseTimes': myMaxNoiseTimes,
                    'CurNoiseTimes': myCurNoiseTimes
                }
                listData.append(dict1)  # 添加到列表
            
            # 5.4 返回用户列表（JSON格式）
            print("所有用户信息：")
            print(listData)
            res_json = json.dumps(listData, ensure_ascii=False)  # ensure_ascii=False支持中文
            return res_json, 200, {"Content-Type": "application/json"}
        else:
            # 数据库中没有用户
            print('注册表为空')
            return json.dumps([]), 200, {"Content-Type": "application/json"}
    except Exception as e:
        # 异常处理：查询失败时返回空数组
        print(f"获取用户列表失败: {e}")
        return json.dumps([]), 200, {"Content-Type": "application/json"}

# ============================================
# 6. 更新用户信息接口
# ============================================
@user_bp.route('/api/UpdateUserInfo', methods=['POST'])
def update_user_info():
    """
    更新用户信息接口
    ===============
    功能：更新用户信息（用户名、性别、生日、用户类型等）
    
    权限控制:
        - 管理员（UserType=1）可以修改所有用户信息
        - 普通用户（UserType=2）只能修改自己的信息
        - 游客（UserType=3）只能修改自己的信息
    
    请求参数（JSON）:
        currentUserPhone (str): 当前登录用户的手机号（用于权限验证）
        currentUserType (int): 当前登录用户的类型（1-管理员，2-普通用户，3-游客）
        targetPhone (str): 要修改的目标用户手机号
        UserName (str, 可选): 新用户名
        Gender (str, 可选): 新性别（'男'或'女'）
        Birthday (str, 可选): 新生日（格式：YYYY-MM-DD）
        UserType (int, 可选): 新用户类型（仅管理员可修改，1-管理员，2-普通用户，3-游客）
        MaxSepTimes (int, 可选): 音频分离最大次数（仅管理员可修改）
        MaxNoiseTimes (int, 可选): 音频降噪最大次数（仅管理员可修改）
    
    返回值:
        成功: {"success": true, "message": "更新成功"}
        失败: {"success": false, "message": "错误信息"}
    """
    try:
        # 6.1 获取请求参数
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        currentUserPhone = data.get("currentUserPhone")
        currentUserType = int(data.get("currentUserType", 2))
        targetPhone = data.get("targetPhone")
        
        # 6.2 参数验证
        if not currentUserPhone or not targetPhone:
            return jsonify({
                "success": False,
                "message": "缺少必要参数：currentUserPhone 或 targetPhone"
            }), 400
        
        # 6.3 权限验证
        # 普通用户和游客只能修改自己的信息
        if currentUserType != 1 and currentUserPhone != targetPhone:
            return jsonify({
                "success": False,
                "message": "权限不足：只能修改自己的信息"
            }), 403
        
        # 6.4 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 6.5 检查目标用户是否存在
        sql_check = 'SELECT * FROM users WHERE Phone=%s'
        cursor.execute(sql_check, (targetPhone,))
        target_user = cursor.fetchone()
        
        if not target_user:
            connect.close()
            return jsonify({
                "success": False,
                "message": "目标用户不存在"
            }), 404
        
        # 6.6 构建更新SQL（只更新提供的字段）
        update_fields = []
        update_values = []
        
        # 用户名（所有用户可修改）
        if "UserName" in data and data["UserName"]:
            update_fields.append("UserName=%s")
            update_values.append(data["UserName"])
        
        # 性别（所有用户可修改）
        if "Gender" in data and data["Gender"]:
            update_fields.append("Gender=%s")
            update_values.append(data["Gender"])
        
        # 生日（所有用户可修改）
        if "Birthday" in data and data["Birthday"]:
            update_fields.append("Birthday=%s")
            update_values.append(data["Birthday"])
        
        # 用户类型（仅管理员可修改）
        if "UserType" in data and data["UserType"]:
            if currentUserType != 1:
                connect.close()
                return jsonify({
                    "success": False,
                    "message": "权限不足：只有管理员可以修改用户类型"
                }), 403
            update_fields.append("UserType=%s")
            update_values.append(int(data["UserType"]))
        
        # 音频分离最大次数（仅管理员可修改）
        if "MaxSepTimes" in data and data["MaxSepTimes"] is not None:
            if currentUserType != 1:
                connect.close()
                return jsonify({
                    "success": False,
                    "message": "权限不足：只有管理员可以修改配额"
                }), 403
            update_fields.append("MaxSepTimes=%s")
            update_values.append(int(data["MaxSepTimes"]))
        
        # 音频降噪最大次数（仅管理员可修改）
        if "MaxNoiseTimes" in data and data["MaxNoiseTimes"] is not None:
            if currentUserType != 1:
                connect.close()
                return jsonify({
                    "success": False,
                    "message": "权限不足：只有管理员可以修改配额"
                }), 403
            update_fields.append("MaxNoiseTimes=%s")
            update_values.append(int(data["MaxNoiseTimes"]))
        
        # 6.7 执行更新
        if update_fields:
            update_values.append(targetPhone)  # 添加WHERE条件参数
            sql_update = f"UPDATE users SET {', '.join(update_fields)} WHERE Phone=%s"
            cursor.execute(sql_update, tuple(update_values))
            connect.commit()
            connect.close()
            
            return jsonify({
                "success": True,
                "message": "用户信息更新成功"
            }), 200
        else:
            connect.close()
            return jsonify({
                "success": False,
                "message": "没有需要更新的字段"
            }), 400
            
    except Exception as e:
        print(f"更新用户信息失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"更新失败: {str(e)}"
        }), 500

