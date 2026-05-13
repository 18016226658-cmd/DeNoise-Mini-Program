#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量更新 backend/app.py 中的数据库连接配置
将所有硬编码的数据库配置替换为使用 DB_CONFIG
"""

import re

def update_db_connections():
    """更新app.py中的所有数据库连接"""
    file_path = 'app.py'
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义替换模式
    # 匹配 pymysql.Connect( 后面跟着多行配置的模式
    pattern = r'pymysql\.Connect\(\s*host=[\'"]localhost[\'"],\s*port=3306,\s*user=[\'"][^\'"]+[\'"],\s*passwd=[\'"][^\'"]+[\'"],\s*db=[\'"][^\'"]+[\'"],\s*charset=[\'"][^\'"]+[\'"]\s*\)'
    
    # 替换为使用 DB_CONFIG
    replacement = r'''pymysql.Connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        charset=DB_CONFIG['charset']
    )'''
    
    # 执行替换
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ 数据库配置已更新")
    else:
        print("ℹ️ 未发现需要更新的配置")

if __name__ == '__main__':
    update_db_connections()

