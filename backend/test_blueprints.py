#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试蓝图导入 - 找出哪个蓝图导致崩溃
"""

import sys
import os

# 基础设置
import warnings
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置 matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

print("=" * 60)
print("测试蓝图导入")
print("=" * 60)

# 测试1: 导入 user 蓝图
print("\n[1/4] 测试 user 蓝图...")
try:
    from routes.user import user_bp
    print("  [成功] user 蓝图导入成功")
except Exception as e:
    print(f"  [失败] user 蓝图导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: 导入 audio 蓝图
print("\n[2/4] 测试 audio 蓝图...")
try:
    from routes.audio import audio_bp
    print("  [成功] audio 蓝图导入成功")
except Exception as e:
    print(f"  [失败] audio 蓝图导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3: 导入 ai 蓝图
print("\n[3/4] 测试 ai 蓝图...")
try:
    from routes.ai import ai_bp
    print("  [成功] ai 蓝图导入成功")
except Exception as e:
    print(f"  [失败] ai 蓝图导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4: 导入 data 蓝图
print("\n[4/4] 测试 data 蓝图...")
try:
    from routes.data import data_bp
    print("  [成功] data 蓝图导入成功")
except Exception as e:
    print(f"  [失败] data 蓝图导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("蓝图测试完成")
print("=" * 60)

# 测试导入 app
print("\n测试导入 app 模块...")
try:
    from app import app
    print("  [成功] app 模块导入成功")
    print(f"  [信息] 蓝图数量: {len(app.blueprints)}")
except Exception as e:
    print(f"  [失败] app 模块导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n所有测试完成！")

