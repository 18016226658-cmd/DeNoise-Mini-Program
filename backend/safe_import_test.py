#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全导入测试 - 逐步导入 app.py 的各个部分
"""

import sys
import traceback

print("=" * 60)
print("安全导入测试")
print("=" * 60)

# 步骤1: 基础设置
print("\n[步骤1] 基础设置...")
try:
    import warnings
    warnings.filterwarnings("ignore")
    import os
    os.environ['PYTHONWARNINGS'] = 'ignore'
    print("  [成功] 基础设置完成")
except Exception as e:
    print(f"  [失败] {e}")
    sys.exit(1)

# 步骤2: 导入 Flask
print("\n[步骤2] 导入 Flask...")
try:
    from flask import Flask
    print("  [成功] Flask 导入成功")
except Exception as e:
    print(f"  [失败] {e}")
    sys.exit(1)

# 步骤3: 设置 matplotlib 后端（在导入 app 之前）
print("\n[步骤3] 设置 matplotlib 后端...")
try:
    import matplotlib
    matplotlib.use('Agg')
    print("  [成功] matplotlib 后端设置完成")
except Exception as e:
    print(f"  [警告] matplotlib 后端设置失败: {e}")

# 步骤4: 尝试导入 app
print("\n[步骤4] 导入 app 模块...")
try:
    # 添加当前目录到路径
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 尝试导入
    from app import app
    print("  [成功] app 模块导入成功")
    print(f"  [信息] app 类型: {type(app)}")
    print(f"  [信息] app 是否为 None: {app is None}")
except Exception as e:
    print(f"  [失败] app 模块导入失败: {e}")
    print("\n详细错误信息:")
    traceback.print_exc()
    sys.exit(1)

# 步骤5: 检查蓝图
print("\n[步骤5] 检查蓝图...")
try:
    blueprints = list(app.blueprints.keys())
    print(f"  [成功] 已注册蓝图: {blueprints}")
except Exception as e:
    print(f"  [失败] 检查蓝图失败: {e}")

# 步骤6: 检查路由
print("\n[步骤6] 检查路由...")
try:
    routes = [r.rule for r in app.url_map.iter_rules() if r.endpoint != 'static']
    print(f"  [成功] 共找到 {len(routes)} 个路由")
    if len(routes) > 0:
        print(f"  [示例] 前5个路由: {routes[:5]}")
except Exception as e:
    print(f"  [失败] 检查路由失败: {e}")

print("\n" + "=" * 60)
print("[成功] 所有测试通过！app 模块可以正常导入。")
print("=" * 60)
print("\n如果这里测试通过，但 run.py 仍然崩溃，")
print("可能是 run.py 中的某些操作导致的问题。")

