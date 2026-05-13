#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
后端启动测试脚本
功能：测试后端服务能否正常启动，检查所有关键组件
"""

import sys
import os

# 设置编码，避免Windows控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("后端启动测试")
print("=" * 60)
print()

# 步骤1：检查Python版本
print("[1/6] 检查Python版本...")
print(f"  Python版本: {sys.version}")
print(f"  Python路径: {sys.executable}")
if sys.version_info < (3, 7):
    print("  [错误] Python版本过低，需要3.7+")
    sys.exit(1)
print("  [成功] Python版本符合要求")
print()

# 步骤2：检查依赖包
print("[2/6] 检查依赖包...")
try:
    import flask
    import flask_cors
    import pymysql
    import pandas
    import scipy
    import pydub
    import numpy
    import mutagen
    import jieba
    import snownlp
    import matplotlib
    import requests
    print("  [成功] 核心依赖包已安装")
except ImportError as e:
    print(f"  [错误] 缺失依赖包: {e}")
    print("  请运行: pip install -r requirements.txt")
    sys.exit(1)
print()

# 步骤3：检查数据库配置
print("[3/6] 检查数据库配置...")
try:
    from db_config import DB_CONFIG
    print(f"  [成功] 数据库配置已加载")
    print(f"  数据库: {DB_CONFIG.get('database', 'N/A')}")
    print(f"  主机: {DB_CONFIG.get('host', 'N/A')}")
except ImportError:
    print("  [警告] db_config.py不存在，将使用默认配置")
except Exception as e:
    print(f"  [警告] 数据库配置加载失败: {e}")
print()

# 步骤4：测试数据库连接
print("[4/6] 测试数据库连接...")
try:
    from db_config import test_connection
    if test_connection():
        print("  [成功] 数据库连接正常")
    else:
        print("  [警告] 数据库连接失败，但服务仍可启动（部分功能可能不可用）")
except Exception as e:
    print(f"  [警告] 数据库连接测试失败: {e}")
print()

# 步骤5：导入Flask应用
print("[5/6] 导入Flask应用...")
try:
    # 过滤警告
    import warnings
    warnings.filterwarnings("ignore")
    os.environ['PYTHONWARNINGS'] = 'ignore'
    
    from app import app
    print(f"  [成功] Flask应用已导入")
    print(f"  App类型: {type(app)}")
    
    # 检查蓝图注册
    blueprint_count = len(app.blueprints)
    print(f"  已注册蓝图数: {blueprint_count}")
    
except Exception as e:
    print(f"  [错误] Flask应用导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# 步骤6：检查路由
print("[6/6] 检查路由...")
try:
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(rule.rule)
    
    print(f"  [成功] 共找到 {len(routes)} 个路由")
    print("  主要路由:")
    for route in sorted(routes)[:10]:  # 显示前10个
        print(f"    - {route}")
    if len(routes) > 10:
        print(f"    ... 还有 {len(routes) - 10} 个路由")
except Exception as e:
    print(f"  [警告] 路由检查失败: {e}")
print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
print()
print("如果所有检查都通过，可以运行以下命令启动服务：")
print("  python run.py")
print()













