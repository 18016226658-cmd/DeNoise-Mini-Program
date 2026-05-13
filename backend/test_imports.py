#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试导入脚本 - 用于诊断崩溃问题
逐步导入各个库，找出导致崩溃的库
"""

import sys
import traceback

print("=" * 60)
print("开始测试导入...")
print("=" * 60)

# 测试1: 基础库
print("\n[1/10] 测试基础库...")
try:
    import warnings
    warnings.filterwarnings("ignore")
    import os
    os.environ['PYTHONWARNINGS'] = 'ignore'
    print("  [成功] 基础库导入成功")
except Exception as e:
    print(f"  [失败] 基础库导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试2: Flask
print("\n[2/10] 测试 Flask...")
try:
    from flask import Flask, jsonify, request, send_from_directory
    from flask_cors import CORS
    print("  [成功] Flask 导入成功")
except Exception as e:
    print(f"  [失败] Flask 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试3: 数据库
print("\n[3/10] 测试数据库库...")
try:
    import pymysql.cursors
    print("  [成功] pymysql 导入成功")
except Exception as e:
    print(f"  [失败] pymysql 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试4: 数据处理
print("\n[4/10] 测试数据处理库...")
try:
    import pandas as pd
    print("  [成功] pandas 导入成功")
except Exception as e:
    print(f"  [失败] pandas 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试5: numpy
print("\n[5/10] 测试 numpy...")
try:
    import numpy as np
    print("  [成功] numpy 导入成功")
except Exception as e:
    print(f"  [失败] numpy 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试6: matplotlib
print("\n[6/10] 测试 matplotlib...")
try:
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    print("  [成功] matplotlib 导入成功")
except Exception as e:
    print(f"  [失败] matplotlib 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试7: scipy
print("\n[7/10] 测试 scipy...")
try:
    from scipy.signal import butter, filtfilt
    print("  [成功] scipy 导入成功")
except Exception as e:
    print(f"  [失败] scipy 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试8: pydub
print("\n[8/10] 测试 pydub...")
try:
    from pydub import AudioSegment
    print("  [成功] pydub 导入成功")
except Exception as e:
    print(f"  [失败] pydub 导入失败: {e}")
    print("  [提示] pydub 需要 ffmpeg，请确保已安装")
    traceback.print_exc()
    sys.exit(1)

# 测试9: mutagen
print("\n[9/10] 测试 mutagen...")
try:
    import mutagen
    print("  [成功] mutagen 导入成功")
except Exception as e:
    print(f"  [失败] mutagen 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试10: 其他库
print("\n[10/10] 测试其他库...")
try:
    from snownlp import SnowNLP
    import requests
    import jieba
    print("  [成功] 其他库导入成功")
except Exception as e:
    print(f"  [失败] 其他库导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[成功] 所有库导入测试通过！")
print("=" * 60)
print("\n如果所有测试都通过，但仍然崩溃，可能是库之间的交互问题。")
print("请尝试重新安装可能有问题的库：")
print("  pip install --upgrade --force-reinstall numpy scipy matplotlib pydub")
