# backend/db_config.py
# ============================================
# 数据库配置文件
# ============================================
# 功能：统一管理数据库连接配置，便于维护和修改
# 说明：所有数据库操作都应使用此配置文件中的DB_CONFIG

# ============================================
# 数据库连接配置字典
# ============================================
DB_CONFIG = {
    'host': 'localhost',        # 数据库服务器地址（本地）
    'port': 3306,               # MySQL默认端口
    'user': 'root',             # 数据库用户名
    'password': '123456',       # ⚠️ 请修改为实际数据库密码
    'database': 'audio',        # 数据库名（根据实际情况修改为 audio 或 chatgpt）
    'charset': 'utf8mb4'        # 字符集（支持emoji和特殊字符）
}

# ============================================
# 数据库连接测试函数
# ============================================
def test_connection():
    """
    测试数据库连接是否正常
    
    返回值:
        bool: 连接成功返回True，失败返回False
    
    使用示例:
        if test_connection():
            print("数据库连接正常")
        else:
            print("数据库连接失败，请检查配置")
    """
    try:
        import pymysql
        # 使用配置字典创建数据库连接
        connect = pymysql.Connect(**DB_CONFIG)
        print("✅ 数据库连接成功！")
        connect.close()  # 关闭连接
        return True
    except Exception as e:
        # 连接失败时打印错误信息
        print(f"❌ 数据库连接失败: {e}")
        print("请检查：")
        print("  1. MySQL服务是否启动")
        print("  2. 数据库配置是否正确（host, port, user, password, database）")
        print("  3. 数据库是否已创建")
        return False

# ============================================
# 主程序入口（用于测试）
# ============================================
if __name__ == '__main__':
    """
    直接运行此文件时，测试数据库连接
    使用方法: python db_config.py
    """
    test_connection()

