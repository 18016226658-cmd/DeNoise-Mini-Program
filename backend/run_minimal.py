#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最小启动脚本 - 使用最少的代码，避免所有可能导致崩溃的操作
"""

import sys
import os

# 基础设置
warnings = __import__('warnings')
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置 matplotlib 后端（在导入任何其他库之前）
try:
    matplotlib = __import__('matplotlib')
    matplotlib.use('Agg')
except:
    pass

# 直接导入并启动，不进行任何检查
try:
    from app import app
    print("服务器启动中...")
    print("地址: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
except KeyboardInterrupt:
    print("\n已停止")
except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)

