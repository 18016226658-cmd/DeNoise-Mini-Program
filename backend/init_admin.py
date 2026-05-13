# backend/init_admin.py
# ============================================
# 初始化管理员账号脚本
# ============================================
# 功能：创建默认管理员账号
# 使用方法: python init_admin.py

import pymysql
from db_config import DB_CONFIG
from datetime import datetime

def init_admin():
    """
    初始化管理员账号
    手机号: 180162226658
    密码: zy6658
    用户类型: 1 (管理员)
    """
    try:
        # 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 检查管理员是否已存在
        phone = '18016226658'
        sql_check = 'SELECT * FROM users WHERE Phone = %s'
        cursor.execute(sql_check, (phone,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # 如果已存在，更新为管理员
            sql_update = """
                UPDATE users 
                SET UserName = %s, 
                    Password = %s, 
                    UserType = %s,
                    MaxNoiseTimes = %s,
                    CurNoiseTimes = %s,
                    MaxSepTimes = %s,
                    CurSepTimes = %s
                WHERE Phone = %s
            """
            cursor.execute(sql_update, (
                '管理员',
                'zy6658',
                1,  # 管理员
                999,  # 最大降噪次数
                0,   # 当前降噪次数
                999,  # 最大分离次数
                0,   # 当前分离次数
                phone
            ))
            connect.commit()
            print(f"✅ 管理员账号已更新: {phone}")
        else:
            # 如果不存在，创建新管理员
            sql_insert = """
                INSERT INTO users 
                (Phone, UserName, Password, RegisterTime, Gender, Birthday, FaceImg, UserType, MaxSepTimes, CurSepTimes, MaxNoiseTimes, CurNoiseTimes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (
                phone,
                '管理员',
                'zy6658',
                datetime.now(),
                '男',
                '1990-01-01',
                '/static/image/header.png',
                1,  # 管理员
                999,  # 最大分离次数
                0,   # 当前分离次数
                999,  # 最大降噪次数
                0    # 当前降噪次数
            ))
            connect.commit()
            print(f"✅ 管理员账号已创建: {phone}")
        
        connect.close()
        return True
    except Exception as e:
        print(f"❌ 初始化管理员账号失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("开始初始化管理员账号...")
    if init_admin():
        print("管理员账号初始化完成！")
        print("手机号: 180162226658")
        print("密码: zy6658")
        print("用户类型: 管理员 (UserType=1)")
    else:
        print("管理员账号初始化失败！")

