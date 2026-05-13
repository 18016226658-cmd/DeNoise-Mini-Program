# backend/api/auth.py
# ============================================
# 用户认证相关接口路由模块
# ============================================

from flask import Blueprint, request, jsonify
import pymysql
import json
from datetime import datetime
from db_config import DB_CONFIG

auth_bp = Blueprint('auth', __name__)

# ============================================
# 1. 用户登录接口（手机号+密码）
# ============================================
@auth_bp.route('/LoginAudio', methods=['POST'])
def login_audio():
    """
    音频登录接口
    验证用户手机号和密码，返回用户信息
    """
    try:
        # 支持 form 和 json 两种格式
        if request.is_json:
            data = request.get_json()
            Phone = data.get('Phone')
            Password = data.get('Password')
        else:
            Phone = request.form.get('Phone')
            Password = request.form.get('Password')
        
        if not Phone or not Password:
            return '0', 200
        
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 先查询用户是否存在
        sql = 'SELECT * FROM users WHERE Phone = %s'
        cursor.execute(sql, (Phone,))
        res = cursor.fetchone()
        
        if not res:
            connect.close()
            return '0', 200
        
        # 验证密码
        if Password != res[3]:  # res[3] 是 Password 字段
            connect.close()
            return '0', 200
        
        # 登录成功，返回用户信息
        user_info = {
            'user_id': res[0],
            'user_Phone': res[1],
            'user_name': res[2],
            'user_Password': res[3],
            'user_RegisterTime': str(res[4]) if res[4] else '',
            'user_Gender': res[5] or '',
            'user_Birthday': str(res[6]) if res[6] else '',
            'user_FaceImg': res[7] or '/static/image/header.png',
            'user_UserType': res[8] or 2,
            'user_MaxNoiseTimes': res[9] if len(res) > 9 and res[9] is not None else 10,
            'user_CurNoiseTimes': res[10] if len(res) > 10 and res[10] is not None else 0,
            'user_MaxSepTimes': res[11] if len(res) > 11 and res[11] is not None else 10,
            'user_CurSepTimes': res[12] if len(res) > 12 and res[12] is not None else 0
        }
        connect.close()
        return json.dumps(user_info, ensure_ascii=False), 200, {"Content-Type": "application/json"}
    except Exception as e:
        print(f"登录失败: {e}")
        import traceback
        traceback.print_exc()
        return '0', 200


# ============================================
# 2. 用户注册接口（手机号+密码）
# ============================================
@auth_bp.route('/RegisterAudio', methods=['POST'])
def register_audio():
    """
    音频注册接口
    注册新用户
    返回值：'0'=成功，'1'=手机号已注册，'2'=注册失败
    """
    try:
        # 支持 form 和 json 两种格式
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        Phone = data.get('Phone')
        UserName = data.get('UserName')
        Password = data.get('Password')
        Gender = data.get('Gender', '')
        Birthday = data.get('Birthday', '')
        FaceImg = data.get('FaceImg', '/static/image/header.png')
        
        if not Phone or not UserName or not Password:
            return '2', 200
        
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 检查手机号是否已存在
        sql_check = 'SELECT * FROM users WHERE Phone = %s'
        cursor.execute(sql_check, (Phone,))
        if cursor.fetchone():
            connect.close()
            return '1', 200  # 手机号已注册
        
        # 插入新用户
        sql_insert = """
            INSERT INTO users 
            (Phone, UserName, Password, RegisterTime, Gender, Birthday, FaceImg, UserType, MaxNoiseTimes, CurNoiseTimes, MaxSepTimes, CurSepTimes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert, (
            Phone, UserName, Password, datetime.now(), Gender, Birthday if Birthday else None, FaceImg,
            2, 10, 0, 10, 0  # 默认普通用户，降噪和分离各10次
        ))
        connect.commit()
        connect.close()
        
        return '0', 200  # 注册成功
    except Exception as e:
        print(f"注册失败: {e}")
        import traceback
        traceback.print_exc()
        return '2', 200  # 注册失败


# ============================================
# 3. 编辑用户接口（获取用户列表）
# ============================================
@auth_bp.route('/EditUser', methods=['POST'])
def edit_user():
    """
    获取用户列表接口
    """
    try:
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        sql = 'SELECT * FROM users'
        cursor.execute(sql)
        res = cursor.fetchall()
        connect.close()
        
        listData = []
        if res:
            for k in range(0, len(res)):
                real_dict = res[k]
                dict1 = {
                    'Phone': real_dict[1],
                    'UserName': real_dict[2],
                    'Password': real_dict[3],
                    'Gender': real_dict[5],
                    'Birthday': str(real_dict[6]) if real_dict[6] else '',
                    'RegisterTime': str(real_dict[4]),
                    'FaceImg': real_dict[7] or '',
                    'UserType': real_dict[8]
                }
                listData.append(dict1)
            
            return json.dumps(listData, ensure_ascii=False), 200, {"Content-Type": "application/json"}
        else:
            return json.dumps([]), 200, {"Content-Type": "application/json"}
    except Exception as e:
        print(f"获取用户列表失败: {e}")
        return json.dumps([]), 200, {"Content-Type": "application/json"}

